import get_files
import re
import os
import argparse
from collections import OrderedDict


def _get_cat(parent_dat_folder):
    cat_folder = os.path.join(parent_dat_folder, 'cat')
    if not os.path.exists(cat_folder):
        raise ValueError("""Cannot find directory containing
                concatenated dat files""")
    return cat_folder


def get_dat_files(parent_dir, filter_func):
    dat_dirs = get_files.main(parent_dir, pattern='.dat')
    return list(filter(filter_func, dat_dirs))


def get_dates(s):
    pattern1 = r'\d{4}-\d{2}-\d{2}'
    pattern2 = r'\d{4}\_\d{2}\_\d{2}'

    if re.search(pattern1, s):
        date = re.search(pattern1, s)[0]
    elif re.search(pattern2, s):
        date = re.search(pattern2, s)[0]
    else:
        raise ValueError("Cannot find date in filename: {}".format(s))
    return date


def get_dates_todo(todo, done):
    s1, s2 = set(todo), set(done)
    return s1.difference(s2)


def _filter_by_string(iterable, string_filter):
    '''given an iterable of strings, return only those containing a
    '''
    return list(filter(lambda x: string_filter in x, iterable))


def _check_for_conditions(files):
    num_conditions = sum(map(bool, files))
    try:
        assert bool(list(filter(_get_PRE_file, files)))
    except AssertionError:
        raise ValueError("NO PRE file found")
    return num_conditions


def _order_files(files, num_conditions):
    funcs = [_get_PRE_file, _get_cond_file, _get_way_file]

    ordered_files = []
    for i in range(num_conditions):
        ordered_files.append(list(filter(funcs[i], files)))

    ordered_files = [x[0] for x in ordered_files]
    return ordered_files


def _get_PRE_file(s):
    ''' function for finding the baseline date file'''
    s = s.upper()
    pattern = r'..-..-.._PRE$'
    return bool(re.search(pattern, s))


def _get_cond_file(s):
    '''function for finding the experimental condition file
    '''
    s = s.upper()
    pattern1 = r'_CIT$'
    pattern2 = r'_SAL$'
    pattern3 = r'_CNO$'
    match = False
    if re.search(pattern1, s):
        match = re.search(pattern1, s)
    elif re.search(pattern2, s):
        match = re.search(pattern2, s)
    elif re.search(pattern3, s):
        match = re.search(pattern3, s)

    return bool(match)


def _get_way_file(s):
    s = s.upper()
    pattern = r'..-..-.._WAY$'
    return bool(re.search(pattern, s))


def _concatenate_files(file_list, output_file):
    file_list = [os.path.join(x, os.path.basename(x)) +
                 '.dat' for x in file_list]
    call_string = ' '.join(file_list)
    call_string = ' '.join(['cat', call_string, '>', output_file])
    if not os.path.exists(os.path.dirname(output_file)):
        os.mkdir(os.path.dirname(output_file))

    print('''Calling:\n\n{}\n\n

        '''.format(call_string))
    resp = os.system(call_string)
    if resp:
        print('Response from shell:\n\n'.format(resp))

    print('=' * 30)


def main(parent_dat_dir, parent_cat_dir=None):
    '''Given a parent directory of dat files and optionally a parent
    concattenated directory, concatenates all appropriate (in order)
    that have not yet been done so.

    '''
    if parent_cat_dir is None:
        parent_cat_dir = _get_cat(parent_dat_dir)

    path_date_map = OrderedDict()
    labels = ['parent_dat_dir', 'parent_cat_dir']
    for i, parent_dir in enumerate([parent_dat_dir, parent_cat_dir]):
        if i == 0:  # hacky way to prevent recursion of os.walk
            def filter_func(x): return 'cat' not in x
        else:
            def filter_func(x): return x

        dat_dirs = get_dat_files(parent_dir, filter_func)
        dates = list(map(get_dates, dat_dirs))
        path_date_map[labels[i]] = OrderedDict(zip(dat_dirs, dates))

    dat_dir_dates, cat_dir_dates = path_date_map[labels[0]].values(
    ), path_date_map[labels[1]].values()
    dates_todo = get_dates_todo(dat_dir_dates, cat_dir_dates)
    for date in dates_todo:
        paths_todo = _filter_by_string(path_date_map[labels[0]], date)
        try:
            num_conditions = _check_for_conditions(paths_todo)
            ordered_files = _order_files(paths_todo, num_conditions)
        except ValueError:
            print("Date: {}".format(date))
            raise
        _concatenate_files(ordered_files,
                           os.path.join(parent_cat_dir, date, date) + '.dat')


def _get_args():
    parser = argparse.ArgumentParser(
        description='''Script for automating preprocessing of in vivo
        ephys probe data.\n

        Problem it automates: for every experiment you perform, you split
        data into three files:\n
        \t...PRE.dat:[baseline data];
        \t...SAL/CIT.dat [experimental condition]; and
        \t...WAY.dat [second experimental condition]

        This script concatenates all of these files (in order) to one file.
        Uses the unix "cat" command line function.

        Only performs concatenation on files not already concatenated.''')

    parser.add_argument('-d', '--dat_file_dir', required=True,
                        help='''path to directory of pre concattenated
                        dat files''')
    parser.add_argument('-c', '--cat_folder', required=False,
                        help='''path to the directory of concatenated dat files.

                        Defaults to a join of dat_file_dir with \'cat\'''')
    return vars(parser.parse_args())


if __name__ == '__main__':
    args = _get_args()
    main(args['dat_file_dir'], args['cat_folder'])

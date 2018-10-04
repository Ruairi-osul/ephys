import argparse
import os


def get_args():
    parser = argparse.ArgumentParser(description='''Given a list of directories,
        outputs the unique directories in each''')
    parser.add_argument('-d', '--directory_list', help='''list of
        directories to search. Enter as comma-separated list''', required=True)
    args = parser.parse_args()
    return vars(args)


def print_differences(d):
    for good_dr in d.keys():
        print('=' * 20)
        print('\n' * 3)

        good_files = d[good_dr]
        for bad_dr in d.keys():
            if bad_dr == good_dr:
                continue
            bad_files = d[bad_dr]
            good_not_bad = good_files.difference(bad_files)

            print('In {gd} but not in {bd}:\n'.format(gd=good_dr,
                                                      bd=bad_dr))
            if good_not_bad:
                for f in good_not_bad:
                    print(''.join(['\t', f]))
            print('\t ')
        print('=' * 20)


def main(dir_list):
    dir_dict = {}
    for d in dir_list:
        dir_dict[d] = set(os.listdir(d))
    print_differences(dir_dict)


if __name__ == '__main__':
    args = get_args()
    main(dir_list=args['directory_list'].split(','))

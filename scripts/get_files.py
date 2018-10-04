import os
import argparse
from glob import glob as glb
from functools import partial


def get_subdirs_with_ext(datfile_dir, pattern='.npy'):
    '''Given a directory and file extention, returns a list subdirectories
    containing files with the extention

    returns: list of strings (absolute paths)
    '''

    sub_dirs = [x[0] for x in os.walk(datfile_dir)]
    func = partial(_contains_pattern, pattern=pattern)
    return list(filter(func, sub_dirs))


def _contains_pattern(directory, pattern):
    pattern = ''.join(['*', pattern])  # wildcard for glob
    return bool(glb(os.path.join(directory, pattern)))


def _write_file(output_name, dirs):
    if os.path.exists(output_name):
        resp = input('''{} already exists.
            would you like to continue? [y / n + ENTER]'''.format(output_name))
        if 'y' not in resp.lower():
            raise IOError("Please try again with a different output filename")

    with open(output_name, 'w') as file:
        for word in dirs:
            file.write(''.join(word, '\n'))


def _get_options():
    parser = argparse.ArgumentParser(
        description='''Given a directory, get subdirectories containing files
                    of a given extention.

                    Directories are printed to the terminal and
                    optionally written to a file.''')

    parser.add_argument('-p', '--parent_dir', required=True,
                        help='''path to parent directory (containing subdirectories
                        to be searched''')

    parser.add_argument('-e', '--extention', required=False, default='.npy',
                        help='''file extention. make sure to include
                        the "."''')

    parser.add_argument('-o', '--out_file', required=False,
                        help='''path to file created with matching
                        subdirectories''')

    args = parser.parse_args()
    return vars(args)


def main(parent_dir, pattern, out_file=None):
    '''Given a directory, get subdirectories containing files
                    of a given extention.

    Directories are returned and optionally written to a file
    '''
    sub_dirs = get_subdirs_with_ext(parent_dir, pattern)
    if out_file:
        _write_file(out_file)
    return sub_dirs


if __name__ == '__main__':
    args = _get_options()
    sub_dirs = main(parent_dir=args['parent_dir'],
                    pattern=args['extention'],
                    out_file=args['out_file'])
    print(sub_dirs)

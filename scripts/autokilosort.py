import argparse
import os
from py_kilosort import main as kilosort
from glob import glob


def _get_options():
    parser = argparse.ArgumentParser(
        description='''Dectect unspikesorted recordings and
        automatically run kilosort

        ''')

    parser.add_argument('-m', '--master', required=True,
                        help='''path to kilosort master file
                        ''')
    parser.add_argument('-c', '--config', required=True,
                        help='''path to kilosort config file
                        ''')
    parser.add_argument('-p', '--parent', required=True,
                        help='''path to parent folder of dat files to be searched
                        ''')
    return parser.parse_args()


def get_recordings_todo(parent):

    def _walklevel(some_dir, level=1):
        some_dir = some_dir.rstrip(os.path.sep)
        assert os.path.isdir(some_dir)
        num_sep = some_dir.count(os.path.sep)
        for root, dirs, files in os.walk(some_dir):
            yield root, dirs, files
            num_sep_this = root.count(os.path.sep)
            if num_sep + level <= num_sep_this:
                del dirs[:]

    def _hasnot_npy(path):
        return not bool(glob(os.path.join(path, '*.npy')))

    children = [x[0]
                for x in _walklevel(parent, level=1) if os.path.isdir(x[0])]
    if parent in children:
        del children[children.index(parent)]

    dirs_todo = list(filter(_hasnot_npy, children))
    recordings_todo = list(map(lambda x: os.path.join(x, os.path.basename(x)) + '.dat',
                               dirs_todo))
    return recordings_todo


def main(master, config, parent):
    print('working')
    recordings_todo = get_recordings_todo(parent)

    for recording in recordings_todo:
        kilosort(recording=recording, master=master, config=config)


if __name__ == '__main__':
    args = _get_options()
    main(args.master, args.config, args.parent)

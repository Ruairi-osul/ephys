import argparse
from pprint import pprint as pp
import json
import pandas as pd
import os


def _get_options():
    parser = argparse.ArgumentParser(
        description='given a dile')

    parser.add_argument('-j', '--dirs_json', required=True,
                        help='produces a json file of the fields ')

    parser.add_argument('-f', '--file_single', required=False,
                        help='colon-separated file list in full paths')
    parser.add_argument('-d', '--destination', required=False,
                        help='specify output destination, if you like')

    parser.add_argument('-m', '--directory_mapper', required=False,
                        help='path to mapper csv config file')
    parser.add_argument('-n', '--named_file', required=False,
                        help='''named file as in the mapper.csv. 
                        must be suplied in combination with mapper''')
    return parser.parse_args()


def load_json(path):
    with open(path) as json_file:
        out = json.loads(json_file.read())
    return out


def main(paths, **kwargs):
    path_list = paths.split(':')
    if not os.path.isabs(path_list[0]):
        print(kwargs['continuous_dir']


if __name__ == "__main__":
    args = vars(_get_options())
    args.update(load_json(args['dirs_json']))
    if args['file_single']:
        paths = os.path.abspath(args['file_single'])
    elif args['directory_mapper'] and args['named_file']:
        df = pd.read_csv(args['directory_mapper'])
        paths = df[df['probe_dir_names'] == args['named_file']].values[0][0]
        assert paths, 'paths not found'
    else:
        print("invalid arguments found\nmust specify file_single or both directory_mapper and named_file")
        raise ValueError()

    main(paths)

import argparse
from pprint import pprint as pp
import json
import pandas as pd
import os
import numpy as np
from preprocess import loadContinuous
import re


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
                        help='named file as in the mapper.csv'
                        'must be suplied in combination with mapper')
    parser.add_argument('-c', '--chan', default='120_CH1.continuous',
                        help='channel to use')
    return parser.parse_args()


def load_json(path):
    with open(path) as json_file:
        out = json.loads(json_file.read())
    return out


def get_paths(args):
    if args['file_single']:
        paths = os.path.abspath(args['file_single'])
    elif args['directory_mapper'] and args['named_file']:
        df = pd.read_csv(args['directory_mapper'])
        paths = df[df['probe_dir_names'] == args['named_file']].values[0][0]
        assert paths, 'paths not found'
    else:
        err = 'Invalid arguments found\n' \
            'Must specify file_single or both directory_mapper and named_file'
        raise ValueError('\n' + err)

    if args['destination']:
        output_dir = args['destination']
    elif (args['directory_mapper'] and args['named_file']):
        output_dir = os.path.join(args['probe_dat_dir'], args['named_file'])
    else:
        output_dir = os.getcwd()

    return paths, output_dir


def get_date_time_name(path):
    name = os.path.split(path)[-1]
    namei = re.search(r'_\d{4}-\d{2}-\d{2}_', name).start()
    name = name[:namei]
    time = re.search(r'_\d{2}-\d{2}-\d{2}_', path).group(0).replace('_', '')
    date = re.search(r'_\d{4}-\d{2}-\d{2}_', path).group(0).replace('_', '')
    return date, time, name


def main(*args, **kwargs):
    '''
    get date, time, and block times for a recording, store in times.json

    args: paths to continuous file of distinct blocks
    kwargs: can specify output_dir for output file
    '''
    out = {}
    print(args[0][0])
    for block in args[0]:
        n_samps = len(loadContinuous(block)['data'])
        block_name = os.path.split(block)[0]
        ind = re.search(r'_\d{2}-\d{2}-\d{2}_', block).end()
        block_name = block_name[ind:]
        out[block_name] = n_samps

        if 'pr' in block_name.lower():
            date, time, name = get_date_time_name(os.path.split(block)[0])

    out['name'] = name
    out['exp_date'] = date
    out['start_time'] = time

    if not kwargs['output_dir']:
        kwargs['output_dir'] = os.getcwd()
    output_fname = os.path.join(kwargs['output_dir'], 'times.json')
    with open(output_fname, 'w') as f:
        json.dump(out, f, indent=2)


if __name__ == "__main__":
    args = vars(_get_options())
    args.update(load_json(args['dirs_json']))
    paths, output_dir = get_paths(args)

    path_list = paths.split(':')
    path_list = [os.path.join(args['continuous_dir'], p, args['chan'])
                 for p in path_list if not os.path.isabs(p)]

    main(path_list, output_dir=output_dir)

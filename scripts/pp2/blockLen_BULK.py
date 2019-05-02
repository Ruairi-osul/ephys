import argparse
import json
from blockLen_single import main as get_times
import pandas as pd
import os


def _get_options():
    parser = argparse.ArgumentParser(
        description='wrapper for blockLen_single using directory_mapper')

    parser.add_argument('-m', '--directory_mapper', required=True,
                        help='path to direcotry_mapper csv config file')

    parser.add_argument('-j', '--dirs_json', required=True,
                        help='dirs json config file')
    parser.add_argument('-c', '--chan', default='120_CH1.continuous',
                        help='chan to use')
    return parser.parse_args()


def load_json(path):
    with open(path) as f:
        out = json.loads(f.read())
    return out


def main(dir_mapper, probe_dir, continious_dir, chan):
    for i in range(len(dir_mapper)):
        continuous_paths, probe_dirname = dir_mapper.iloc[i, :].values
        continuous_list = continuous_paths.split(':')
        continuous_list = list(
            map(lambda x: os.path.join(continious_dir, x, chan), continuous_list))
        out_dir = os.path.join(probe_dir, probe_dirname)

        if not os.path.isdir(out_dir):
            print(f"**** Skipping****\n: {out_dir}")
            continue
        get_times(continuous_list, output_dir=out_dir)


if __name__ == "__main__":
    args = vars(_get_options())
    args.update(load_json(args['dirs_json']))
    dir_mapper = pd.read_csv(args['directory_mapper'])

    main(dir_mapper=dir_mapper, probe_dir=args['probe_dat_dir'],
         continious_dir=args['continuous_dir'], chan=args['chan'])

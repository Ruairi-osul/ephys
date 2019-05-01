import argparse
from pprint import pprint as pp
import pandas as pd
import json
import os
from preprocess import loadContinuous
import numpy as np


def _get_options():
    parser = argparse.ArgumentParser(
        description='Get bulk timstamps using directory mapper and dir.json')
    parser.add_argument('-j', '--dirs_json', required=True,
                        help='path to dirs.json config file')
    parser.add_argument('-m', '--directory_mapper', required=True,
                        help='path to directory_mapper.csv config file')
    parser.add_argument('-a', '--adc_file', default='120_ADC8.continuous',
                        help='name of adc file containing the timestamps')
    parser.add_argument('-b', '--block', default='shock',
                        help='name of the block on which timestamps can be found')

    return parser.parse_args()


def load_json(path):
    with open(path) as json_file:
        out = json.loads(json_file.read())
    return out


def get_timestamps(arr, threshold=2.51):
    increasers = np.diff(arr)
    return np.argwhere(increasers > threshold).flatten()


def to_csv(arr, destination):
    df = pd.DataFrame({'sample': arr})
    df.to_csv(os.path.join(destination, 'timestamps.csv'), index=False)


def main(df_m, continuous_dir, probe_dat_dir, block, adc):

    for i in range(len(df_m)):

        paths, name = df_m.iloc[i, :].values
        path_out = os.path.join(probe_dat_dir, name)
        paths = paths.split(':')

        if len(paths) == 1:
            print(f"skipping {name}\n")
            continue
        pre, exp = paths[0], paths[1]
        # quick check for correct ordering of files
        assert exp.split('_')[-1].lower()[:2] == block.lower()[
            :2], f'Block names do not match \nexp: {exp}, \nblock: {block}'
        pre, exp = os.path.join(
            continuous_dir, pre, adc), os.path.join(continuous_dir, exp, adc)

        try:
            pre, exp = loadContinuous(pre)['data'], loadContinuous(exp)['data']
        except:
            print(f"***error*** when loading {name}\ncontinuing...")
            continue

        all_data = np.concatenate([pre, exp])
        timestamps = get_timestamps(all_data)

        try:
            assert len(timestamps) > 0
        except AssertionError:
            print('No timestamps found on recordings'
                  f'pre: {pre}\nexp: {exp}')
            raise AssertionError()

        to_csv(timestamps, path_out)


if __name__ == "__main__":
    args = vars(_get_options())
    args.update(load_json(args['dirs_json']))
    df = pd.read_csv(args['directory_mapper'])

    main(df_m=df, continuous_dir=args['continuous_dir'],
         probe_dat_dir=args['probe_dat_dir'], block=args['block'],
         adc=args['adc_file'])

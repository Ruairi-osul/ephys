import pandas as pd
import numpy as np
import argparse
import os
import sys
from preprocess import loadContinuous


def _get_options():
    parser = argparse.ArgumentParser(
        description='''Concatenate and Extract Timestamps from ADC files''')
    parser.add_argument('-p', '--path', required=True,
                        help='''Path to ADC files. 
                        *** Separate pre_path.continuous,exp_path.continuous with : COLONS : ***''')
    parser.add_argument('-d', '--destination', required=False,
                        help='''specify the directory for the output file to be written''')
    return parser.parse_args()


def get_timestamps(arr, threshold=2.51):
    increasers = np.diff(arr)
    return np.argwhere(increasers > threshold).flatten()


def to_csv(arr, destination):
    df = pd.DataFrame({'sample': arr})
    df.to_csv(os.path.join(destination, 'timestamps.csv'), index=False)


def main(pre_path, exp_path, destination):
    pre = loadContinuous(pre_path)['data']
    exp = loadContinuous(exp_path)['data']
    cat = np.concatenate([pre, exp])
    time_stamps = get_timestamps(cat)
    to_csv(time_stamps, destination)


if __name__ == "__main__":
    args = vars(_get_options())
    if 'destination' not in args.keys():
        args['destination'] = os.getcwd()
    pre_path, exp_path = args['path'].split(':')
    main(pre_path=pre_path,
         exp_path=exp_path,
         destination=args['destination'])

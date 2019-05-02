import argparse
from preprocess import get_spike_times, load_dat_data, get_waveforms
from functools import partial
import pandas as pd
import os
import json
import numpy as np


def _get_options():
    parser = argparse.ArgumentParser(
        description='get waveforms from a single file')

    parser.add_argument('-j', '--dirs_json', required=False,
                        help='path to dirs.json config file')
    parser.add_argument('-f', '--dat_file_dir', required=False,
                        help='path to directory where raw data dat file is located')
    parser.add_argument('-a', '--all', action='store_true',
                        help='use this flag to run all. must be used in combination with dirs.json')

    return parser.parse_args()


def load_json(path):
    with open(path) as f:
        out = json.loads(f.read())
    return out


def get_paths(args):
    if not os.path.isabs(args['dat_file_dir']):
        assert args['dirs_json'], 'Must either pass full path or dirs.json config file'
        dat_file_dir = os.path.join(
            args['probe_dat_dir'], args['dat_file_dir'])
        name = args['dat_file_dir']
    else:
        dat_file_dir = args['dat_file_dir']
        name = os.path.split(args['dat_file_dir'])[-1]
    return dat_file_dir, name


def main(dat_file_dir, name):
    spike_df = get_spike_times(dat_file_dir, r_id=name, mua=False)
    if len(spike_df) == 0:
        return
    waveforms, chans = get_waveforms(spike_df, dat_file_dir)

    waves_out = os.path.join(dat_file_dir, 'waveforms.csv')
    waveforms.to_csv(waves_out, index=False)

    chans_out = os.path.join(dat_file_dir, 'chans.csv')
    chans.to_csv(chans_out, index=False)

    spikes_out = os.path.join(dat_file_dir, 'good_spikes.csv')
    spike_df.to_csv(spikes_out, index=False)


if __name__ == "__main__":
    args = vars(_get_options())
    args.update(load_json(args['dirs_json']))

    if not args['all']:
        dat_file_dir, name = get_paths(args)
        main(dat_file_dir, name)
    else:
        assert args['dirs_json'], 'must pass dirs.json for running batch'
        for name in os.listdir(args['probe_dat_dir']):
            print(name)
            dat_file_dir = os.path.join(args['probe_dat_dir'], name)
            main(dat_file_dir, name)

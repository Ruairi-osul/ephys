import argparse
import json
import re
from pathlib import Path
import pandas as pd
import os
from pprint import pprint as pp


def _get_options():
    parser = argparse.ArgumentParser(
        description='''create mapping of continuous files to dat files \
                       output is a csv file''')

    parser.add_argument('-c', '--config_json', required=True,
                        help='''path to config json specifying the paths of \
                                directories to be mapped.
                                Required fields: continuous_dir''')

    parser.add_argument('-d', '--destination', required=False,
                        help='''path to location of outcut .csv file''')
    return parser.parse_args()


def load_json(path):
    'load json file to dict'
    with open(path) as json_file:
        dict_out = json.loads(json_file.read())
    return dict_out


def get_unique_recordings(dirs):
    'get the ESHOCK_02 or CIT_05 root of the filenames. returns set of unique recordings'
    dates = ("2017", "2018", "2019", "2020", "2021", "2022")
    recording_indicators = []
    for d in dirs:
        for date in dates:
            date_ind = re.search(date, d)
            if date_ind is not None:
                break
        if date_ind is None:
            raise ValueError("could not find date: {}".format(date))

        date_ind = date_ind.start() - 1
        recording_indicators.append(d[:date_ind])
    return set(recording_indicators)


def map_subdirs(s, pattern):
    in_path = re.compile(pattern).match(s)
    if in_path is not None:
        end_ind = re.search(pattern, s).end()
        not_double_loc = 'LOC' not in s[end_ind:end_ind+10].upper()
        return in_path and not_double_loc
    else:
        return False


def main(continuous_dir, probe_dat_dir, destination, blocks):
    continuous_path = Path(continuous_dir)

    # get all subdirectories in the continuous dir
    sub_dirs = [x.parts[-1] for x in continuous_path.iterdir() if x.is_dir()]

    # get unique recordings in the continuous fir
    ui = get_unique_recordings(sub_dirs)

    # map continuous sub_dirs to each unique recording
    m = {i: list(filter(lambda x: map_subdirs(x, i), sub_dirs))
         for i in ui}

    # sort files so that blocks are in the correct order
    # first two chars of block name
    flex_blocks = list(map(lambda x: x[:2], blocks))
    probe_dir_names, continuous_dir_names = [], []
    for k, v in m.items():
        # v is a list of directories, function returns int position in flex_blocks
        sorted_files = (sorted(v, key=lambda x: flex_blocks.index(
            x.split('_')[-1][:2].lower())))
        sorted_files = ':'.join(sorted_files)

        probe_dir_names.append(k)
        continuous_dir_names.append(sorted_files)

    df = pd.DataFrame({"continuous_dir_names": continuous_dir_names,
                       "probe_dir_names": probe_dir_names})
    df.to_csv(destination, index=False)


if __name__ == "__main__":

    args = vars(_get_options())
    args.update(load_json(args['config_json']))
    if args['destination'] is None:
        args['destination'] = os.getcwd()
    args['destination'] = os.path.join(
        args['destination'], 'directory_mapper.csv')

    main(args['continuous_dir'], args['probe_dat_dir'],
         args['destination'], args['blocks'])

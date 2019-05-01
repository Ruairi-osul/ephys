import argparse
from pack_single import main as pack_continous
import os
import json


def _get_options():
    parser = argparse.ArgumentParser(
        description='''Convert all continous files to dat files 
        ''')

    parser.add_argument('-c', '--config_file', required=False,
                        help='''path to the .json config file. 
                                This should contain a "exp_home_dir" field''')

    return parser.parse_args()


def _update_options_from_json(config_file):
    with open(config_file) as file:
        config_options = json.loads(file.read())
    return config_options


def _get_dirs(home_dir):
    '''given an exp home dir, return continuous and temp dirs

    returns: continuous_dir, temp_dat_dir'''
    return (os.path.join(home_dir, 'continuous'),
            os.path.join(home_dir, 'temp_dat_dir'))


def main(continuous_dir, temp_dat_dir, chan_map, reference_method="ave"):
    recordings = os.listdir(args['continuous_dir'])
    for recording in recordings:
        pack_continous(in_dir=continuous_dir,
                       out_dir=temp_dat_dir,
                       recording=recording,
                       chan_map=chan_map,
                       reference_method=reference_method)


if __name__ == "__main__":
    args = vars(_get_options())
    args.update(_update_options_from_json(args['config_file']))
    args['continuous_dir'], args['temp_dat_dir'] = _get_dirs(
        args['exp_home_dir'])

    recordings = os.listdir(args['continuous_dir'])

    main(continuous_dir=args['continuous_dir'],
         temp_dat_dir=args['temp_dat_dir'],
         chan_map=args['chan_map'],
         reference_method=args['reference_method'])

import argparse
import sys
import os
import json
sys.path.append('/home/ruairi/repos/ephys/package')
from preprocess import pack_2


def _get_options():
    parser = argparse.ArgumentParser(
        description='''pack continuous probe files to one dat file
        ''')

    parser.add_argument('-r', '--recording', required=False,
                        help='''recording to convert.
                        can be a path to a single file or a comma-separated

                        ''')

    parser.add_argument('-c', '--config_file', required=True,
                        help='''path to preprocessing_config_file''')
    return parser.parse_args()


def main(in_dir, recording, out_dir, chan_map, reference_method='ave',
         chprefix='CH', session='0', source='100'):

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    in_path = os.path.join(in_dir, recording)
    out_path = os.path.join(out_dir, recording, recording) + '.dat'

    if not os.path.exists(os.path.dirname(out_path)):
        os.mkdir(os.path.dirname(out_path))

    done = False

    try:  # source = 100, session = 0
        pack_2(folderpath=in_path,
               filename=out_path,
               chprefix=chprefix,
               channels=chan_map,
               dref=reference_method,
               session=session,
               source=source)
        done = True
    except (OSError, IndexError):
        print('''\nCould not load data for recording {a}.
                 with session indicator {b} and source indicator {c}.
                 Trying with session indicator {d}
                 and source indicator {e}\n'''.format(a=in_path,
                                                      b=session,
                                                      c=source,
                                                      d='1',
                                                      e='100'))
    if not done:
        try:  # source = 100, session = 1
            pack_2(folderpath=in_path,
                   filename=out_path,
                   chprefix=chprefix,
                   channels=chan_map,
                   dref=reference_method,
                   session='1',
                   source=source)
            done = True
        except (OSError, IndexError):
            print('''\nCould not load data for recording {a}.
                     with session indicator {b} and source indicator {c}.
                     Trying with source indicator {d}
                     and session indicator {e}\n'''.format(a=in_path,
                                                           b='1',
                                                           c='100',
                                                           d='120',
                                                           e='0'))
    if not done:
        try:  # source = 120, session = 0
            pack_2(folderpath=in_path,
                   filename=out_path,
                   chprefix=chprefix,
                   channels=chan_map,
                   dref=reference_method,
                   session=session,
                   source='120')
            done = True
        except (OSError, IndexError):
            print('''\nCould not load data for recording {a}.
                     with session indicator {b} and source indicator {d}.
                     Trying with source indicator {d}
                     and session indicator {e}\n'''.format(a=in_path,
                                                           b='0',
                                                           c='1',
                                                           d='120',
                                                           e='1'))
    if not done:
        try:  # source = 120, session = 1
            pack_2(folderpath=in_path,
                   filename=out_path,
                   chprefix=chprefix,
                   channels=chan_map,
                   dref=reference_method,
                   session='1',
                   source='120')
            done = True
        except (OSError, IndexError) as e:
            print('''Could not load data for recording {a}.
                     with session indicator {b} and source indicator {d}.
                     Trying with source indicator {d}
                     and session indicator {e}'''.format(a=in_path,
                                                         b='0',
                                                         c='1',
                                                         d='120',
                                                         e='2'))
    if not done:
        try:  # source = 120, session = 1
            pack_2(folderpath=in_path,
                   filename=out_path,
                   chprefix=chprefix,
                   channels=chan_map,
                   dref=reference_method,
                   session='2',
                   source='120')
            done = True
        except (OSError, IndexError) as e:
            print('Could not open file {}'.format(in_path))
            raise e

    return out_path


if __name__ == '__main__':
    def _update_options_from_json(config_file):
        with open(config_file) as file:
            config_options = json.loads(file.read())
        return config_options

    def _get_dirs(home_dir):
        '''given an exp home dir, return continuous and temp dirs

        returns: continuous_dir, temp_dat_dir'''
        return (os.path.join(home_dir, 'continuous'),
                os.path.join(home_dir, 'temp_dat_dir'))

    # converting to a dict so that it can be updated with config json
    args = vars(_get_options())
    args.update(_update_options_from_json(args['config_file']))
    args['continuous_dir'], args['temp_dat_dir'] = _get_dirs(
        args['exp_home_dir'])

    if ',' in args['recording']:
        recordings = args['recording'].split(',')
    else:
        recordings = [args['recording']]

    for recording in recordings:
        main(in_dir=args['continuous_dir'],
             recording=recording,
             out_dir=args['temp_dat_dir'],
             chan_map=args['chan_map'],
             reference_method=args['reference_method'])

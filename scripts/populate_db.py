import argparse
import os
from functools import partial
from post_kilosort import main as get_data
from preprocess import get_subfolders, load_table


def _get_options():
    parser = argparse.ArgumentParser(
        description='''given parent dat file dir of
        an experiment, go through each recording and
        add spikes and waveforms to tables
        ''')

    parser.add_argument('-p', '--parent', required=True,
                        help='''parent dir of .dat files with kilosort files in each sub dir''')
    parser.add_argument('-d', '--db_dir',
                        required=False, default='/home/ruairi/data/db',
                        help='path to data base tables')
    return parser.parse_args()


def main(parent, nrns, wvfms, spktms, rcds):
    todo = get_subfolders(parent, containing_filetype='npy', verbose=True)

    for rd in todo:
        nrns, wvfms, spktms = get_data(rd=rd, nrns=nrns,
                                       wvfms=wvfms, spktms=spktms,
                                       rcds=rcds)
            '''
    try:
        add_to_db(nrns)
    except InternalError:
        log.write(error)
    '''
    return nrns, wvfms, spktms


if __name__ == '__main__':
    args = _get_options()
    tlbs_to_load = ['neurons', 'spike_times',
                    'recordings', 'waveform_timepoints']
    loader = partial(load_table, d=args.db_dir)
    nrns, spktms, rcds, wvfms = list(map(loader, tlbs_to_load))
    nrns, wvfms, spktms = main(parent=args.parent, nrns=nrns,
                               spktms=spktms,
                               rcds=rcds,
                               wvfms=wvfms)
    nrns.to_csv(os.path.join(args.db_dir, 'neurons.csv'), index=False)
    spktms.to_csv(os.path.join(args.db_dir, 'spike_times.csv'), index=False)
    wvfms.to_csv(os.path.join(
        args.db_dir, 'waveform_timepoints.csv'), index=False)

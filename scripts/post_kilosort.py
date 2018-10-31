import argparse
import pandas as pd
from preprocess import (get_spike_times, get_waveforms,
                        load_table, update_tble)
import os
from functools import partial
import numpy as np


def _get_options():
    parser = argparse.ArgumentParser(
        description='''FileDescription

        ''')

    parser.add_argument('-d', '--db_dir',
                        required=False, default='/home/ruairi/data/db',
                        help='path to data base')
    parser.add_argument('-r', '--r_dir',
                        required=True,
                        help='path to dir of kilosort files')
    return parser.parse_args()


def _reformat_waveforms(waveforms, nrns):
    # add nrn_id, drop cluster_id
    waveforms = pd.merge(left=waveforms,
                         right=nrns[[
                             'neuron_id', 'cluster_id']],
                         on='cluster_id').drop('cluster_id',
                                               axis=1)
    return waveforms[['neuron_id', 'sample', 'value']]  # rearange columns


def _format_to_nrns(spike_data):
    # add new var: has bl [True if baseline spikes > 800, False otherwise]
    g = spike_data[spike_data['spike_times'] < 108000000].groupby('cluster_id')[
        'spike_times']
    col = g.apply(
        lambda x: 1 if np.sum(x) > 800 else 0)

    # drop spike times
    spike_data = spike_data.drop('spike_times', axis=1).drop_duplicates()
    # add has_bl column
    spike_data = spike_data.set_index('cluster_id').join(col).reset_index()
    spike_data.columns = ['cluster_id', 'recording_id', 'channel', 'has_bl']
    return spike_data


def _reformat_spktms(spike_data, nrns):
    # add neuron_id, drop cluster id, recording id, channel
    spike_data = pd.merge(left=spike_data,
                          right=nrns[['neuron_id', 'cluster_id']],
                          on='cluster_id')
    spike_data.drop(['cluster_id', 'channel', 'recording_id'],
                    axis=1, inplace=True)
    return spike_data[['neuron_id', 'spike_times']]  # rearange columns


def _check_data(tbl1, tbl2, key1, key2):
    m = '''Bad data in table
    {t1}
    and
    {t2}.
    non matching values in keys
    {k1}
    and
    {k2}'''.format(t1=tbl1, t2=tbl2,
                   k1=key1, k2=key2)
    pks1 = set(tbl1[key1].values)
    pks2 = set(tbl2[key2].values)
    assert (not pks1.difference(pks2)) and (not pks2.difference(pks1)), m


def _get_recording_id(rd, r_tbl):
    assert 'dat_filename' in r_tbl.columns, 'Cannot find datfile column'
    name = os.path.basename(rd)
    matches = r_tbl[r_tbl['dat_filename'] == name]['recording_id'].values
    assert len(
        matches) == 1, 'Error finding recording id: {}. multiple IDs found'.format(name)
    return matches[0]


def _get_neurons_todelete(r_id, nrns, spktms, wvfms):
    matches = nrns.loc[nrns['recording_id'] == r_id]
    if len(matches) == 0:
        return nrns, spktms, wvfms

    else:
        m = '''\n\n\nNeurons belonging to this recording have previous been entered
                These neurons are now being deleted before continuing'''
        print(m)
        neuron_ids = matches['neuron_id'].values
        spktms = spktms[~spktms['neuron_id'].isin(neuron_ids)]
        nrns = nrns[~nrns['neuron_id'].isin(neuron_ids)]
        wvfms = wvfms[~wvfms['neuron_id'].isin(neuron_ids)]

    return nrns, spktms, wvfms


def main(rd, nrns, wvfms, spktms, rcds, v=True):
    '''given a path to a recording dir and db tables,
    returns tables updated with spike times and waveforms
    from that recording

    returns:
        neurons table, waveforms table, spike times table
    '''
    if v:
        print('\n' * 3)
        print('Getting data for {}'.format(os.path.basename(rd)))

    # extracting and reformatting new data
    r_id = _get_recording_id(rd=rd, r_tbl=rcds)
    if v:
        print('Extracting spike times...')
    nrns, spktms, wvfms = _get_neurons_todelete(r_id, nrns, spktms, wvfms)
    spike_data = get_spike_times(p=rd, r_id=r_id)
    if v:
        print('Extracting waveforms...')
    waveforms, chans = get_waveforms(spike_data=spike_data, rd=rd)
    spike_data = pd.merge(spike_data, chans, on='cluster_id')

    if v:
        print('Updating tables...')
    # updating existing tables
    nrns = update_tble(tbl=nrns,
                       n_data=_format_to_nrns(spike_data),
                       ind_name=nrns.columns[0])
    wvfms = update_tble(tbl=wvfms,
                        n_data=_reformat_waveforms(waveforms, nrns),
                        ind_name=wvfms.columns[0])
    spktms = update_tble(tbl=spktms,
                         n_data=_reformat_spktms(spike_data, nrns),
                         ind_name=spktms.columns[0])
    return nrns, wvfms, spktms


if __name__ == '__main__':
    args = _get_options()

    tlbs_to_load = ['neurons', 'spike_times',
                    'recordings', 'waveform_timepoints']
    loader = partial(load_table, d=args.db_dir)
    try:
        nrns, spktms, rcds, wvfms = list(map(loader, tlbs_to_load))
        _check_data(nrns, spktms, 'neuron_id', 'neuron_id')
    except (ValueError, AssertionError):
        print('Error on data import')
        raise ValueError


    nrns, wvfms, spktms = main(rd=args.r_dir,
                               nrns=nrns,
                               spktms=spktms,
                               rcds=rcds,
                               wvfms=wvfms)
    nrns.to_csv(os.path.join(args.db_dir, 'neurons.csv'), index=False)
    spktms.to_csv(os.path.join(args.db_dir, 'spike_times.csv'), index=False)
    wvfms.to_csv(os.path.join(
        args.db_dir, 'waveform_timepoints.csv'), index=False)

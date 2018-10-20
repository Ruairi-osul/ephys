import argparse
import pandas as pd
from preprocess import load_kilosort_arrays, get_good_cluster_numbers, gen_df
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


def load_table(table=None, d=None):
    '''given a parent path and table name, returns table as pandas df

    params:
        d = parent dir of db tables
        table = name of table. can be path to table if d not specified
    '''

    assert table, 'table to load not specified'
    if not table.endswith('.csv'):
        table = ''.join([table, '.csv'])

    if os.path.isabs(table):
        p = table
    else:
        assert d, 'no parent diectory given to load_table'
        p = os.path.join(d, table)

    try:
        return pd.read_csv(p)
    except (IOError, OSError):
        raise ValueError('''\nTable name specified but not found.
            Tried to load: %s''' % p)


def _check_data(tbl1, tbl2, key1, key2):
    m = '''Bad data in table {t1} and {t2}.
        duplicate values in keys {k1} and {k2}'''.format(t1=tbl1, t2=tbl2,
                                                         k1=key1, k2=key2)
    pks1 = set(tbl1[key1].values)
    pks2 = set(tbl2[key2].values)
    assert not pks1.difference(pks2) and not pks2.difference(pks1), m


def _get_recording_id(rd, r_tbl):
    assert 'dat_filename' in r_tbl.columns, 'Cannot find datfile column'
    name = os.path.basename(rd)
    matches = r_tbl[r_tbl['dat_filename'] == name]['recording_id'].values
    assert len(
        matches) == 1, 'Error finding recording id: {}. multiple IDs found'.format(name)
    return matches[0]


def get_spike_times(p, r_id):
    spk_c, spk_tms, c_gps = load_kilosort_arrays(p)
    clusters = get_good_cluster_numbers(c_gps)
    df = gen_df(spk_c, spk_tms, clusters)
    df['recording_id'] = r_id
    return df


def get_waveforms(spike_data, r_id, rd):
    raw_data = _load_dat_data(p=os.path.join(
        rd, os.path.basename(rd)) + '.dat')
    f1 = partial(_extract_waveforms, raw_data=raw_data, ret='data')
    f2 = partial(_extract_waveforms, raw_data=raw_data, ret='')
    waveforms = spike_data.groupby('cluster_id')['spike_times'].apply(
        f1, raw_data=raw_data).apply(pd.Series).reset_index()
    chans = spike_data.groupby('cluster_id')[
        'spike_times'].apply(f2, raw_data=raw_data).apply(pd.Series).reset_index()
    chans.columns = ['cluster_id', 'channel']
    waveforms.columns = ['cluster_id', 'sample', 'value']
    return waveforms, chans


def _load_dat_data(p, n_chans=32):
    tmp = np.memmap(p, dtype=np.int16)
    shp = int(len(tmp) / n_chans)
    return np.memmap(p, dtype=np.int16,
                     shape=(shp, n_chans))


def _extract_waveforms(spk_tms, raw_data, ret='data', n_spks=800, n_samps=240, n_chans=32):
    assert len(spk_tms) > n_spks, 'Not ennough spikes'
    spk_tms = spk_tms.values
    window = np.arange(int(-n_samps / 2), int(n_samps / 2))
    wvfrms = np.zeros((n_spks, n_samps, n_chans))
    for i in range(n_spks):
        srt = int(spk_tms[i] + window[0])
        end = int(spk_tms[i] + window[-1] + 1)
        srt = srt if srt > 0 else 0
        wvfrms[i, :, :] = raw_data[srt:end, :]
    wvfrms = pd.DataFrame(np.mean(wvfrms, axis=0),
                          columns=range(1, n_chans + 1))
    norm = wvfrms - np.mean(wvfrms)
    tmp = norm.apply(np.min, axis=0)
    good_chan = tmp.idxmin()
    wvfrms = wvfrms.loc[:, good_chan]
    if ret == 'data':
        return wvfrms
    else:
        return good_chan


def update_neurons(n_tbl, new_data, r_id):

    def _reformat(new_data):
        g = new_data[new_data['spike_times'] < 108000000].groupby('cluster_id')[
            'spike_times']
        col = g.apply(
            lambda x: 1 if np.sum(x) > 800 else 0)
        new_data = new_data.drop('spike_times', axis=1).drop_duplicates()
        new_data = new_data.set_index('cluster_id').join(col).reset_index()
        new_data.columns = ['cluster_id', 'recording_id', 'channel', 'has_bl']
        return new_data

    new_data = _reformat(new_data)
    if len(n_tbl) == 0:
        out = new_data
        out.index = pd.RangeIndex(0, len(new_data))
    else:
        n_tbl.set_index('neuron_id', inplace=True)
        i = n_tbl.index[-1]
        new_data.index = pd.RangeIndex(i + 1, i + 1 + len(new_data))
        out = pd.concat([n_tbl, new_data])
    out.index.name = 'neuron_id'
    return out.reset_index()


def update_spike_times(s_tbl, n_tbl, n_data):
    n_data = pd.merge(left=n_data, right=n_tbl[[
        'neuron_id', 'cluster_id']], on='cluster_id').drop(['cluster_id', 'recording_id', 'channel'], axis=1)
    n_data = n_data[['neuron_id', 'splike_times']]

    if len(s_tbl) == 0:
        out = n_data
        out.index = pd.RangeIndex(0, len(n_data))
    else:
        s_tbl.set_index('waveform_timepoint_id,', inplace=True)
        i = n_tbl.index[-1]
        n_data.index = pd.RangeIndex(i + 1, i + 1 + len(n_data))
        out = pd.concat([n_tbl, n_data])
    out.index.name = 'spike_time_id,,'
    return out.reset_index()


def update_waveforms(w_tbl, n_tbl, n_data):

    n_data = pd.merge(left=n_data, right=n_tbl[[
        'neuron_id', 'cluster_id']], on='cluster_id').drop('cluster_id', axis=1)
    n_data = n_data[['neuron_id', 'sample', 'value']]

    if len(w_tbl) == 0:
        out = n_data
        out.index = pd.RangeIndex(0, len(n_data))
    else:
        w_tbl.set_index('waveform_timepoint_id,', inplace=True)
        i = n_tbl.index[-1]
        n_data.index = pd.RangeIndex(i + 1, i + 1 + len(n_data))
        out = pd.concat([n_tbl, n_data])

    out.index.name = 'waveform_timepoint_id,'
    return out.reset_index()


def main(rd, nrns, wvfms, spktms, rcds, v=True):
    '''given a path to a recording dir and db tables,
    returns tables updated with spike times and waveforms
    from that recording

    returns:
        neurons table, waveforms table, spike times table
    '''

    r_id = _get_recording_id(rd=rd, r_tbl=rcds)
    spike_data = get_spike_times(p=rd, r_id=r_id)
    waveforms, chans = get_waveforms(spike_data=spike_data, r_id=r_id, rd=rd)
    spike_data = pd.merge(spike_data, chans, on='cluster_id')
    nrns = update_neurons(nrns, spike_data, r_id=r_id)
    wvfms = update_waveforms(w_tbl=wvfms, n_tbl=nrns, n_data=waveforms)
    spktms = update_spike_times(s_tbl=spktms, n_tbl=nrns, n_data=spike_data)
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

    main(rd=args.r_dir,
         nrns=nrns,
         spktms=spktms,
         rcds=rcds,
         wvfms=wvfms)

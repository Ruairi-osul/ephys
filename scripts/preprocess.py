import numpy as np
import pandas as pd
import os


def load_kilosort_arrays(parent_dir):
    '''
    Loads arrays generated during kilosort into numpy arrays and pandas DataFrames
    Parameters:
        parent_dir       = name of the parent_dir being analysed
    Returns:
        spike_clusters  = numpy array of len(num_spikes) identifying the cluster from which each spike arrose
        spike_times     = numpy array of len(num_spikes) identifying the time in samples at which each spike occured
        cluster_groups  = pandas DataDrame with one row per cluster and column 'cluster_group' identifying whether
                          that cluster had been marked as 'Noise', 'MUA' or 'Good'
    '''
    try:
        spike_clusters = np.load(os.path.join(
            parent_dir, 'spike_clusters.npy'))
        spike_times = np.load(os.path.join(parent_dir, 'spike_times.npy'))
        cluster_groups = pd.read_csv(os.path.join(
            parent_dir, 'cluster_groups.csv'), sep='\t')
    except IOError:
        print('Error loading Kilosort Files. Files not found')
        raise
    try:  # check data quality
        assert np.shape(spike_times.flatten()) == np.shape(spike_clusters)
    except AssertionError:
        AssertionError('Array lengths do not match in parent_dir {}'.format(
            parent_dir))
    return spike_clusters, spike_times, cluster_groups


def get_good_cluster_numbers(cluster_groups_df):
    '''
    Takes the cluster_groups pandas DataFrame fomed during data loading and returns a numpy array of cluster
    ids defined as 'Good' during kilosort and phy spike sorting
    Parameters:
        cluster_groups_df   = the pandas DataFrame containing information on which cluster is 'Good', 'Noise' etc.
    Returns:
        A numpy array of 'Good' cluster ids
    '''
    good_clusters_df = cluster_groups_df.loc[cluster_groups_df['group'] == 'good', :]
    return good_clusters_df['cluster_id'].values


def gen_df(spike_clusters, spike_times, good_cluster_nums):
    data = {'cluster_id': spike_clusters.flatten(),
            'spike_times': spike_times.flatten()}
    df = pd.DataFrame(data)
    df = df.loc[df['cluster_id'].isin(good_cluster_nums), :]
    return df


def get_waveforms(recording_id, processed_data_dir, raw_data_dir,
                  neurons_table, recordings_table, spiketimes_table,
                  num_channels=32):

    def _get_spike_times():
        neurons = neurons_table.loc[neurons_table['recording_id']
                                    == recording_id].values
        spike_times = spiketimes_table.loc[spiketimes_table['neuron_id'].isin(
            neurons)]
        return spike_times

    def _load_raw_data():
        dat_filename = recordings_table.loc[recordings_table['recording_id']
                                            == recording_id]['dat_filename'].values[0]

        path = os.path.join(raw_data_dir,
                            dat_filename, dat_filename) + '.dat'
        tmp = np.memmap(path, dtype=np.int16)  # adjust shape
        adjusted_len = int(len(tmp) / num_channels)
        return np.memmap(path, dtype=np.int16,
                         shape=(adjusted_len, num_channels))

    def _extract_waveforms(spike_times, raw_data,
                           num_spikes=1000, num_samples=240,
                           num_chans=32):
        waveform_window = np.arange(
            int(-num_samples / 2), int(num_samples / 2))
        out = []
        channels = []
        for neuron in spike_times['neuron_id'].unique():
            data = spike_times[spike_times['neuron_id']
                               == neuron]['spike_times']
            try:
                assert num_spikes <= len(data)
            except AssertionError:
                raise ValueError(
                    "not enough spikes. neuron: {}".format(neuron))

            waveforms = np.zeros((num_spikes, num_samples, num_chans))
            for i in range(num_spikes):
                start = int(data.iloc[i] + waveform_window[0])
                end = int(data.iloc[i] + waveform_window[-1] + 1)
                if start < 0:
                    start = 0
                waveforms[i, :, :] = raw_data[start:end, :]
            df = pd.DataFrame(np.mean(waveforms, axis=0),
                              columns=[''.join(['Chan_', str(i)]) for
                                       i in range(0, num_chans)])

            df_norm = df - np.mean(df)
            tmp = df_norm.apply(np.min, axis=0)
            chan_label = tmp.idxmin()
            data = df.loc[:, chan_label]
            data.name = neuron
            out.append(data)
            channels.append({'neuron_id': neuron, 'channel': chan_label})

        waveform_data = pd.concat(out, axis=1).transpose()
        waveform_data.index.name = 'neuron_id'
        waveform_data.reset_index(inplace=True)
        channel_info = pd.DataFrame(channels)
        return waveform_data, channel_info

    raw_data = _load_raw_data()
    spike_times = _get_spike_times()
    waveform_data, channel_info = _extract_waveforms(spike_times=spike_times,
                                                     raw_data=raw_data)
    return waveform_data, channel_info


def get_recording_id(subject_table, recording_path):
    try:
        df = pd.read_csv(subject_table)
    except IOError:
        print('''Recording table not found.
              Path searching: {}'''.format(subject_table))
    return df.loc[df['dat_filename'] == os.path.basename(recording_path), :]['recording_id']

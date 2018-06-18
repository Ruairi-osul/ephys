import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')


def load_kilosort_arrays(kilosort_folder, recording, verbose):
    if verbose:
        print('Loading Kilosort arrays: {}\n\n'.format(recording))
    path = os.path.join(kilosort_folder, recording)
    spike_clusters = np.load(os.path.join(path, 'spike_clusters.npy'))
    spike_times = np.load(os.path.join(path, 'spike_times.npy'))
    cluster_groups = pd.read_csv(os.path.join(path, 'cluster_groups.csv'), sep='\t')

    return spike_clusters, spike_times, cluster_groups


def load_raw_data(kilosort_folder, recording, num_channels):
    path = os.path.join(kilosort_folder, recording, recording) + '.dat'
    temp_data = np.memmap(path, dtype=np.int16)
    adjusted_len = int(len(temp_data) / num_channels)  # adjust for number of channels

    raw_data = np.memmap(path, dtype=np.int16, shape=(adjusted_len, num_channels))
    return raw_data


def get_good_cluster_numbers(cluster_groups):
    good_clusters = cluster_groups[cluster_groups['group'] == 'good']
    return good_clusters['cluster_id'].values


def gen_good_spikes_df(spike_times, spike_clusters, good_cluster_numbers):
    all_spikes_df = pd.DataFrame({'spike_time': spike_times.flatten(),
                                  'spike_cluster': spike_clusters.flatten()})
    good_spikes_df = all_spikes_df[all_spikes_df['spike_cluster'].isin(good_cluster_numbers)]
    return good_spikes_df


def gen_spiketimes_series(good_spikes_df, cluster, num_spikes, last_spikes):
    if len(good_spikes_df) < num_spikes:
        num_spikes = len(good_spikes_df)
    if last_spikes:
        spike_times = good_spikes_df[good_spikes_df['spike_cluster'] == cluster].iloc[-num_spikes:]
    else:
        spike_times = good_spikes_df[good_spikes_df['spike_cluster'] == cluster].iloc[num_spikes:]
    spike_times.index = range(len(spike_times))
    return spike_times


def extract_waveforms(num_spikes, num_samples, num_channels,
                      spike_times, raw_data):
    waveform_window = np.arange(-num_samples / 2, num_samples / 2)
    cols = [''.join(['Chan_', str(num)]) for num in range(0, num_channels)]

    if num_spikes >= len(spike_times['spike_time']):
        num_spikes = len(spike_times['spike_time']) - 20

    empty_template = np.zeros((num_spikes, num_samples, num_channels))
    for spike in range(num_spikes):
        start_index = int(spike_times['spike_time'].iloc[spike] + waveform_window[0])
        end_index = int((spike_times['spike_time'].iloc[spike] + waveform_window[-1]) + 1)
        waveform = raw_data[start_index:end_index, :]
        empty_template[spike, :, :] = waveform[:, :]

    waveform_per_chan = np.mean(empty_template, axis=0)
    waveform_per_chan = pd.DataFrame(waveform_per_chan, columns=cols)
    return waveform_per_chan


def choose_channel(df, method, broken_chans):
    '''
    Choose either channel with max or minumum values
    method == 'max' or 'min'
    '''
    if broken_chans:
        for chan in broken_chans:
            df.drop('Chan_{}'.format(str(chan)), inplace=True, axis=1)
    if method.lower() == 'max':
        chan = df.apply(np.max, axis=0)
        selected_chan = df.loc[:, chan.idxmax()]
        chan = chan.idxmax()
    elif method.lower() == 'min':
        chan = df.apply(np.min, axis=0)
        selected_chan = df.loc[:, chan.idxmin()]
        chan = chan.idxmin()
    else:
        raise ValueError('Unable to parse channel selection method.\nEnter \'min\' or\'max\'')

    return selected_chan, chan


def gen_peak_finding_df(chan_df):
    df = pd.DataFrame({'y_values': chan_df})
    df['y_values'] = df['y_values'].rolling(5).mean()
    df['diff'] = df.diff(periods=1)
    df['change'] = (df['diff'] >= 0).map({True: 'increase', False: 'decrease'})
    return df


def calculate_spikewidth(spike_type, fs, cluster, recording, **kwargs):
    divisor = int(round(fs / 1000))
    SWs = {'spike_type': spike_type, 'cluster': cluster, 'recording': recording}
    if spike_type == 'up_down_up':
        try:
            SWs['SW_peak'] = np.absolute(kwargs['peak_sample'] - kwargs['baseline_sample']) / divisor
            SWs['SW_troff'] = np.absolute(kwargs['min_sample'] - kwargs['baseline_sample']) / divisor
            SWs['SW_return'] = np.absolute(kwargs['return_sample'] - kwargs['baseline_sample']) / divisor
            SWs['min_max_amp'] = kwargs['peak_amp'] + np.absolute(kwargs['min_amp'])
            SWs['base_min_amp'] = kwargs['baseline_amp'] + np.absolute(kwargs['min_amp'])
        except:
            SWs['SW_peak'] = np.nan
            SWs['SW_troff'] = np.nan
            SWs['SW_return'] = np.nan
            SWs['min_max_amp'] = np.nan
            SWs['base_min_amp'] = np.nan
    elif spike_type == 'down_up':
        try:
            SWs['SW_peak'] = np.nan
            SWs['SW_troff'] = np.absolute(kwargs['min_sample'] - kwargs['baseline_sample']) / divisor
            SWs['SW_return'] = np.absolute(kwargs['return_sample'] - kwargs['baseline_sample']) / divisor
            SWs['base_min_amp'] = kwargs['baseline_amp'] + np.absolute(kwargs['min_amp'])
        except:
            SWs['SW_peak'] = np.nan
            SWs['SW_troff'] = np.nan
            SWs['SW_return'] = np.nan
            SWs['min_max_amp'] = np.nan
            SWs['base_min_amp'] = np.nan
    return SWs


def find_baseline_return(df, baseline_amp, min_sample):
    try:
        increasing = df.loc[(df['y_values'] < baseline_amp) & (df['change'] == 'increase') & (df.index > min_sample)]

        if (increasing.reset_index().set_index('index', drop=False)['index'].diff() > 1).any():
            last_name = increasing[increasing.reset_index().set_index('index', drop=False)['index'].diff() > 1].iloc[0].name
            increasing = increasing.iloc[:increasing.index.get_loc(last_name)]
        return increasing.iloc[-1].name, increasing.iloc[-1]['y_values']
    except:
        return np.nan


def find_baseline_up_down_up(df, num_samples, thresh):
    '''
    Function to find baseline for up-down-up
    '''
    from_start_to_max = np.arange(2, df['y_values'].iloc[:int(num_samples / 2)].idxmax() + 1, 1)
    for time_point in from_start_to_max:
        if np.absolute(df.loc[time_point][0] - df.loc[time_point - 2][0]) > thresh and df.loc[time_point]['change'] == 'increase':
            return time_point


def up_down_up(df, fig_folder, cluster, recording, num_samples, thresh=10, fs=30000):

    half_samples = int(num_samples / 2)
    peak_amp = df['y_values'].iloc[:half_samples].max()
    peak_sample = df['y_values'].iloc[:half_samples].idxmax()

    min_amp = df['y_values'].min()
    min_sample = df['y_values'].idxmin()

    baseline_amp = peak_amp * 0.05
    baseline_sample = find_baseline_up_down_up(df=df,
                                               num_samples=num_samples,
                                               thresh=thresh)
    return_sample, return_amp = find_baseline_return(df, baseline_amp, min_sample)

    SWs = calculate_spikewidth(spike_type='up_down_up',
                               fs=fs,
                               recording=recording,
                               cluster=cluster,
                               peak_sample=peak_sample,
                               baseline_sample=baseline_sample,
                               baseline_amp=baseline_amp,
                               min_sample=min_sample,
                               peak_amp=peak_amp,
                               return_sample=return_sample,
                               min_amp=min_amp)
    if baseline_sample:
        plot_points(baseline_sample, min_sample, return_sample, df=df, cluster=cluster, fig_folder=fig_folder)
    return pd.DataFrame(SWs, index=[0])


def find_baseline_down_up(df, thresh):
    '''
    Same as standard baseline except the value is the first point where there's a significant y-value DECREASE
    '''

    from_start_to_min = np.arange(2, df['y_values'].idxmin(), 1)
    if len(from_start_to_min) > 1:
        for time_point_for_down_up in from_start_to_min:
            if (np.absolute(df.loc[time_point_for_down_up][0] - df.loc[time_point_for_down_up - 2][0]) > thresh) and (df.loc[time_point_for_down_up]['change'] == 'decrease'):
                return time_point_for_down_up - 4
    else:
        return np.nan


def down_up(df, fig_folder, num_samples, recording, cluster, thresh, chan, fs=30000):
    min_amp = df['y_values'].min()
    min_sample = df['y_values'].idxmin()

    baseline_amp = np.mean(df['y_values'].iloc[:int(num_samples / 2)])
    baseline_sample = find_baseline_down_up(df, thresh)
    try:
        return_sample, return_amp = find_baseline_return(df, baseline_amp, min_sample)
    except:
        return_sample = np.nan
        return_amp = np.nan

    SWs = calculate_spikewidth(spike_type='down_up',
                               fs=fs,
                               recording=recording,
                               cluster=cluster,
                               baseline_sample=baseline_sample,
                               min_sample=min_sample,
                               return_sample=return_sample,
                               baseline_amp=baseline_amp,
                               min_amp=min_amp)
    try:
        plot_points(baseline_sample, min_sample, return_sample, df=df, cluster=cluster, fig_folder=fig_folder)
    finally:
        return pd.DataFrame(SWs, index=[0])


def plot_points(*args, df, cluster, fig_folder):
    f, a = plt.subplots(figsize=(8, 8))
    df['y_values'].plot(ax=a)
    for arg in args:
        x_values = np.ones(2) * arg
        y_values = np.linspace(np.min(df['y_values']), np.max(df['y_values']), 2)
        a.plot(x_values, y_values)
        a.set_title('cluster:\t {}'.format(str(cluster)))
    if not os.path.exists(os.path.join(fig_folder, 'spike_widths')):
        os.mkdir(os.path.join(fig_folder, 'spike_widths'))
    plt.savefig(os.path.join(fig_folder, 'spike_widths') + str(cluster) + '.png')
    plt.close()


def merge_dfs(df_list, broadcast, **kwargs):
    df = pd.concat(df_list)
    df.index = range(len(df))
    if broadcast:
        df['recording'] = kwargs['recording']
    return df


def plot_waveform(all_chans_df, recording, one_chan_df, method, chan, cluster, fig_folder):
    f, a = plt.subplots(figsize=(20, 8), ncols=3)

    all_chans_df.iloc[:, :15].plot(ax=a[0], title='All channels: Shank 1')
    all_chans_df.iloc[:, 15:].plot(ax=a[1], title='All channels: Shank 2')
    one_chan_df.plot(ax=a[2], title='Cluster number {clus}:\t{chan}'.format(clus=str(cluster), chan=chan))
    if not os.path.exists(os.path.join(fig_folder, 'waveforms')):
        os.mkdir(os.path.join(fig_folder, 'waveforms'))
    plt.savefig('_'.join([os.path.join(fig_folder, 'waveforms'), str(recording), str(cluster)]) + '.png')
    plt.close()

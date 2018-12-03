import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz
from scipy import signal as ss
plt.style.use('ggplot')


def load_kilosort_arrays(recording):
    spike_clusters = np.load('spike_clusters.npy')
    spike_times = np.load('spike_times.npy')
    cluster_groups = pd.read_csv('cluster_groups.csv', sep='\t')
    try:  # check data quality
        assert np.shape(spike_times.flatten()) == np.shape(spike_clusters)
    except AssertionError:
        AssertionError('Array lengths do not match in recording {}'.format(
            recording))
    return spike_clusters, spike_times, cluster_groups


def load_raw_data(kilosort_folder, recording, num_channels):
    path = os.path.join(kilosort_folder, recording, recording) + '.dat'
    temp_data = np.memmap(path, dtype=np.int16)
    adjusted_len = int(len(temp_data) / num_channels)  # adjust for number of channels

    raw_data = np.memmap(path, dtype=np.int16, shape=(adjusted_len, num_channels))
    return raw_data


def choosing_spike(extracted_spikes, time_chosen):
    Spike_chosen = (extracted_spikes - time_chosen * 30000).abs().argsort()[:1]
    return Spike_chosen


def load_data(recording, kilosort_folder, verbose):
    if verbose:
        print('\nLoading Data:\t{}\n'.format(recording))
        os.chdir(os.path.join(kilosort_folder, recording))
        spike_clusters, spike_times, cluster_groups = load_kilosort_arrays(
            recording)
    return spike_clusters, spike_times, cluster_groups


def get_good_cluster_numbers(cluster_groups_df):
    good_clusters_df = cluster_groups_df.loc[cluster_groups_df['group'] == 'good', :]
    return good_clusters_df['cluster_id'].values


def band_passfilter(fs, low=None, high=None, order=None):
    low = low / (fs / 2)
    high = high / (fs / 2)
    return ss.butter(N=order, Wn=(low, high), btype='pass')


def apply_filter(array, low, high, fs, order, axis=-1):
    b, a = band_passfilter(fs=fs, low=low, high=high, order=order)
    return ss.filtfilt(b, a, array, axis=axis)


def extract_highlighted_spikes(time_span, extracted_spikes, Spike_chosen):
    num_samples_in_trace = time_span * 30000
    waveform_window = np.arange(int(-num_samples_in_trace / 2), int(num_samples_in_trace / 2))
    start_index = int(extracted_spikes.iloc[Spike_chosen] + waveform_window[0])
    end_index = int((extracted_spikes.iloc[Spike_chosen] + waveform_window[-1]) + 1)
    highlighted_spike_list = extracted_spikes[(start_index <= extracted_spikes) & (extracted_spikes <= end_index)]
    return highlighted_spike_list


def create_3D_matrix(num_spikes_for_averaging, extracted_spikes, data):
    threeD_matrix = np.zeros((num_spikes_for_averaging, 240, 32))
    waveform_window = np.arange(-120, 120)
    for spike in np.arange(0, num_spikes_for_averaging):
        start_index = int(extracted_spikes.iloc[spike] + waveform_window[0])
        end_index = int((extracted_spikes.iloc[spike] + waveform_window[-1]) + 1)

        waveform = data[start_index:end_index, 0:32]
        threeD_matrix[spike, :, :] = waveform[:, :]
    return threeD_matrix


def extract_trace(Spike_chosen, extracted_spikes, time_span, data, chosen_channel):
    start_index, end_index = create_trace_parameters(time_span, extracted_spikes, Spike_chosen)
    filtered_data = apply_filter(array=data[start_index:end_index, chosen_channel], low=400, high=6000, fs=30000, order=4)
    df_trace = pd.DataFrame({'Value': filtered_data})
    df_trace['time'] = np.arange(start_index / 30000, end_index / 30000, 1 / 30000)
    return df_trace


def create_trace_parameters(time_span, extracted_spikes, Spike_chosen):
    num_samples_in_trace = time_span * 30000
    waveform_window = np.arange(int(-num_samples_in_trace / 2), int(num_samples_in_trace / 2))
    start_index = int(extracted_spikes.iloc[Spike_chosen] + waveform_window[0])
    end_index = int((extracted_spikes.iloc[Spike_chosen] + waveform_window[-1]) + 1)
    return start_index, end_index


def choose_channel(Spike_chosen, extracted_spikes, time_span, data, broken_chans, num_spikes_for_averaging):
    start_index, end_index = create_trace_parameters(time_span, extracted_spikes, Spike_chosen)
    temporary_df = pd.DataFrame(data[start_index:end_index])
    if broken_chans:
        for chan in broken_chans:
            temporary_df.drop((chan), inplace=True, axis=1)

    threeD_matrix = create_3D_matrix(num_spikes_for_averaging, extracted_spikes, data)

    mean_waveform = np.mean(threeD_matrix, axis=0)
    waveform_per_channel_df = pd.DataFrame(mean_waveform)
    maxes = waveform_per_channel_df.apply(np.min, axis=0)
    chosen_channel = maxes.idxmin()
    return chosen_channel


def spike_highlight(spike, extracted_spikes, data, chosen_channel):
    window_for_highlight = np.arange(-30, 30)
    start_highlight = int(spike + window_for_highlight[0])
    end_highlight = int((spike + window_for_highlight[-1]) + 1)
    filtered_highlight_data = apply_filter(array=data[start_highlight:end_highlight, chosen_channel], low=400, high=6000, fs=30000, order=4)
    df_highlight = pd.DataFrame({'Value': filtered_highlight_data})
    df_highlight['time'] = np.arange(start_highlight, end_highlight, 1)
    df_highlight_final = pd.DataFrame({'time': df_highlight['time'] / 30000, 'Value': df_highlight['Value']})
    return df_highlight_final


def plot_final_data(kilosort_folder, recording, chosen_channel, chosen_cluster, highlighted_spike_list, time_chosen):
    fig_folder = os.path.join(kilosort_folder, recording, 'figures', 'Cluster no.' + str(chosen_cluster))
    # font = {'fontname': 'Calibri'}
    plt.ylim(-1200, 800)
    plt.tick_params(axis='both', which='major', labelsize=50)
    locs, labels = plt.xticks()
    plt.xticks(np.arange(time_chosen - 2.5, time_chosen + 3.5, 1), np.arange(0, 6, 1.0))
    plt.xlabel('Time [s]', fontsize=70)
    plt.ylabel('Voltage [uV]', fontsize=70)
    plt.title('V.Fast Firing', fontsize=80)
    plt.annotate('no. of spikes: {}'.format(len(highlighted_spike_list)), xy=(time_chosen, 1500), xytext=(time_chosen, 1500), size=30)
    mkdirs_(fig_folder)
    if time_chosen >= 60 * 60:
        figpath = os.path.join(kilosort_folder, recording, 'figures', 'Cluster no.' + str(chosen_cluster), recording + ' Cluster no.' + str(chosen_cluster) + ' After.png')
    else:
        figpath = os.path.join(kilosort_folder, recording, 'figures', 'Cluster no.' + str(chosen_cluster), recording + ' Cluster no.' + str(chosen_cluster) + ' Before.png')
    plt.tight_layout()
    plt.savefig(figpath)


def choose_cluster_to_plot(cluster_groups, spike_clusters, spike_times, chosen_cluster):
    good_cluster_numbers = get_good_cluster_numbers(cluster_groups)
    df = pd.DataFrame({'cluster': spike_clusters.flatten(), 'spike_times': spike_times.flatten()})
    df = df.loc[df['cluster'].isin(good_cluster_numbers)]
    cluster_to_plot = good_cluster_numbers[good_cluster_numbers == chosen_cluster][0]
    return df, cluster_to_plot


def mkdirs_(path):
    if not os.path.exists(path):
        os.mkdir(path)

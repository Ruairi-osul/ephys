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
    spike_clusters = np.load(os.path.join(parent_dir, 'spike_clusters.npy'))
    spike_times = np.load(os.path.join(parent_dir, 'spike_times.npy'))
    cluster_groups = pd.read_csv(os.path.join(
        parent_dir, 'cluster_groups.csv'), sep='\t')
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


def get_recording_id(subject_table, recording_path):
    df = pd.read_csv(subject_table)
    return df.loc[df['dat_filename'] == os.path.basename(recording_path), :]['recording_id']

import os
import numpy as np
import pandas as pd
import NeuroTools.signals as nt
pd.options.mode.chained_assignment = None


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


def load_data(recording, kilosort_folder, verbose, sep):
    if verbose:
        print('\nLoading Data:\t{}\n'.format(recording))
    os.chdir(sep.join([kilosort_folder, recording]))
    spike_clusters, spike_times, cluster_groups = load_kilosort_arrays(
        recording)
    return spike_clusters, spike_times, cluster_groups


def get_good_cluster_numbers(cluster_groups_df):
    good_clusters_df = cluster_groups_df.loc[cluster_groups_df['group'] == 'good', :]
    return good_clusters_df['cluster_id'].values


def create_dirs(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)


def create_good_spikes_df(data, good_cluster_numbers,
                          sampling_rate, verbose, recording, experiment,
                          spikes_df_csv_out_folder, sep):
    if verbose:
        print('Creating creating good_spikes_df')
    df = pd.DataFrame(data)
    df = df.transpose()
    df.rename(columns={0: 'spike_cluster',
                       1: 'spike_time'},
              inplace=True)
    df = df.loc[df['spike_cluster'].isin(good_cluster_numbers), :]

    df['time'] = df['spike_time'].divide(sampling_rate)
    df = df.drop('spike_time', axis=1)
    df = add_condition(df=df, experiment=experiment)

    df.to_csv(return_path(path_to_data=spikes_df_csv_out_folder,
                          recording=recording,
                          sep=sep))
    return df


def return_path(path_to_data, recording, sep):
    recording_folder = sep.join([path_to_data, recording])
    create_dirs(recording_folder)
    return sep.join([recording_folder, recording]) + '.csv'


def add_condition(df, experiment):
    if experiment == 'DREADD':
        df['condition'] = (df['time'] <= 3600).map({True: 'Baseline',
                                                    False: 'CNO'})
    elif experiment == 'CIT':
        def citalopram_mapper(row):
            if row['time'] <= 3600:
                return 'Baseline'
            elif row['time'] <= 3600 * 2:
                return 'CIT'
            else:
                return 'WAY'

        df['condition'] = df.apply(citalopram_mapper, axis=1)
    return df


def get_neuron_chars(df, good_cluster_numbers, verbose, sep, recording, out_dir,
                     condition='Baseline'):
    if verbose:
        print('Extracting Neuron Characteristics')
    df = df.loc[df['condition'] == condition]
    all_neurons_container = {}
    for cluster in good_cluster_numbers:
        neuron = df.loc[df['spike_cluster'] == cluster]
        spike_times = neuron['time'].values * 1000
        try:
            t_start = spike_times[0]
            t_stop = spike_times[-1]
            spike_train_object = nt.SpikeTrain(spike_times,
                                               t_start=t_start,
                                               t_stop=t_stop)
            rate = spike_train_object.mean_rate()
            cv_isi = spike_train_object.cv_isi()
        except IndexError:
            print('Problem with cluster number:\t{}'.format(cluster))
            continue
        neuron_dict = {'cluster': cluster, 'rate': rate, 'cv_isi': cv_isi}
        all_neurons_container[cluster] = neuron_dict
    df = pd.DataFrame(data=all_neurons_container)
    df = df.transpose()
    df = label_neuron_chars(df=df)
    df = df.set_index('cluster')
    df.to_csv(return_path(path_to_data=out_dir,
                          recording=recording,
                          sep=sep))
    return df


def label_neuron_chars(df):
    df['firing_cat'] = (df['rate'] <= 4).map({True: 'slow', False: 'fast'})
    df['regularity_cat'] = (df['cv_isi'] <= 0.6).map({True: 'regular',
                                                      False: 'irregular'})
    df['neuron_category'] = df.apply(concatenate_columns, axis=1)
    return df


def concatenate_columns(row):
    return ' '.join([row['firing_cat'], row['regularity_cat']])

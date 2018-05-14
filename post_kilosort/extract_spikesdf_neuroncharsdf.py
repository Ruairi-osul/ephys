import os
import numpy as np
import pandas as pd
import NeuroTools.signals as nt
pd.options.mode.chained_assignment = None

recordings_to_extract = ['2018-04-18']
kilosort_folder = r'C:\Users\Rory\raw_data\SERT_DREADD\dat_files\cat'
spikes_df_csv_out_folder = r'C:\Users\Rory\raw_data\SERT_DREADD\spikes_df'
nrn_char_out_fol = r'C:\Users\Rory\raw_data\SERT_DREADD\neuron_characteristics'
sampling_rate = 30000
verbose = True


def concatenate_columns(row):
    return ' '.join([row['firing_cat'], row['regularity_cat']])


def add_condition(df, time=3600):
    df['condition'] = (df['time'] <= time).map({True: 'Baseline',
                                                False: 'CNO'})
    return df


def create_dirs(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)


def return_path(path_to_data, recording):
    recording_folder = '\\'.join([path_to_data, recording])
    return '\\'.join([recording_folder, recording]) + '.csv'


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


def create_good_spikes_df(data, good_cluster_numbers, sampling_rate, verbose):
    df = pd.DataFrame(data)
    df = df.transpose()
    df.rename(columns={0: 'spike_cluster',
                       1: 'spike_time'},
              inplace=True)
    df = df.loc[df['spike_cluster'].isin(good_cluster_numbers), :]

    df['time'] = df['spike_time'].divide(sampling_rate)
    df = df.drop('spike_time', axis=1)
    df = add_condition(df=df, time=3600)
    if verbose:
        print('\n\nSpikes df Preview So Far:\n')
        print(df.head())
    return df


def get_good_cluster_numbers(cluster_groups_df):
    good_clusters_df = cluster_groups_df.loc[cluster_groups_df['group']
                                             == 'good', :]
    return good_clusters_df['cluster_id'].values


def get_neuron_chars(df, good_cluster_numbers):
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
    return df


def label_neuron_chars(df):
    df['firing_cat'] = (df['rate'] <= 4).map({True: 'slow', False: 'fast'})
    df['regularity_cat'] = (df['cv_isi'] <= 0.6).map({True: 'regular',
                                                      False: 'irregular'})
    df['neuron_category'] = df.apply(concatenate_columns, axis=1)
    return df


def main():
    create_dirs(spikes_df_csv_out_folder)
    create_dirs(nrn_char_out_fol)

    for recording in recordings_to_extract:
        if verbose:
            print(recording + '\n')
            print('\nLoading Data:\t{}\n'.format(recording))

        os.chdir('\\'.join([kilosort_folder, recording]))

        spike_clusters, spike_times, cluster_groups = load_kilosort_arrays(
            recording)

        good_cluster_numbers = get_good_cluster_numbers(cluster_groups)
        data = [spike_clusters.flatten(), spike_times.flatten()]
        df = create_good_spikes_df(data=data,
                                   good_cluster_numbers=good_cluster_numbers,
                                   sampling_rate=sampling_rate,
                                   verbose=verbose)

        if verbose:
            print('Saving Spikes df to csv')
        df.to_csv('\\'.join([spikes_df_csv_out_folder, recording])
                  + '.csv')

        if verbose:
            print('Extracting Neuron Characteristics')
        df_chars = get_neuron_chars(df=df,
                                    good_cluster_numbers=good_cluster_numbers)
        df_chars = label_neuron_chars(df=df_chars)

        df_chars = df_chars.set_index('cluster')
        if verbose:
            print('Saving Neuron Characteristics Dataframe')
        df_chars.to_csv('\\'.join([nrn_char_out_fol,
                                   recording])
                        + '.csv')


if __name__ == '__main__':
    main()

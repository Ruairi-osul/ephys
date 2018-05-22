import os
import numpy as np
import pandas as pd
import NeuroTools.signals as nt
pd.options.mode.chained_assignment = None


def load_kilosort_arrays(recording):
    '''
    Loads arrays generated during kilosort into numpy arrays and pandas DataFrames
    Parameters:
        recording       = name of the recording being analysed
    Returns:
        spike_clusters  = numpy array of len(num_spikes) identifying the cluster from which each spike arrose
        spike_times     = numpy array of len(num_spikes) identifying the time in samples at which each spike occured
        cluster_groups  = pandas DataDrame with one row per cluster and column 'cluster_group' identifying whether
                          that cluster had been marked as 'Noise', 'MUA' or 'Good'
    '''
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
    '''
    Loads arrays generated during kilosort into numpy arrays and pandas DataFrames
    Parameters:
        recording       = name of the recording being analysed
        kilosort_folder = the name of the root directory in which subdirectories for each recording are stored
                          inside the sub-directories should be the files generated during spike sorting with
                          kilosort and phy
        verbose         = True or False
        sep             = os directory delimeter e.g. '/'
    Returns:
        spike_clusters  = numpy array of len(num_spikes) identifying the cluster from which each spike arrose
        spike_times     = numpy array of len(num_spikes) identifying the time in samples at which each spike occured
        cluster_groups  = pandas DataDrame with one row per cluster and column
                          'cluster_group' identifying whetherthat cluster had been marked as 'Noise', 'MUA' or 'Good'
    '''
    if verbose:
        print('\nLoading Data:\t{}\n'.format(recording))
    os.chdir(sep.join([kilosort_folder, recording]))
    spike_clusters, spike_times, cluster_groups = load_kilosort_arrays(
        recording)
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


def create_dirs(folder):
    '''
    Takes a direcotry and checks whether it already exists, if it doesn't, it creates it
    Parameters:
        folder = folder to make
    '''
    if not os.path.exists(folder):
        os.mkdir(folder)


def create_good_spikes_df(data, good_cluster_numbers,
                          sampling_rate, verbose, recording, experiment,
                          spikes_df_csv_out_folder, sep):
    '''
    Uses numpy arrays containing information generated during kilosort and phy spike sorting
    to generate a tidy csv file with one row per spike and columns containg cluster_id (only 'Good' clusters) and time
    Saves as well as returns tidy csv as a pandas DataFrame
    Parameters:
        data                        = list of arrays contains in spike_cluster and spike_time kilosort files
        good_cluster_numbers        = numpy array of cluster ids of clusters perviously marked as 'Good'
        sampling_rate               = sampling rate of the recording (used to convert between samples and time)
        verbose                     = True or False
        recording                   = name of the recording being analysed
        experiment                  = category of experiment ('CNO' or 'CIT')
        spikes_df_csv_out_folder    = root folder for output csv files
        sep                         = os directory serperator e.g. '/'
    Returns:
        df                          = tidy pandas df of spike information
    '''
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
    '''
    Creates a subdirecotry within the root directory for the recording
    returns the absolute path to a csv file within that directory
    Parameters:
        path_to_data    = name of the root folder for the csv file
        recording       = name of the current recording
        sep             = operating system serperator e.g. '/'
    Returns:
        The absolute path to a csv file in the new subdirectory
    '''
    recording_folder = sep.join([path_to_data, recording])
    create_dirs(recording_folder)
    return sep.join([recording_folder, recording]) + '.csv'


def add_condition(df, experiment):
    '''
    Given the name of the experiment, adds a condtion to a tidy pandas DataFrame
    Parameters:
        df              = pandas DataFrame containg spiking information (one row per spike)
        experiment      = Name of experiment e.g 'CIT' or 'CNO'
    Returns:
        tidy pandas DataFrame with added 'condition' column
    '''
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
    '''
    Takes a tidy pandas DataFrame (one row per spike) and calculates summary statistics over a condition.
    Outputs the result to a csv file
    Parameters:
        df                          = tidy pandas df of spiking data (one row per spike; only good clusters etc.)
        good_cluster_numbers        = array of ids of clusters marked as 'Good' during spike sorting
        verbose                     = True or False
        sep                         = operating system serperator e.g. '/'
        recording                   = name of the recording being analysed
        out_dir                     = root direcotry for output csv
        condition                   = condition over which statistics will be calculated
    '''
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
    '''
    Adds columns to a pandas df containg categories based on firing rates
    Parameters:
        df      = df containg summary statistics of neuron firing patterns
    Returns
        df      = df containg new rows with categorical information
    '''
    df['firing_cat'] = (df['rate'] <= 4).map({True: 'slow', False: 'fast'})
    df['regularity_cat'] = (df['cv_isi'] <= 0.6).map({True: 'regular',
                                                      False: 'irregular'})
    df['neuron_category'] = df.apply(concatenate_columns, axis=1)
    return df


def concatenate_columns(row):
    '''
    Used to concatenate columns of a pandas DataFrame
    '''
    return ' '.join([row['firing_cat'], row['regularity_cat']])

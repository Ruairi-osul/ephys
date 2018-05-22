import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from glob import glob
sns.set()


def load_data(source_folder, recording, sep):
    '''
    Loads power spectrum csv into a pandas DataFrame for all channges in the recording subdirectory of the source folder
    Parameters:
        source_folder   = root folder for csv files
        recording       = name of subdirectory for individual recording. Subdirectory should contain
                          the csv files for each channel
        sep             = operating system directory seperator e.g. '/'
    Returns:
        data            = list of pandas DataFrames corresponding to different channels
        file_names      = list of filenames (index is the same for data; i.e. the label for the first
                          channel is file_names[0] and the corresponding data is found in data[0])
    '''
    data_dir = sep.join([source_folder, recording])
    os.chdir(data_dir)
    file_names = glob("*.csv")
    data = [pd.read_csv(file, index_col=0) for file in file_names]
    return data, file_names


def manipulate_df(df):
    '''
    Manipulates a pandas df such that it is ready for time frequency analysis
    Parameters:
        df              = pandas DataFrame
    Returns:
        log_df          = logged values of df
        low_freqs_df    = logged values of df indexed such that only the low frequencies are present
    '''
    log_df = np.log(df)
    log_df.reset_index(inplace=True)
    log_df['time'] = pd.to_timedelta(log_df['time'])
    log_df.set_index('time', inplace=True)
    low_freqs_df = log_df.iloc[:, :80]
    return log_df, low_freqs_df


def plot_mean_power(dfs, recording, chan_lab, both, dpi,
                    fig_out_folder, verbose, sep):
    '''
    Takes a pandas DataFrame and plots mean power density accross all time periods
    Parameters:
        dfs             = pandas DataFrame or list of two DataFrames
        recording       = name of the recording being plotted
        chan_lab        = label of the channel being plotted
        both            = Bool, whether plotting both low and all frequencies,
                          or (False) just all frequencies
        dpi             = resolution of the produced image
        fig_out_folder  = directory of the produced figure
        verbose         = Bool
        sep             = operating system directory seperator e.g. '/'
    '''
    if verbose:
        print('Plotting mean power figures')
    if both and len(dfs) == 2:
        f, a = plt.subplots(nrows=2, ncols=1, figsize=(10, 10))
        labs = ['All Frequencies', 'Low Frequencies']
        for ind, df in enumerate(dfs):
            mean_freqs = df.apply(np.mean, axis=0)
            a[ind].plot(mean_freqs.index, mean_freqs.values)
            a[ind].set_xlabel('Frequency (Hz)')
            a[ind].set_ylabel('Mean Power Density')
            a[ind].set_title(' '.join([recording, labs[ind], chan_lab]))
    else:
        f, a = plt.subplots(figsize=(10, 10))
        mean_freqs = dfs.apply(np.mean, axis=0)
        a.plot(mean_freqs.index, mean_freqs.values)
        a.set_xlabel('Frequency (Hz)')
        a.set_ylabel('Mean Power Density')
        a.set_title(recording)
    filename = genfirgure_fname(fig_out_folder,
                                fig_type='mean_power',
                                recording=recording,
                                chan_lab=chan_lab,
                                sep=sep)
    plt.tight_layout()
    plt.savefig(fname=filename, dpi=dpi)


def plot_spectrogram(dfs, recording, chan_lab,
                     recording_len, dpi, verbose, both,
                     fig_out_folder, vmin, vmax, sep):
    '''
    Takes a pandas DataFrame and plots and saves a spectrogram
    Parameters:
        dfs             = pandas DataFrame or list of two DataFrames
        recording       = name of the recording being plotted
        chan_lab        = label of the channel being plotted
        recording_len   = Length of the recording. Used to calculate xticks
        both            = Bool, whether plotting both low and all frequencies,
                          or (False) just all frequencies
        dpi             = resolution of the produced image
        fig_out_folder  = directory of the produced figure
        verbose         = Bool
        sep             = operating system directory seperator e.g. '/'
    '''
    if verbose:
        print('Plotting spectrograms')
    x_tick_pos = round(recording_len / 4)
    if both and len(dfs) == 2:
        f, a = plt.subplots(nrows=2, ncols=1, figsize=(10, 10))
        labs = ['All Frequencies', 'Low Frequencies']
        for ind, df in enumerate(dfs):
            sns.heatmap(df.transpose(),
                        vmin=vmin, vmax=vmax, cmap='coolwarm',
                        xticklabels=x_tick_pos, ax=a[ind])
            a[ind].set_ylabel('Frequency\n(Hz)')
            a[ind].set_xticklabels(list(map(lambda num:
                                            str(round(recording_len / 4 / 60 * num,
                                                      -1)),
                                            [0, 1, 2, 3])))
            a[ind].set_xlabel('Time \n(min)')
            a[ind].set_title(labs[ind])
            a[ind].invert_yaxis()
            filename = genfirgure_fname(fig_out_folder,
                                        fig_type='spectrograms',
                                        recording=recording,
                                        chan_lab=chan_lab,
                                        sep=sep)
    else:
        f, a = plt.subplots(figsize=(10, 10))
        sns.heatmap(dfs.transpose(),
                    vmin=vmin, vmax=vmax, cmap='coolwarm',
                    xticklabels=x_tick_pos, ax=a)
        a.set_ylabel('Frequency\n(Hz)')
        a.set_xticklabels(list(map(lambda num:
                                   str(round(recording_len / 4 / 60 * num,
                                             -1)),
                                   [0, 1, 2, 3])))
        a.set_xlabel('Time \n(min)')
        a.set_title(recording)
        a.invert_yaxis()
        filename = genfirgure_fname(fig_out_folder,
                                    fig_type='spectrograms',
                                    recording=recording,
                                    chan_lab=chan_lab,
                                    sep=sep)
    plt.tight_layout()
    plt.savefig(fname=filename, dpi=dpi)


def genfirgure_fname(fig_out_folder, fig_type, recording,
                     chan_lab, sep):
    '''
    Generates an absolute path to a .png figure
    Creates nessessary directories
    Parameters:
        fig_out_folder          = root figure folder
        fig_type                = category of figure
        recording               = name of recording
        chan_lab                = chan label for data
        sep                     = operating system directory seperator e.g. '/'
    '''
    out_dir = sep.join([fig_out_folder, fig_type])
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    out_dir = sep.join([out_dir, recording])
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    return sep.join([out_dir, recording]) + '_' + chan_lab + '.png'

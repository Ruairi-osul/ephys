import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from glob import glob
sns.set()


def load_data(source_folder, recording, sep):
    data_dir = sep.join([source_folder, recording])
    os.chdir(data_dir)
    file_names = glob("*.csv")
    data = [pd.read_csv(file, index_col=0) for file in file_names]
    return data, file_names


def manipulate_df(df):
    log_df = np.log(df)
    log_df.reset_index(inplace=True)
    log_df['time'] = pd.to_timedelta(log_df['time'])
    log_df.set_index('time', inplace=True)
    low_freqs_df = log_df.iloc[:, :80]
    return log_df, low_freqs_df


def plot_mean_power(dfs, recording, chan_lab, both, dpi, fig_out_folder, verbose, sep):
    if verbose:
        print('Plotting mean power figures')
    if both and len(dfs) == 2:
        f, a = plt.subplots(nrows=2, ncols=1, figsize=(10, 10))
    else:
        f, a = plt.subplots(figsize=(10, 10))

    labs = ['All Frequencies', 'Low Frequencies']
    if both and len(dfs) == 2:
        for ind, df in enumerate(dfs):
            mean_freqs = df.apply(np.mean, axis=0)
            a[ind].plot(mean_freqs.index, mean_freqs.values)
            a[ind].set_xlabel('Frequency (Hz)')
            a[ind].set_ylabel('Mean Power Density')
            a[ind].set_title(' '.join([recording, labs[ind], chan_lab]))
    else:
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


def plot_spectrogram(dfs, recording, chan_lab, recording_len, dpi, verbose, both, fig_out_folder, vmin, vmax, sep):
    if verbose:
        print('Plotting spectrograms')
    if both and len(dfs) == 2:
        f, a = plt.subplots(nrows=2, ncols=1, figsize=(10, 10))
    else:
        f, a = plt.subplots(figsize=(10, 10))

    labs = ['All Frequencies', 'Low Frequencies']
    x_tick_pos = round(recording_len / 4)
    if both and len(dfs) == 2:
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
    out_dir = sep.join([fig_out_folder, fig_type])
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    out_dir = sep.join([out_dir, recording])
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    return sep.join([out_dir, recording]) + '_' + chan_lab + '.png'

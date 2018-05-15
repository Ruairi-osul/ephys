import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from glob import glob
sns.set()

pds_folder = 'D:\CIT_WAY\dfs\pds'
recordings_to_plot = ['CIT_WAY_1_2018-05-01_15-59-19_PRE']

fig_out_folder = r'D:\CIT_WAY\figures'


def load_data(source_folder, recording):
    data_dir = '\\'.join([source_folder, recording])
    os.chdir(data_dir)
    file_names = glob("*.csv")
    data = [pd.read_csv(file, index_col=0) for file in file_names]
    return data, file_names


def plot_mean_power(dfs, recording, chan_lab, dpi):
    f, a = plt.subplots(nrows=2, ncols=1, figsize=(10, 10))
    labs = ['All Frequencies', 'Low Frequencies']

    for ind, df in enumerate(dfs):
        mean_freqs = df.apply(np.mean, axis=0)
        a[ind].plot(mean_freqs.index, mean_freqs.values)
        a[ind].set_xlabel('Frequency (Hz)')
        a[ind].set_xlabel('Mean Power Density')
        a[ind].set_title(labs[ind])
    filename = genfirgure_fname(fig_out_folder,
                                fig_type='mean_power',
                                recording=recording,
                                chan_lab=chan_lab)

    plt.savefig(fname=filename, dpi=dpi)


def plot_spectrogram(dfs, recording, chan_lab, recording_len, dpi):

    labs = ['All Frequencies', 'Low Frequencies']

    x_pick_pos = round(recording_len/4)
    f, a = plt.subplots(nrows=2, ncols=1, figsize=(19, 9))
    for ind, df in enumerate(dfs):

        sns.heatmap(df.transpose(),
                    vmin=0, vmax=8, cmap='coolwarm',
                    xticklabels=x_pick_pos, ax=a[ind])
        a[ind].set_ylabel('Frequency\n(Hz)')
        a[ind].set_xticklabels(list(map(lambda num:
                                        str(round(recording_len/4/60 * num, -1)),
                                        [0, 1, 2, 3])))
        a[ind].set_xlabel('Time \n(min)')
        a[ind].set_title(labs[ind])
        a[ind].invert_yaxis()
        filename = genfirgure_fname(fig_out_folder,
                                    fig_type='spectrograms',
                                    recording=recording,
                                    chan_lab=chan_lab)
    plt.savefig(fname=filename, dpi=dpi)


def genfirgure_fname(fig_out_folder, fig_type, recording, chan_lab):
    out_dir = '\\'.join([fig_out_folder, fig_type])
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    out_dir = '\\'.join([out_dir, fig_type])
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    return '\\'.join([out_dir, recording]) + '_' + chan_lab + '.png'


def main():
    for recording in recordings_to_plot:
        df_list, file_names = load_data(source_folder=pds_folder,
                                        recording=recording)
        for ind, df in enumerate(df_list):
            chan_label = file_names[ind].split('.')[0][-4:]
            log_df = np.log(df)
            log_df.reset_index(inplace=True)
            log_df['time'] = pd.to_timedelta(log_df['time'])
            log_df.set_index('time', inplace=True)
            recording_len = log_df.index.max().seconds

            low_freqs_df = log_df.iloc[:, :20]
            print(low_freqs_df.info())
            plot_mean_power(dfs=[log_df, low_freqs_df],
                            recording=recording,
                            chan_lab=chan_label, dpi=300)
            plot_spectrogram(dfs=[log_df, low_freqs_df],
                             recording=recording,
                             chan_lab=chan_label,
                             recording_len=recording_len,
                             dpi=300)


if __name__ == '__main__':
    main()

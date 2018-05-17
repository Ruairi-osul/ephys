from spectrograms.funcs import *
import matplotlib.pyplot as plt

def main(ops):
    for recording in ops.recordings_to_plot:
        df_list, file_names = load_data(source_folder=ops.pds_folder,
                                        recording=recording,
                                        sep=ops.sep)
        for ind, df in enumerate(df_list):
            chan_label = file_names[ind].split('.')[0][-4:]
            all_freqs_df, low_freqs_df = manipulate_df(df)
            recording_len = all_freqs_df.index.max().seconds
            if ops.which == 'all_freqs':
                plot_mean_power(dfs=all_freqs_df,
                                recording=recording,
                                chan_lab=chan_label,
                                dpi=ops.dpi,
                                fig_out_folder=ops.fig_out_folder,
                                verbose=ops.verbose,
                                sep=ops.sep,
                                both=False)
                plot_spectrogram(dfs=all_freqs_df,
                                 recording=recording,
                                 recording_len=recording_len,
                                 chan_lab=chan_label,
                                 dpi=ops.dpi,
                                 fig_out_folder=ops.fig_out_folder,
                                 verbose=ops.verbose,
                                 vmin=ops.vmin,
                                 vmax=ops.vmax,
                                 sep=ops.sep,
                                 both=False)
            elif ops.which == 'low_freqs':
                plot_mean_power(dfs=low_freqs_df,
                                recording=recording,
                                chan_lab=chan_label,
                                dpi=ops.dpi,
                                fig_out_folder=ops.fig_out_folder,
                                verbose=ops.verbose,
                                sep=ops.sep,
                                both=False)
                plot_spectrogram(dfs=low_freqs_df,
                                 recording=recording,
                                 recording_len=recording_len,
                                 chan_lab=chan_label,
                                 dpi=ops.dpi,
                                 fig_out_folder=ops.fig_out_folder,
                                 verbose=ops.verbose,
                                 vmin=ops.vmin,
                                 vmax=ops.vmax,
                                 sep=ops.sep,
                                 both=False)
            elif ops.which == 'both':
                plot_mean_power(dfs=[all_freqs_df, low_freqs_df],
                                recording=recording,
                                chan_lab=chan_label,
                                dpi=ops.dpi,
                                fig_out_folder=ops.fig_out_folder,
                                verbose=ops.verbose,
                                sep=ops.sep,
                                both=True)
                plot_spectrogram(dfs=[all_freqs_df, low_freqs_df],
                                 recording=recording,
                                 recording_len=recording_len,
                                 chan_lab=chan_label,
                                 dpi=ops.dpi,
                                 fig_out_folder=ops.fig_out_folder,
                                 verbose=ops.verbose,
                                 vmin=ops.vmin,
                                 vmax=ops.vmax,
                                 sep=ops.sep,
                                 both=True)
            else:
                raise ValueError('Incorrect ops.which parameter\nEnter "all_freqs", "low_freqs" or "both"')
            plt.clf()

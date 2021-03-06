from extract_waveforms.funcs import *


def main(ops):
    df_list_2 = []
    for recording in ops.recordings_to_analyse:
        spike_clusters, spike_times, cluster_groups = load_kilosort_arrays(recording=recording,
                                                                           kilosort_folder=ops.kilosort_folder, verbose=ops.verbose)
        raw_data = load_raw_data(recording=recording,
                                 kilosort_folder=ops.kilosort_folder,
                                 num_channels=ops.num_channels)
        good_cluster_numbers = get_good_cluster_numbers(cluster_groups)
        good_spikes_df = gen_good_spikes_df(spike_times=spike_times,
                                            spike_clusters=spike_clusters,
                                            good_cluster_numbers=good_cluster_numbers)
        df_list = []
        for cluster in good_cluster_numbers:
            spiketimes_series = gen_spiketimes_series(good_spikes_df=good_spikes_df,
                                                      cluster=cluster,
                                                      num_spikes=ops.num_spikes,
                                                      last_spikes=ops.last_spikes)
            waveform_per_chan = extract_waveforms(num_spikes=ops.num_spikes,
                                                  num_samples=ops.num_samples,
                                                  num_channels=ops.num_channels,
                                                  spike_times=spiketimes_series,
                                                  raw_data=raw_data)
            one_channel, chan = choose_channel(df=waveform_per_chan,
                                               method=ops.spike_selection_method,
                                               broken_chans=ops.borken_channels)
            df = gen_peak_finding_df(chan_df=one_channel)
            presence_of_initial_peak = (df['y_values'].iloc[:int(ops.num_samples / 2)] > 20).any()
            if presence_of_initial_peak:
                cluster_df = up_down_up(df=df,
                                        cluster=cluster,
                                        recording=recording,
                                        num_samples=ops.num_samples,
                                        thresh=ops.thresh_udu,
                                        fig_folder=ops.fig_folder,
                                        fs=ops.fs)
            else:
                cluster_df = down_up(df=df,
                                     num_samples=ops.num_samples,
                                     recording=recording,
                                     cluster=cluster,
                                     thresh=ops.thesh_du,
                                     fig_folder=ops.fig_folder,
                                     chan=chan,
                                     fs=ops.fs)
            df_list.append(cluster_df)
            plot_waveform(all_chans_df=waveform_per_chan,
                          one_chan_df=one_channel,
                          recording=recording,
                          method=ops.spike_selection_method,
                          chan=chan,
                          cluster=cluster,
                          fig_folder=ops.fig_folder)
        df_merged = merge_dfs(df_list, broadcast=True, recording=recording)
        df_list_2.append(df_merged)
        print(len(df_list_2))
    final_df = merge_dfs(df_list_2, broadcast=False)
    final_df.to_csv(os.path.join(ops.temp_folder, 'waveforms.csv'), index=False)

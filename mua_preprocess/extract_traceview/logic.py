from extract_traceview.funcs import *


def main(ops):

    data = load_raw_data(kilosort_folder=ops.kilosort_folder,
                         recording=ops.recording,
                         num_channels=ops.num_channels)
    spike_clusters, spike_times, cluster_groups = load_data(recording=ops.recording,
                                                            kilosort_folder=ops.kilosort_folder,
                                                            verbose=ops.verbose)
    df, cluster_to_plot = choose_cluster_to_plot(cluster_groups=cluster_groups,
                                                 spike_clusters=spike_clusters,
                                                 spike_times=spike_times,
                                                 chosen_cluster=ops.chosen_cluster)
    if ops.verbose:
        print('Cluster ID: ' + str(cluster_to_plot))

    extracted_spikes = df[df['cluster'] == cluster_to_plot]['spike_times']
    Spike_chosen = choosing_spike(extracted_spikes=extracted_spikes,
                                  time_chosen=ops.time_chosen)
    plt.figure(figsize=(24.5, 10))
    chosen_channel = choose_channel(Spike_chosen=Spike_chosen,
                                    extracted_spikes=extracted_spikes,
                                    time_span=ops.time_span,
                                    data=data,
                                    broken_chans=ops.broken_chans,
                                    num_spikes_for_averaging=ops.num_spikes_for_averaging)
    if ops.verbose:
        print('Plotting Channel: ' + str(chosen_channel))

    df_trace = extract_trace(Spike_chosen=Spike_chosen,
                             extracted_spikes=extracted_spikes,
                             time_span=ops.time_span,
                             data=data,
                             chosen_channel=chosen_channel)

    plt.plot(df_trace['time'], df_trace['Value'], color='gray', alpha=0.5)

    highlighted_spike_list = extract_highlighted_spikes(time_span=ops.time_span,
                                                        extracted_spikes=extracted_spikes,
                                                        Spike_chosen=Spike_chosen)

    for spike in highlighted_spike_list:  # loop over each spike in original trace. Plot in color
        df_highlight = spike_highlight(spike=spike,
                                       extracted_spikes=extracted_spikes,
                                       data=data,
                                       chosen_channel=chosen_channel)
        plt.plot(df_highlight['time'], df_highlight['Value'], color=ops.color, linewidth=2)

    plot_final_data(kilosort_folder=ops.kilosort_folder,
                    recording=ops.recording,
                    chosen_channel=chosen_channel,
                    chosen_cluster=ops.chosen_cluster, highlighted_spike_list=highlighted_spike_list, time_chosen=ops.time_chosen)

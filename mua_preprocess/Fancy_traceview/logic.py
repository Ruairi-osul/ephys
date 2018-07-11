from Fancy_traceview.funcs import *


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
	extracted_spikes = df[df['cluster'] == cluster_to_plot]['spike_times']

	time_chosen=(ops.time_span_chosen[0]+ops.time_span_chosen[1])/2*60

	time_span=(ops.time_span_chosen[1]-ops.time_span_chosen[0])*60

	Spike_chosen = choosing_spike(extracted_spikes=extracted_spikes,
	                                  time_chosen=time_chosen)

	chosen_channel = choose_channel(Spike_chosen=Spike_chosen,
	                                    extracted_spikes=extracted_spikes,
	                                    time_span=time_span,
	                                    data=data,
	                                    broken_chans=ops.broken_chans,
	                                    num_spikes_for_averaging=ops.num_spikes_for_averaging)

	df_trace = extract_trace(Spike_chosen=Spike_chosen,
	                             extracted_spikes=extracted_spikes,
	                             time_span=time_span,
	                             data=data,
	                             chosen_channel=chosen_channel)

	plotly_plot(time_span=time_span, time_chosen = time_chosen, extracted_spikes=extracted_spikes, Spike_chosen=Spike_chosen, df_trace=df_trace, data=data, chosen_channel=chosen_channel)
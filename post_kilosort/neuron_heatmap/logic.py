from neuron_heatmap.funcs import *
'''
Logic for neuron heatmap
Loads data
Manipulates such that is in a good shape for time series analysis
Caculates baseline statistics
Creates a time series pandas DataFrame over all the entire time period

'''

def main(ops):
    for recording in ops.recordings_to_analyse:
        df = load_data(recording=recording,
                       data_dir=ops.data_dir,
                       sep=ops.sep,
                       verbose=ops.verbose)
        df = manipulate_df(df)
        baseline_means, baseline_stds, baseline_sorted = calculate_condition_statistics(df=df,
                                                                                        condition=ops.condition,
                                                                                        resample_period=ops.resample_period)
        df = create_ts(df=df,
                       rolling=ops.rolling,
                       resample_period=ops.resample_period)
        df = normalise(df, method=ops.method, condition_means=baseline_means,
                       condition_stds=baseline_stds, condition_sorted=baseline_sorted,
                       verbose=ops.verbose)
        plot_heat(df=df, dpi=ops.dpi, vmin=ops.vmin, vmax=ops.vmax,
                  method=ops.method, fig_dir=ops.fig_dir, sep=ops.sep,
                  recording=recording, verbose=ops.verbose)

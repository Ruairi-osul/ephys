from neuron_heatmap.funcs import *


def main(ops):
    for recording in ops.recordings_to_analyse:
        df = load_data(recording=recording,
                       dara_dir=ops.data_dir)
        df = manipulate_df(df)
        baseline_means, baseline_stds, baseline_sorted = calculate_condition_statistics(df=df,
                                                                                        condition=condition)
        df = create_ts(df=df,
                       rolling=ops.rolling)
        df = normalise(df, method=ops.method)
        gen_fig_path(df=df, dpi=ops.dpi, vmin=ops.vmin, vmax=ops.vmax,
                     method=ops.method)

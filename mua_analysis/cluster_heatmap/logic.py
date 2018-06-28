from cluster_heatmap.funcs import *


def main(ops):
    df_all_data = load_data(path=ops.csv_dir,
                            csv_file_name=ops.csv_file_name)

    for recording in df_all_data.loc[:, 'recording'].unique():
        df_rec = df_all_data[df_all_data['recording'] == recording].copy()

        df_rec = manipulate_df(df=df_rec)
        base_means, base_stds, base_sorted = get_baseline_stats(df=df_rec,
                                                                condition_label='Baseline',
                                                                resample_period=ops.resample_period)
        df_rec = create_ts(df=df_rec,
                           resample_period=ops.resample_period,
                           rolling_period=ops.rolling_periods)

        df_rec = normalise(df=df_rec,
                           method=ops.normalisation_method,
                           condition_means=base_means,
                           condition_stds=base_stds,
                           condition_sorted=base_sorted)
        plot_heatmap_separate_categories(ts_df=df_rec,
                                         df_all_neurons=df_all_data,
                                         recording=recording,
                                         category_column=ops.category_column,
                                         vmin=ops.vmin, vmax=ops.vmax,
                                         normalise_method=ops.normalisation_method,
                                         out_folder=ops.out_folder)

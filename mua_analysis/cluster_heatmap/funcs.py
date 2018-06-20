import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
sns.set()


def load_data(path, csv_file_name):
    if not csv_file_name.endswith('.csv'):
        csv_file_name = ''.join([csv_file_name, '.csv'])
    file_path = os.path.join(path, csv_file_name)
    return pd.read_csv(file_path)


def manipulate_df(df):
    df['spike'] = 1
    df['time'] = pd.to_timedelta(df['time'], unit='s')
    return df


def create_ts(df, rolling_period, resample_period=1):
    df = df.pivot_table(index='time',
                        columns='spike_cluster',
                        values='spike',
                        aggfunc='count')
    df = df.resample('s').count()
    if rolling_period:
        df = df.rolling(rolling_period).mean()
    return df


def get_baseline_stats(df, condition_label, resample_period):
    df = df[df['condition'] == condition_label]
    df = create_ts(df=df,
                   rolling_period=False,
                   resample_period=resample_period)
    condition_means = df.transpose().mean(axis=1)
    condition_stds = df.transpose().std(axis=1)
    condition_sorted = condition_means.sort_values()
    return condition_means, condition_stds, condition_sorted


def normalise(df, method, condition_means, condition_stds, condition_sorted):
    if method == 'zscore':
        def f(col):
            return (col.subtract(condition_means)).divide(condition_stds)
    elif method == 'percent':
        def f(col):
            return col.divide(condition_means) * 100
    elif not method:
        def f(col):
            print('Note: No Normalisation Method Provided')
            return col
    df = df.transpose().apply(f)
    return df.reindex(condition_sorted.index)


def select_neruon_cat(ts_df, df_all_neurons, recording, category_column, category):
    clusters = df_all_neurons[(df_all_neurons['recording'] == recording) & (df_all_neurons[category_column] == category)]['spike_cluster'].unique()
    return ts_df[ts_df.index.isin(clusters)]


def plot_heatmap_separate_categories(ts_df, df_all_neurons, recording, category_column, vmin, vmax, normalise_method, out_folder):

    num_categories = len(df_all_neurons['category'].unique())
    f, a = plt.subplots(nrows=num_categories, ncols=1, figsize=(19, 25))

    for index, category in enumerate(df_all_neurons[category_column].unique()):
        df_cat = select_neruon_cat(ts_df=ts_df,
                                   df_all_neurons=df_all_neurons,
                                   recording=recording,
                                   category_column=category_column,
                                   category=category)

        recording_len = df_cat.transpose().index.max().seconds
        x_tick_pos = round(recording_len / 4)

        sns.heatmap(data=df_cat,
                    cmap='coolwarm',
                    vmin=vmin,
                    vmax=vmax,
                    ax=a.flat[index],
                    xticklabels=x_tick_pos,
                    cbar_kws={'label': f'{normalise_method} Baseline mean'})

        a.flat[index].set_xticklabels(list(map(lambda num:
                                               str(round(recording_len / 4 / 60 * num, -1)),
                                               [0, 1, 2, 3])))
        a.flat[index].set_title(category)
    plt.suptitle(recording, fontsize=15)
    plt.tight_layout()
    plt.savefig(gen_fig_path(out_folder, recording))


def gen_fig_path(out_folder, recording):
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)
    return ''.join([os.path.join(out_folder, recording), '.png'])

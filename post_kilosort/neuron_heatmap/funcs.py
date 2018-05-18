import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


def load_data(recording, data_dir, sep):
    file = sep.join([data_dir, recording]) + '.csv'
    return pd.read_csv(file, index_col=1)


def manipulate_df(df):
    df['spike'] = 1
    df['time'] = pd.to_timedelta(df['time'], unit='s')
    return df


def create_ts(df, rolling):
    df = df.pivot_table(index='time',
                        columns='spike_cluster',
                        values='spike',
                        aggfunc='count')
    if rolling:
        df = df.rolling(rolling).mean()
    return df


def calculate_condition_statistics(df, condition):
    df = df.loc[df['condition'] == condition]
    df = create_ts(df=df,
                   rolling=False)
    condition_means = df.transpose().mean(axis=1)
    condition_stds = df.transpose().std(axis=1)
    condition_sorted = df.sort_values()
    return condition_means, condition_stds, condition_sorted


def normalise(df, method):
    global baseline_means
    global baseline_stds
    global baseline_sorted
    if method == 'zscore':
        def f(col):
            return (col.subtract(baseline_means)).divide(baseline_stds)
    elif method == 'percent':
        def f(col):
            return col.divide(baseline_means) * 100
    elif not method:
        def f(col):
            return col
    df = df.transpose().apply(f)
    return df.reindex(baseline_sorted)


def gen_fig_path(fig_dir, recording, sep):
    return sep.join([fig_dir, recording]) + '.png'


def plot_heat(df, dpi, vmin, vmax, method, recording, fig_dir, sep):
    f, a = plt.subplots(19, 9)
    recording_len = df.transpose().index.max().seconds
    x_tick_pos = round(recording_len / 4)
    sns.heatmap(data=df, cmap='coolwarm', vmin=vmin,
                vmax=vmax, xticklabels=x_tick_pos)
    a.set_ylabel('Neuron Number\nSorting by baseline firing rate in ascending order (slowest on top)')
    a.set_xlabel('Time (min)')
    a.set_title(f'Firing Rate Normalised by {method}')
    a.set_xticklabels(list(map(lambda num:
                               str(round(recording_len / 4 / 60 * num, -1)),
                               [0, 1, 2, 3])))
    plt.savefig(gen_fig_path(fig_dir=fig_dir, recording=recording,
                             sep=sep), dpi=600)

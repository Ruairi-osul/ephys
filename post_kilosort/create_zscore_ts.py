import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

path_to_data = r'C:\Users\Rory\raw_data\SERT_DREADD\spikes_df'
recordings_to_analyse = ['2018-04-10_391b',
                         '2018-04-11_371a',
                         '2018-04-12_371b',
                         '2018-04-17_401c']

for recording in recordings_to_analyse:
    file = '\\'.join([path_to_data, recording]) + '.csv'
    df = pd.read_csv(file, index_col=0)
    df['spike'] = 1
    df['time'] = pd.to_timedelta(df['time'], unit='s')

    baseline = df.loc[df['condition'] == 'Baseline']
    base_ts = df.pivot_table(index='time',
                             columns='spike_cluster',
                             values='spike',
                             aggfunc='count')
    base_sec = base_ts.resample('s').count()
    baseline_means = base_sec.transpose().mean(axis=1)
    baseline_stds = base_sec.transpose().std(axis=1)
    baseline_sorted = baseline_means.sort_values()

    df_ts = df.pivot_table(index='time',
                           columns='spike_cluster',
                           values='spike',
                           aggfunc='count')

    df_ts_sec = df_ts.resample('s').count()
    fr_rolling = df_ts_sec.rolling(60*2).mean()
    # groupby spike_cluster

    x = fr_rolling.transpose().apply(lambda col:
                                     (col.subtract(baseline_means)
                                      ).divide(baseline_stds))
    x = x.reindex(baseline_sorted.index)
    recording_len = x.transpose().index.max().seconds
    x_pick_pos = round(recording_len/4)
    f, a = plt.subplots(figsize=(19, 9))
    sns.heatmap(x, ax=a, cmap='coolwarm', vmin=-3, vmax=3,
                xticklabels=x_pick_pos)
    a.set_ylabel('Neuron Number\nSorting by baseline firing rate in ascending order (slowest on top)')
    a.set_title('Firing Rate Normalised to Neuron Mean During Baseline\nTwo minute rolling window')
    a.set_xticklabels(list(map(lambda num:
                               str(round(recording_len/4/60 * num, -1)),
                               [0, 1, 2, 3])))
    a.set_xlabel('Time (min)\nCNO administration at 60 minutes')
    plt.savefig(r'C:\Users\Rory\raw_data\SERT_DREADD\figures\heat\{}.png'.format(
        recording), dpi=600)

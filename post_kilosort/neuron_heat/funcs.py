import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


def load_data(recording, csv_dir, sep, chans):
    file_name = sep.join([csv_dir, recording]) + 'csv'
    df = pd.read_csv(file_name, index_col=0)
    df['time'] = pd.to_timedelta(df['time'], unit='s')
    df['spike'] = 1
    return df


def create_cluster_ts(df):
    df = df.pivot_table(index='time', colums='spike_cluster',
                        values='spike',
                        aggfunc='count')
    df = df.resample('s').count()
    return df


def calculate_condition_statistics(df, condition):
    df = df.loc[df['condition'] == condition]
    create_cluster_ts(df)

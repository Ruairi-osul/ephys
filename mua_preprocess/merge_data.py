import pandas as pd
from glob import glob
import os

path_to_temp = r'C:\Users\Rory\raw_data\CIT_WAY\temp'
out_folder = r'C:\Users\Rory\raw_data\CIT_WAY\csvs'

for file in glob(os.path.join(path_to_temp, '*.csv')):
    df = pd.read_csv(file)
    if 'cluster' in df.columns:
        right = df
    elif 'spike_cluster':
        left = df

df = pd.merge(left=left, right=right, left_on=['spike_cluster', 'recording'], right_on=['cluster', 'recording'])
df.drop('cluster', axis=1, inplace=True)

path_out = os.path.join(out_folder, 'neuron_stats.csv')
df.to_csv(path_out, index=Fal)

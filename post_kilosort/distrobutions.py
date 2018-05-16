import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


path_to_data = r'C:\Users\Rory\raw_data\SERT_DREADD\neuron_characteristics'
fig_folder = r'C:\Users\Rory\raw_data\SERT_DREADD\figures'
recordings_to_analyse = ['2018-04-10_391b',
                         '2018-04-11_371a',
                         '2018-04-12_371b',
                         '2018-04-17_401c']
operating_system = 'win'
verbose = True

sep = '\\' if operating_system == 'win' else '/'


def return_path(path_to_data, recording):
    return sep.join([path_to_data, recording]) + '.csv'


def fig_path(fig_type, fig_folder, recording):
    if not os.path.exists(sep.join([fig_folder, fig_type])):
        os.mkdir(sep.join([fig_folder, fig_type]))
    return sep.join([fig_folder, fig_type, recording]) + '.png'


for recording in recordings_to_analyse:
    file = return_path(path_to_data, recording)
    df = pd.read_csv(file)

    total_neurons = df['cluster'].count()
    by_neuron_cat = df.groupby('neuron_category')['rate'].apply(
        lambda ser: ser.count()/total_neurons)
    by_neuron_cat = by_neuron_cat.reindex(
        ['slow irregular', 'slow regular', 'fast regular', 'fast irregular'])

    f, a = plt.subplots(figsize=(8, 8))
    by_neuron_cat.plot(kind='bar', ax=a,
                       title='Distrobution of Firing Properties of Recorded Neurons: {}'.format(recording[-4:]))
    a.set_ylabel('Percentage total neurons (n={})'.format(total_neurons))
    print('Saving neuron distrobution figure:\t{}'.format(recording))
    plt.savefig(fig_path(fig_type='neuron_cat_distrobution',
                         fig_folder=fig_folder,
                         recording=recording),
                dpi=500)

    print('Saving neuron distrobution figure:\t{}'.format(recording))
    sns.jointplot(data=df, x='cv_isi', y='rate', stat_func=None,
                  size=8)
    plt.title('Scatter plot of Rate (Hz) versus CV ISI: {}'.format(recording[-4:]))
    plt.savefig(fig_path(fig_type='rate_reg_distscatter',
                         fig_folder=fig_folder,
                         recording=recording), dpi=500)

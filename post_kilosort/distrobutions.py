import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


recordings_to_analyse = ['401a_2018-04-18_16-34-20_NO_CNO']

path_to_data = r'C:\Users\Rory\raw_data\SERT_DREADD\neuron_characteristics'
fig_folder = r'C:\Users\Rory\raw_data\SERT_DREADD\figures'
verbose = True


def return_path(path_to_data, recording):
    recording_folder = '\\'.join([path_to_data, recording])
    return '\\'.join([recording_folder, recording]) + '.csv'


def fig_path(fig_type, fig_folder, recording):
    if not os.path.exists('\\'.join([fig_folder, fig_type])):
        os.mkdir('\\'.join([fig_folder, fig_type]))
    return '\\'.join([fig_folder, fig_type, recording]) + '.png'


df_list = []
for recording in recordings_to_analyse:
    file = return_path(path_to_data, recording)
    df = pd.read_csv(file)
    df_list.append(df)
    if verbose:
        print('Saving neuron distrobution figure:\t{}'.format(recording))

    total_neurons = df['cluster'].count()
    by_neuron_cat = df.groupby('neuron_category')['rate'].apply(
        lambda ser: ser.count()/total_neurons)
    by_neuron_cat = by_neuron_cat.reindex(['slow irregular', 'slow regular',
                                           'fast irregular',
                                           'fast regular'])
    f, a = plt.subplots(figsize=(8, 8))
    by_neuron_cat.plot(kind='bar',
                       ax=a,
                       title='Distrobution of Neuron Firing Properties')
    a.set_ylabel('Percentage total neurons (n={})'.format(total_neurons))
    plt.savefig(fig_path(fig_type='neuron_cat_distrobution',
                         fig_folder=fig_folder,
                         recording=recording),
                dpi=500)

    print('Saving regularity rate figure:\t{}'.format(recording))
    sns.jointplot(data=df, x='cv_isi', y='rate', stat_func=None,
                  size=8)
    plt.savefig(fig_path(fig_type='rate_regularity_scatter',
                         fig_folder=fig_folder,
                         recording=recording), dpi=500)

print('Saving joint scatter plot figure')
df_joint = pd.concat(df_list)
sns.lmplot(data=df_joint, x='cv_isi', y='rate',
           hue='condition',
           size=8,
           fit_reg=False)
plt.title('Joint Scatter plot')
plt.savefig(fig_path(fig_type='joint_scatter',
                     fig_folder=fig_folder,
                     recording=recording), dpi=500)

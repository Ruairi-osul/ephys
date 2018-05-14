import pandas as pd


def return_path(path_to_data, recording):
    recording_folder = '\\'.join([path_to_data, recording])
    return '\\'.join([recording_folder, recording]) + '.csv'


recordings_to_analyse = ['401a_2018-04-18_16-34-20_NO_CNO',
                         '401a_2018-04-18_17-40-36_CNO']

path_to_data = r'C:\Users\Rory\raw_data\SERT_DREADD\neuron_characteristics'
path_to_amps = r'C:\Users\Rory\raw_data\SERT_DREADD\cluster_channels'

for recording in recordings_to_analyse:
    neuron_char_path = return_path(path_to_data, recording)
    df_chars = pd.read_csv(neuron_char_path, index_col=0)

    file = return_path(path_to_amps, recording)
    df_chans = pd.read_csv(file, index_col=0)
    df_chans = df_chans.drop('depth', axis=1)

    df = pd.merge(left=df_chars,
                  right=df_chans,
                  left_index=True, right_index=True)
    df.to_csv(neuron_char_path)

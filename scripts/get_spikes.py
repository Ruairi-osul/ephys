import argparse
from preprocess import load_kilosort_arrays, get_good_cluster_numbers, gen_df
import json
import os
import pandas as pd


def _get_options():
    parser = argparse.ArgumentParser(
        description='''Extract spikes from kilosort files
        ''')

    parser.add_argument('-r', '--recording',
                        required=False,
                        help='''path to directory of recording to analyse

                        ''')
    parser.add_argument('-c', '--config',
                        required=False,
                        help='''path to config file for the experiment

                        ''')
    return parser.parse_args()


def _get_config_options(config_path):
    with open(config_path) as file:
        return json.loads(file.read())


def get_tables(processed_data_dir):
    '''returns: mice, recordings, neurons'''
    dirs = list(map(lambda x: os.path.join(processed_data_dir, x),
                    ['mice.xlsx', 'recordings.csv', 'neurons.csv', 'spike_times.csv']))
    out = []
    try:
        for i, d in enumerate(dirs):
            if i == 0 and '.xlsx' in d:
                out.append(pd.read_excel(d, sheet_name='Sheet1'))
            elif i in [1, 2] and '.csv' in d:
                out.append(pd.read_csv(d))
            else:
                raise IOError("Error loading {}".format(d))
    except IOError as e:
        print('Cannot open tables')
        raise e
    return out


def update_neurons_table(neurons_table, new_data, recording_id):
    to_add = new_data.drop('spike_times', axis=1).drop_duplicates()

    if len(neurons_table) == 0:
        out = to_add
        out.index = pd.RangeIndex(0, len(to_add))
    else:
        neurons_table.set_index('neuron_id', inplace=True)
        maxidx = neurons_table.index[-1]
        to_add.index = pd.RangeIndex(maxidx + 1, maxidx + 1 + len(to_add))
        out = pd.concat([neurons_table, to_add], sort=False)

    out.index.name = 'neuron_id'
    return out


def update_spike_times(spike_times, new_data, neurons):
    pass


def _get_recording_id(recording_dir, recordings_table):
    if os.path.isabs(recording_dir):
        recording_dir = os.path.basename(recording_dir)
    matches = recordings_table.loc[recordings_table['dat_filename']
                                   == recording_dir]['recording_id'].values
    try:
        assert len(matches) == 1
    except AssertionError:
        raise ValueError("Error finding recording id. Mutiple marches found")
    return matches[0]


def main(recording_dir, processed_data_dir, sampling_rate=30000):
    spike_clusters, spike_times, cluster_groups = load_kilosort_arrays(
        recording_dir)
    good_cluster_nums = get_good_cluster_numbers(cluster_groups)
    new_data = gen_df(spike_clusters, spike_times, good_cluster_nums)

    mice, recordings, neurons, spike_times = get_tables(processed_data_dir)
    recording_id = _get_recording_id(recording_dir, recordings)
    new_data['recording_id'] = recording_id

    neurons = update_neurons_table(neurons, new_data)
    spike_times = update_spike_times(spike_times, new_data)


if __name__ == '__main__':

    def _update_paths(ops):
        if ',' in ops['recording']:
            recordings = ops['recording'].split(',')
        else:
            recordings = [ops['recording']]
        if not os.path.isabs(recordings[0]):
            recordings = list(map(
                lambda x: os.path.join(
                    ops["concatenated_datfile_directory"], x),
                recordings))
        return recordings

    ops = vars(_get_options())
    ops.update(_get_config_options(ops['config']))
    recordings = _update_paths(ops)
    for recording in recordings:
        main(recording_dir=recording,
             processed_data_dir=ops['processed_data_dir'])

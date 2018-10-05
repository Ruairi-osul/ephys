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
        out = json.loads(file.read())
    return out


def get_tables(processed_data_dir, tables=['mice.csv', 'recordings.csv', 'neurons.csv', 'spike_times.csv']):
    '''returns: mice, recordings, neurons, spike_times'''

    if not isinstance(tables, list) and not isinstance(tables, tuple):
        tables = [tables]

    dirs = list(map(lambda x: os.path.join(processed_data_dir, x),
                    tables))
    out = {}
    try:
        for i, d in enumerate(dirs):
            root, ext = os.path.splitext(os.path.basename(d))
            if ext == '.xlsx':
                out[root] = pd.read_excel(
                    d, sheet_name='Sheet1', index_col=None)
            elif ext == '.csv':
                out[root] = pd.read_csv(d, index_col=None)
            else:
                raise ValueError(
                    "Table file extention incorrect. Expected /'.csv/' or /'.xlsx/'. \nReceived: {}".format(ext))
    except (IOError, ValueError):
        print('Cannot open tables')
        raise

    return out


def update_neurons_table(neurons_table, new_data):
    to_add = new_data.drop('spike_times', axis=1).drop_duplicates()

    if len(neurons_table) == 0:
        out = to_add
        out.index = pd.RangeIndex(0, len(to_add))
    else:
        neurons_table.set_index('neuron_id', inplace=True)
        maxidx = neurons_table.index[-1]
        to_add.index = pd.RangeIndex(maxidx + 1, maxidx + 1 + len(to_add))
        out = pd.concat([neurons_table, to_add], sort=False).drop_duplicates()
    out.index.name = 'neuron_id'
    return out.reset_index()


def update_spike_times(spike_times, neurons, new_data):
    to_add = pd.merge(left=neurons, right=new_data,
                      on=['recording_id', 'cluster_id']).drop(['cluster_id', 'recording_id'], axis=1)
    out = pd.concat([spike_times, to_add], sort=False).drop_duplicates()
    return out


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


def get_new_data(recording_dir):
    spike_clusters, spike_times, cluster_groups = load_kilosort_arrays(
        recording_dir)
    good_cluster_nums = get_good_cluster_numbers(cluster_groups)
    return gen_df(spike_clusters, spike_times, good_cluster_nums)


def _check_table_data_quality(tables):
    try:
        assert not set(tables['spike_times'].neuron_id.values).difference(
            set(tables['neurons'].neuron_id.values))
    except AssertionError:
        print('''Bad data in Tables. Number of neuron_ids
            in neurons table and spike_time table not equal.''')
        raise


def save_tables(processed_data_dir, tables):
    if not isinstance(tables, dict):
        raise ValueError('''Incorrect type passed to save_tables function.
            Expected a dict. Received: {}'''.format(type(tables)))

    for table_name, df in tables.items():
        path = os.path.join(processed_data_dir, table_name) + '.csv'
        df.to_csv(path, index=False)


def main(recording_dir, processed_data_dir, sampling_rate=30000):

    tables = get_tables(processed_data_dir)
    try:
        _check_table_data_quality(tables)
    except AssertionError:
        print('Data quality bad at input stage')
        raise

    new_data = get_new_data(recording_dir)
    recording_id = _get_recording_id(recording_dir, tables['recordings'])
    new_data['recording_id'] = recording_id

    tables['neurons'] = update_neurons_table(tables['neurons'], new_data)
    tables['spike_times'] = update_spike_times(
        tables['spike_times'], tables['neurons'], new_data)

    try:
        _check_table_data_quality(tables)
    except AssertionError:
        print('Data quality bad at output stage')
        raise
    save_tables(processed_data_dir, tables)


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

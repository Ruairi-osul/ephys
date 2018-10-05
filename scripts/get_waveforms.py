import argparse
import os
import pandas as pd
from functools import partial
from preprocess import (load_kilosort_arrays, get_good_cluster_numbers,
                        get_waveforms)


def _get_options():
    parser = argparse.ArgumentParser(
        description='''Extract waveforms from .dat file given spiketimes

        ''')

    parser.add_argument('-r', '--recording_ids', type=int, required=True,
                        help='''recording_ids of recordings to extract''')
    parser.add_argument('-d', '--db_dir', required=True,
                        help='''path to parent dir of db files
                        ''')
    parser.add_argument('-c', '--raw_data_dir', required=True,
                        help='''path to parent dir of db files
                        ''')
    return parser.parse_args()


def get_tables(processed_data_dir, tables=['mice.csv', 'recordings.csv', 'neurons.csv', 'spike_times.csv', 'waveforms.csv']):
    '''returns: mice, recordings, neurons, spike_times'''

    if not isinstance(tables, list) and not isinstance(tables, tuple):
        tables = [tables]

    dirs = list(map(lambda x: os.path.join(processed_data_dir, x),
                    tables))
    out = {}
    try:
        for d in dirs:
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


def _check_table_data_quality(tables):
    try:
        assert not set(tables['spike_times'].neuron_id.values).difference(
            set(tables['neurons'].neuron_id.values))
    except AssertionError:
        print('''Bad data in Tables. Number of neuron_ids
            in neurons table and spike_time table not equal.''')
        raise


def update_waveforms(waveforms_table, new_data):
    if len(waveforms_table) == 0:
        waveforms_table = new_data
    else:
        waveforms_table.set_index('neuron_id', inplace=True)
        new_data.set_index('neuron_id', inplace=True)
        waveforms_table.append(new_data, sort=False)
        waveforms_table.drop_duplicates(inplace=True)
        waveforms_table.reset_index(inplace=True)
    try:
        assert waveforms_table.neuron_id.value_counts().max() == 1
    except AssertionError:
        raise IndexError(
            '''Error inputing waveform data.
                Duplicate neuron IDs in waveform table''')
    return waveforms_table


def update_neurons(neuron_table, new_data, recording_id):

    def _mapper(row, df2, rows_to_change):
        id_ = row['neuron_id']
        if id_ in rows_to_change:
            return df2[df2['neuron_id'] == id_]['channel'].values[0]
        else:
            return row['channel']

    new_data['channel'] = pd.to_numeric(new_data.channel.str[-1])
    if len(neuron_table) == 0:
        out = new_data
    else:
        f = partial(_mapper, df2=new_data,
                    rows_to_change=new_data['neuron_id'].values)
        neuron_table['channel'] = neuron_table.apply(f, axis=1)
        out = neuron_table
    try:
        assert len(out) == len(neuron_table)
    except AssertionError:
        raise IndexError('''Error updating neuron table.
            length of table changes when merging channels''')
    return out


def save_tables(processed_data_dir, tables):
    if not isinstance(tables, dict):
        raise ValueError('''Incorrect type passed to save_tables function.
            Expected a dict. Received: {}'''.format(type(tables)))
    for table_name, df in tables.items():
        path = os.path.join(processed_data_dir, table_name) + '.csv'
        df.to_csv(path, index=False)


def main(recording_id, processed_data_dir, raw_data_dir):
    tables = get_tables(processed_data_dir)
    try:
        _check_table_data_quality(tables)
    except AssertionError:
        print('Data quality bad at input stage')
        raise

    waveform_data, channel_info = get_waveforms(recording_id, processed_data_dir,
                                                raw_data_dir,
                                                neurons_table=tables['neurons'],
                                                recordings_table=tables['recordings'],
                                                spiketimes_table=tables['spike_times'])
    try:
        tables['waveforms'] = update_waveforms(tables['waveforms'],
                                               waveform_data)
    except IndexError:
        print('''Error occured when updating waveforms.
            recording id: {}'''.format(recording_id))
        raise
    try:
        tables['neurons'] = update_neurons(
            tables['neurons'], channel_info, recording_id)
    except IndexError as e:
        raise e
    save_tables(processed_data_dir, tables)


if __name__ == '__main__':
    args = _get_options()
    main(args.recording_ids, args.db_dir, args.raw_data_dir)

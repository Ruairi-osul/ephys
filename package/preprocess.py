import numpy as np
import pandas as pd
import os
from copy import deepcopy
from functools import partial
from utils import (load_dat_data, _extract_waveforms, gen_spikes_ts_df,
                   load_kilosort_arrays, get_good_cluster_numbers,
                   loadFolderToArray, _get_sorted_channels,
                   readHeader, _walklevel, _has_ext)


def get_spike_times(p, r_id=None):
    '''Given a path to a dictory containing kilosort files,
    returns a pandas dataframe with spike times of clusters
    marked as good during spike sorting. You can optionally specify
    a the recording id for further identification'''
    spk_c, spk_tms, c_gps = load_kilosort_arrays(p)
    clusters = get_good_cluster_numbers(c_gps)
    df = gen_spikes_ts_df(spk_c, spk_tms, clusters)
    if r_id is not None:
        df['recording_id'] = r_id
    return df


def get_waveforms(spike_data, rd):
    '''Given a pandas df of spike times and the path to
    a the parent directory of the .dat file containing the raw
    data for that recording, extracts waveforms for each cluester
    and the channel on which that cluster had the highest amplitude

    params:
        spike_data: pandas df of spike times and cluster ids as cols
        rid
    '''
    raw_data = load_dat_data(p=os.path.join(
        rd, os.path.basename(rd)) + '.dat')
    f1 = partial(_extract_waveforms, raw_data=raw_data, ret='data')
    f2 = partial(_extract_waveforms, raw_data=raw_data, ret='')
    waveforms = spike_data.groupby('cluster_id')['spike_times'].apply(
        f1, raw_data=raw_data).apply(pd.Series).reset_index()
    chans = spike_data.groupby('cluster_id')[
        'spike_times'].apply(f2,
                             raw_data=raw_data).apply(pd.Series).reset_index()
    chans.columns = ['cluster_id', 'channel']
    waveforms.columns = ['cluster_id', 'sample', 'value']
    return waveforms, chans


def get_subfolders(parent, containing_filetype=None, verbose=True):
    '''Used in automatic preprocessing [continuous -> .dat -> kilosort]

    Given a parant directory, provides subdirectories that

    Usage:
        dirs_with_npy_files =  get_subfolders(
            some_dir, containing_filetype='.npy')
    '''

    # get paths
    try:
        paths = [x[0]
                 for x in _walklevel(parent, level=1) if
                 os.path.isdir(x[0])]
        if parent in paths:
            del paths[paths.index(parent)]
    except AssertionError:
        if verbose:
            print('Could not find {} dir'.format(parent))
        raise

    # filter to only have the ext.
    if containing_filetype:
        f = partial(_has_ext, ext=containing_filetype)
        paths = list(filter(f, paths))

    return paths


def loadContinuous(filepath, dtype=float):

        # constants
    NUM_HEADER_BYTES = 1024
    SAMPLES_PER_RECORD = 1024
    BYTES_PER_SAMPLE = 2
    RECORD_SIZE = 4 + 8 + SAMPLES_PER_RECORD * BYTES_PER_SAMPLE + \
        10  # size of each continuous record in bytes

    assert dtype in (float, np.int16), \
        'Invalid data type specified for loadContinous, valid types are float and np.int16'

    print("Loading continuous data...")

    ch = {}

    # read in the data
    f = open(filepath, 'rb')

    fileLength = os.fstat(f.fileno()).st_size

    # calculate number of samples
    recordBytes = fileLength - NUM_HEADER_BYTES
    if recordBytes % RECORD_SIZE != 0:
        raise Exception('''File size is not consistent with a
                        continuous file: may be corrupt''')
    nrec = recordBytes // RECORD_SIZE
    nsamp = nrec * SAMPLES_PER_RECORD
    # pre-allocate samples
    samples = np.zeros(nsamp, dtype)
    timestamps = np.zeros(nrec)
    recordingNumbers = np.zeros(nrec)
    indices = np.arange(0, nsamp + 1, SAMPLES_PER_RECORD, np.dtype(np.int64))

    header = readHeader(f)

    recIndices = np.arange(0, nrec)

    for recordNumber in recIndices:

        timestamps[recordNumber] = np.fromfile(f, np.dtype(
            '<i8'), 1)  # little-endian 64-bit signed integer
        # little-endian 16-bit unsigned integer
        N = np.fromfile(f, np.dtype('<u2'), 1)[0]

        # print index

        if N != SAMPLES_PER_RECORD:
            raise Exception(
                'Found corrupted record in block ' + str(recordNumber))

        # big-endian 16-bit unsigned integer
        recordingNumbers[recordNumber] = (np.fromfile(f, np.dtype('>u2'), 1))

        if dtype == float:  # Convert data to float array and convert bits to voltage.
            # big-endian 16-bit signed integer, multiplied by bitVolts
            data = np.fromfile(f, np.dtype('>i2'), N) * \
                float(header['bitVolts'])
        else:  # Keep data in signed 16 bit integer format.
            # big-endian 16-bit signed integer
            data = np.fromfile(f, np.dtype('>i2'), N)
        samples[indices[recordNumber]:indices[recordNumber + 1]] = data

        marker = f.read(10)  # dump

    # print recordNumber
    # print index

    ch['header'] = header
    ch['timestamps'] = timestamps
    ch['data'] = samples  # OR use downsample(samples,1), to save space
    ch['recordingNumber'] = recordingNumbers
    f.close()
    return ch


def pack_2(folderpath, filename='', channels='all', chprefix='CH',
           dref=None, session='0', source='100'):
    '''numpy array.tofile wrapper. Loads .continuous files in folderpath,
    (channels specidied by channels), applies reference and saves as .dat

    filename: Name of the output file. By default, it follows the same layout of continuous files,
              but without the channel number, for example, '100_CHs_3.dat' or '100_ADCs.dat'.

    channels:  List of channel numbers specifying order in which channels are packed. By default
               all CH continous files are packed in numerical order.

    chprefix:  String name that defines if channels from headstage, auxiliary or ADC inputs
               will be loaded.

    dref:  Digital referencing - either supply a channel number or 'ave' to reference to the
           average of packed channels.

    source: String name of the source that openephys uses as the prefix. It is usually 100,
            if the headstage is the first source added, but can specify something different.

    '''

    data_array = loadFolderToArray(
        folderpath, channels, chprefix, np.int16, session, source)

    if dref:
        if dref == 'ave':
            print('Digital referencing to average of all channels.')
            reference = np.mean(data_array, 1)
        else:
            print('Digital referencing to channel ' + str(dref))
            if channels == 'all':
                channels = _get_sorted_channels(
                    folderpath, chprefix, session, source)
            reference = deepcopy(data_array[:, channels.index(dref)])
        for i in range(data_array.shape[1]):
            data_array[:, i] = data_array[:, i] - reference

    if session == '0':
        session = ''
    else:
        session = '_' + session

    if not filename:
        filename = source + '_' + chprefix + 's' + session + '.dat'
    print('Packing data to file: ' + filename)
    data_array.tofile(os.path.join(folderpath, filename))


def update_tble(tbl, n_data, ind_name=None):
    '''Updates a table with n_data. n_data must be in the same format as tbl.

    '''
    if not ind_name:
        ind_name = tbl.columns[0]

    # checks num columns
    assert len(tbl.columns.values) == (len(n_data.columns.values) + 1), '''
    Columns do not match [should be one less in to be updated]:
        new data       {a}
        to be updated  {b}'''.format(a=n_data, b=tbl)

    # sets index of table to be primary key for later concatenation
    tbl.set_index(ind_name, inplace=True)

    if len(tbl) == 0:
        # if table to be updated is empty, set new data as output
        updated = n_data
        updated.index = pd.RangeIndex(0, len(n_data))

    else:
        # if it is not empty, set highest value in primary key to be index
        # of new data, then concatenate them on top of each other
        i = int(tbl.index.max())
        n_data.index = pd.RangeIndex(i + 1, i + 1 + len(n_data))
        updated = pd.concat([tbl, n_data])

    # set the name of the primary key and convert back from index to a column
    updated.index.name = ind_name
    updated = updated.reset_index()

    # check that
    _check_primary_key(updated, ind_name)  # no duplicates in primary key
    _check_concat(updated, tbl.reset_index())  # no changes in column numbers

    return updated


def load_table(table=None, d=None):
    '''given a parent path and table name, returns table as pandas df
    of the table

    params:
        d = parent dir of db tables
        table = name of table. can be path to table if d not specified

    Usage:
        df = load_table('neurons', d='~/data/db')
    '''

    assert table, 'table to load not specified'
    if not table.endswith('.csv'):
        table = ''.join([table, '.csv'])

    if os.path.isabs(table):
        p = table
    else:
        assert d, 'no parent diectory given to load_table'
        p = os.path.join(d, table)

    try:
        return pd.read_csv(p)
    except (IOError, OSError):
        raise ValueError('''\nTable name specified but not found.
            Tried to load: %s''' % p)


def _check_primary_key(tbl, key):
    m = '''Duplicate primary key in the following table:
    \t\t{t}
    \nDuplicate on key {k}'''.format(t=tbl, k=key)
    assert np.max(tbl[key].value_counts()) == 1, m


def _check_concat(updated, pre):
    ncols_u = len(updated.columns)
    ncols_p = len(pre.columns)
    m = '''Column numbers altered following concatenation
    pre df:
        data:\n{p}
        col nums =\n\n{pc}

    post df:
        data:\n\n{u}
        col nums = {uc}
    '''.format(p=pre, u=updated, pc=str(ncols_p),
               uc=str(ncols_u))
    assert ncols_u == ncols_p, m

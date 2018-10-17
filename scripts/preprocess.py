import numpy as np
import pandas as pd
import os
import scipy.signal
import scipy.io
import time
from copy import deepcopy

# constants
NUM_HEADER_BYTES = 1024
SAMPLES_PER_RECORD = 1024
BYTES_PER_SAMPLE = 2
RECORD_SIZE = 4 + 8 + SAMPLES_PER_RECORD * BYTES_PER_SAMPLE + \
    10  # size of each continuous record in bytes
RECORD_MARKER = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 255])

# constants for pre-allocating matrices:
MAX_NUMBER_OF_SPIKES = int(1e6)
MAX_NUMBER_OF_RECORDS = int(1e6)
MAX_NUMBER_OF_EVENTS = int(1e6)


def loadContinuous(filepath, dtype=float):

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


def _get_sorted_channels(folderpath, chprefix='CH', session='0', source='100'):
    Files = [f for f in os.listdir(folderpath) if '.continuous' in f
             and '_' + chprefix in f
             and source in f]

    if session == '0':
        Files = [f for f in Files if len(f.split('_')) == 2]
        Chs = sorted([int(f.split('_' + chprefix)[1].split('.')[0])
                      for f in Files])
    else:
        Files = [f for f in Files if len(f.split('_')) == 3
                 and f.split('.')[0].split('_')[2] == session]

        Chs = sorted([int(f.split('_' + chprefix)[1].split('_')[0])
                      for f in Files])

    return(Chs)


def readHeader(f):
    header = {}
    h = f.read(1024).decode().replace('\n', '').replace('header.', '')
    for i, item in enumerate(h.split(';')):
        if '=' in item:
            header[item.split(' = ')[0]] = item.split(' = ')[1]
    return header


def pack_2(folderpath, filename='', channels='all', chprefix='CH',
           dref=None, session='0', source='100'):
    '''Alternative version of pack which uses numpy's tofile function to write data.
    pack_2 is much faster than pack and avoids quantization noise incurred in pack due
    to conversion of data to float voltages during loadContinous followed by rounding
    back to integers for packing.

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


def loadFolderToArray(folderpath, channels='all', chprefix='CH',
                      dtype=float, session='0', source='100'):
    '''Load continuous files in specified folder to a single numpy array. By default all
    CH continous files are loaded in numerical order, ordering can be specified with
    optional channels argument which should be a list of channel numbers.'''

    if channels == 'all':
        channels = _get_sorted_channels(folderpath, chprefix, session, source)

    if session == '0':
        filelist = [source + '_' + chprefix + x +
                    '.continuous' for x in map(str, channels)]
    else:
        filelist = [source + '_' + chprefix + x + '_' +
                    session + '.continuous' for x in map(str, channels)]

    t0 = time.time()
    numFiles = 1

    channel_1_data = loadContinuous(os.path.join(
        folderpath, filelist[0]), dtype)['data']

    n_samples = len(channel_1_data)
    n_channels = len(filelist)

    data_array = np.zeros([n_samples, n_channels], dtype)
    data_array[:, 0] = channel_1_data

    for i, f in enumerate(filelist[1:]):
        data_array[:, i +
                   1] = loadContinuous(os.path.join(folderpath, f), dtype)['data']
        numFiles += 1

    print(''.join(('Avg. Load Time: ', str((time.time() - t0) / numFiles), ' sec')))
    print(''.join(('Total Load Time: ', str((time.time() - t0)), ' sec')))

    return data_array


def downsample(trace, down):
    downsampled = scipy.signal.resample(trace, np.shape(trace)[0] / down)
    return downsampled


def load_kilosort_arrays(parent_dir):
    '''
    Loads arrays generated during kilosort into numpy arrays and pandas DataFrames
    Parameters:
        parent_dir       = name of the parent_dir being analysed
    Returns:
        spike_clusters  = numpy array of len(num_spikes) identifying the cluster from which each spike arrose
        spike_times     = numpy array of len(num_spikes) identifying the time in samples at which each spike occured
        cluster_groups  = pandas DataDrame with one row per cluster and column 'cluster_group' identifying whether
                          that cluster had been marked as 'Noise', 'MUA' or 'Good'
    '''
    try:
        spike_clusters = np.load(os.path.join(
            parent_dir, 'spike_clusters.npy'))
        spike_times = np.load(os.path.join(parent_dir, 'spike_times.npy'))
        cluster_groups = pd.read_csv(os.path.join(
            parent_dir, 'cluster_groups.csv'), sep='\t')
    except IOError:
        print('Error loading Kilosort Files. Files not found')
        raise
    try:  # check data quality
        assert np.shape(spike_times.flatten()) == np.shape(spike_clusters)
    except AssertionError:
        AssertionError('Array lengths do not match in parent_dir {}'.format(
            parent_dir))
    return spike_clusters, spike_times, cluster_groups


def get_good_cluster_numbers(cluster_groups_df):
    '''
    Takes the cluster_groups pandas DataFrame fomed during data loading and returns a numpy array of cluster
    ids defined as 'Good' during kilosort and phy spike sorting
    Parameters:
        cluster_groups_df   = the pandas DataFrame containing information on which cluster is 'Good', 'Noise' etc.
    Returns:
        A numpy array of 'Good' cluster ids
    '''
    good_clusters_df = cluster_groups_df.loc[cluster_groups_df['group'] == 'good', :]
    return good_clusters_df['cluster_id'].values


def gen_df(spike_clusters, spike_times, good_cluster_nums):
    data = {'cluster_id': spike_clusters.flatten(),
            'spike_times': spike_times.flatten()}
    df = pd.DataFrame(data)
    df = df.loc[df['cluster_id'].isin(good_cluster_nums), :]
    return df


def get_waveforms(recording_id, processed_data_dir, raw_data_dir,
                  neurons_table, recordings_table, spiketimes_table,
                  num_channels=32):

    def _get_spike_times():
        neurons = neurons_table.loc[neurons_table['recording_id']
                                    == recording_id].values
        spike_times = spiketimes_table.loc[spiketimes_table['neuron_id'].isin(
            neurons)]
        return spike_times

    def _load_raw_data():
        dat_filename = recordings_table.loc[recordings_table['recording_id']
                                            == recording_id]['dat_filename'].values[0]

        path = os.path.join(raw_data_dir,
                            dat_filename, dat_filename) + '.dat'
        tmp = np.memmap(path, dtype=np.int16)  # adjust shape
        adjusted_len = int(len(tmp) / num_channels)
        return np.memmap(path, dtype=np.int16,
                         shape=(adjusted_len, num_channels))

    def _extract_waveforms(spike_times, raw_data,
                           num_spikes=1000, num_samples=240,
                           num_chans=32):
        waveform_window = np.arange(
            int(-num_samples / 2), int(num_samples / 2))
        out = []
        channels = []
        for neuron in spike_times['neuron_id'].unique():
            data = spike_times[spike_times['neuron_id']
                               == neuron]['spike_times']
            try:
                assert num_spikes <= len(data)
            except AssertionError:
                raise ValueError(
                    "not enough spikes. neuron: {}".format(neuron))

            waveforms = np.zeros((num_spikes, num_samples, num_chans))
            for i in range(num_spikes):
                start = int(data.iloc[i] + waveform_window[0])
                end = int(data.iloc[i] + waveform_window[-1] + 1)
                if start < 0:
                    start = 0
                waveforms[i, :, :] = raw_data[start:end, :]
            df = pd.DataFrame(np.mean(waveforms, axis=0),
                              columns=[''.join(['Chan_', str(i)]) for
                                       i in range(0, num_chans)])

            df_norm = df - np.mean(df)
            tmp = df_norm.apply(np.min, axis=0)
            chan_label = tmp.idxmin()
            data = df.loc[:, chan_label]
            data.name = neuron
            out.append(data)
            channels.append({'neuron_id': neuron, 'channel': chan_label})

        waveform_data = pd.concat(out, axis=1).transpose()
        waveform_data.index.name = 'neuron_id'
        waveform_data.reset_index(inplace=True)
        channel_info = pd.DataFrame(channels)
        return waveform_data, channel_info

    raw_data = _load_raw_data()
    spike_times = _get_spike_times()
    waveform_data, channel_info = _extract_waveforms(spike_times=spike_times,
                                                     raw_data=raw_data)
    return waveform_data, channel_info


def get_recording_id(subject_table, recording_path):
    try:
        df = pd.read_csv(subject_table)
    except IOError:
        print('''Recording table not found.
              Path searching: {}'''.format(subject_table))
    return df.loc[df['dat_filename'] == os.path.basename(recording_path), :]['recording_id']

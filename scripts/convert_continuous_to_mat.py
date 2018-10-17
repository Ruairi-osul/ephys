'''Convert a file saved in continuous format to a .mat file

1.
    edit the path_in variable to be the path to the


2.
    run the scrip


3.
    the data in the continuous file will be saved to a .mat file
    this file will be located in the same directory as the
    .continuous file

'''


#####################################################
#####################################################
#####################################################
#####################################################

# 'PUT THE PATH TO THE CONTINUOS FILE HERE IN QUOTES'

path_in = r'/media/ruairi/Ephys_back_up_1/CIT_WAY/good_eegchans/CIT_WAY_1_2018-05-01_15-59-19_PRE/100_CH45.continuous'

#####################################################
#####################################################
#####################################################
#####################################################

import os
import numpy as np
import scipy.io as io
import scipy.signal


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


def load(filepath):

    # redirects to code for individual file types
    if 'continuous' in filepath:
        data = loadContinuous(filepath)
    elif 'spikes' in filepath:
        data = loadSpikes(filepath)
    elif 'events' in filepath:
        data = loadEvents(filepath)
    else:
        raise Exception(
            "Not a recognized file type. Please input a .continuous, .spikes, or .events file")

    return data


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
        raise Exception(
            "File size is not consistent with a continuous file: may be corrupt")
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


def readHeader(f):
    header = {}
    h = f.read(1024).decode().replace('\n', '').replace('header.', '')
    for i, item in enumerate(h.split(';')):
        if '=' in item:
            header[item.split(' = ')[0]] = item.split(' = ')[1]
    return header


def downsample(trace, down):
    downsampled = scipy.signal.resample(trace, np.shape(trace)[0] / down)
    return downsampled


data = loadContinuous(path_in)['data']
file_name, _ = os.path.splitext(path_in)
path_out = ''.join([file_name, '.mat'])
io.savemat(path_out, mdict={'data': data})

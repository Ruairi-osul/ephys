import numpy as np
from OpenEphys import loadContinuous
import os
import glob
from scipy import signal as ss
from scipy.signal import butter, lfilter
import pandas as pd


def load_data(source_folder, recording, sep):
    '''
    loads data continuous files, returns a list of data and another list of associated
    file names
    Parameters:
        source_folder       = root direcotry containing subdirs for each recording containg the
                              continuous files
        recording           = name of the recording currently being analysed
        sep                 = operating system seperator
    '''
    data_dir = sep.join([source_folder, recording])
    os.chdir(data_dir)
    file_names = glob.glob("*.continuous")
    chans = [loadContinuous(file) for file in file_names]
    return chans, file_names


def butter_lowpass_filter(data, low_cutoff, fs, order=5):
    '''
    Designs and implemts a butterworth low pass filter
    Parameters:
        data                = numpy array of y values
        low_cuttoff         = cut off for filter e.g. 100 for 100Hz lpf
        fs                  = sampling rate of the recording
        order               = order of the butter filter
    Returns:
        y_low               = the filtered data
    '''
    def butter_lowpass(low_cutoff, fs, order=5):
        nyq = 0.5 * fs
        normal_low_cutoff = low_cutoff / nyq
        b_low, a_low = butter(order, normal_low_cutoff, btype='lowpass', analog=False)
        return b_low, a_low

    b_low, a_low = butter_lowpass(low_cutoff, fs, order=order)
    y_low = lfilter(b_low, a_low, data)
    return y_low


def downsample_fourier(data, fs, new_fs, verbose=True):
    '''
    Downsample an array using a fourier method
    Parameters:
        data            = numpy array of y values
        fs              = current sampling rate
        new_fs          = desired sampling rate
        vervose         = Bool
    Returns:
        data            = downsampled array
    '''
    if verbose:
        print('Downsampling array')
    duration = np.shape(data)[0] / fs
    new_shape = np.real(int(round(new_fs * duration)))
    return ss.resample(data, new_shape)


def downsample_decimate(data, verbose=True):
    '''
    Downsample array using scipy decimate method
    Parameters:
        data            = data to be downsampled in a numpy array
        verbose         = Bool
    Returns:
        data            = downsampled array
    '''
    if verbose:
        print('Downsampling array')
    data = ss.decimate(x=data, q=12, ftype='fir')
    data = ss.decimate(x=data, q=10, ftype='fir')
    return data


def compute_spectrum(data, new_fs, noverlap=0, secs_per_bin=4, verbose=True):
    '''
    Takes a numpy array, calculates a spectrogram over a specified size of bins
    Parameters:
        data                    = array to be downsampled
        new_fs                  = sampling rate
        noverlap                = degree of overlap in fft bins. Leave at 0 for secs_per_bin act as expected
        secs_per_bin            = seconds per time bin
        verbose                 = Bool
    Returns:
        df                      = a pandas dataframe with timedelta index of time bins
                                  and columns containing frequency information
    '''
    if verbose:
        print('Computing Spectrogram')
    samples_per_bin = new_fs * secs_per_bin

    fq, time, Sxx = ss.spectrogram(x=data,
                                   fs=new_fs,
                                   window=ss.get_window('hamming', samples_per_bin),
                                   noverlap=noverlap,
                                   nperseg=samples_per_bin)
    df = pd.DataFrame(data=Sxx,
                      columns=time,
                      index=fq).transpose()
    df = df.reset_index()
    df = df.rename(columns={'index': 'time'})
    df['time'] = pd.to_timedelta(df['time'], unit='s')
    df.set_index('time', inplace=True)
    return df


def save(recording, chan_lab, df, out_folder, sep, verbose=True):
    '''
    Saves a dataframe to a csv file
    Parameters:
        recording           = recording being analysed
        chan_lab            = channel label for the recording
        df                  = dataframe being saved
        out_folder          = root folder for csv files
        sep                 = operating system serperator
        verbose             = Bool
    '''
    chan_lab = chan_lab.split('.')[0][-4:]
    recording_outf = sep.join([out_folder, recording])
    if not os.path.exists(recording_outf):
        os.mkdir(recording_outf)
    filename = sep.join([recording_outf, recording]) + chan_lab + '.csv'
    if verbose:
        print('Saving')
    df.to_csv(filename)


def write_eeg_files(a_list, lab_list, eeg_numpy_folder, recording):
    if not os.path.exists(eeg_numpy_folder):
        os.mkdir(eeg_numpy_folder)
    target_dir = os.path.join(eeg_numpy_folder, recording)
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    data = np.stack(a_list)
    np.save(file=os.path.join(target_dir, 'data.npy'), arr=data)

    for lab in lab_list:
        if not glob.glob(os.path.join(target_dir, '*.txt')):
            with open(os.path.join(target_dir, 'chan_labs.txt'), 'w') as f:
                f.write(lab)
        else:
            with open(os.path.join(target_dir, 'chan_labs.txt'), 'a') as f:
                f.write('\n' + lab)

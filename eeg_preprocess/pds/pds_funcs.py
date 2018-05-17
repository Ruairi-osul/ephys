import numpy as np
from OpenEphys import loadContinuous
import os
import glob
from scipy import signal as ss
from scipy.signal import butter, lfilter
import pandas as pd


def load_data(source_folder, recording, sep):
    data_dir = sep.join([source_folder, recording])
    os.chdir(data_dir)
    file_names = glob.glob("*.continuous")
    chans = [loadContinuous(file) for file in file_names]
    return chans, file_names


def butter_lowpass_filter(data, low_cutoff, fs, order=5, verbose=True):
    if verbose:
        print('Filtering data')

    def butter_lowpass(low_cutoff, fs, order=5):
        nyq = 0.5 * fs
        normal_low_cutoff = low_cutoff / nyq
        b_low, a_low = butter(order,
                              normal_low_cutoff,
                              btype='low',
                              analog=False)
        return b_low, a_low

    b_low, a_low = butter_lowpass(low_cutoff, fs, order=order)
    y_low = lfilter(b_low, a_low, data)
    return y_low


def downsample_fourier(data, fs, new_fs, verbose=True):
    if verbose:
        print('Downsampling array')
    duration = np.shape(data)[0] / fs
    new_shape = np.real(int(round(new_fs * duration)))
    return ss.resample(data, new_shape)


def downsample_decimate(data, verbose=True):
    if verbose:
        print('Downsampling array')
    data = ss.decimate(x=data, q=12, ftype='fir')
    data = ss.decimate(x=data, q=10, ftype='fir')
    return data


def compute_spectrum(data, new_fs, noverlap=None, secs_per_bin=4, verbose=True):
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
    chan_lab = chan_lab.split('.')[0][-4:]
    recording_outf = sep.join([out_folder, recording])
    if not os.path.exists(recording_outf):
        os.mkdir(recording_outf)
    filename = sep.join([recording_outf, recording]) + chan_lab + '.csv'
    if verbose:
        print('Saving')
    df.to_csv(filename)

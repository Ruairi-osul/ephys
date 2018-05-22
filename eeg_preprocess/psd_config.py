from pds.pds_logic import main
from pds.pds_classes import Options

'''
Creates a csv file with frequencies as columns and time bins as time.
Data in the csv correspond to the power spectral density over time.
This csv file is used in other scripts in this repository for EEG analysis

************************************************************************************************
 Not yet completed:
    - Need to find correct method for downsampling from 30000Hz to 256Hz
    - Need to find correct method for application of 100Hz low pass filter to downsampled signal
    - Need to find appropiate technique for calculating power spectral density over time
************************************************************************************************

Change the following parameters in the Options instantiation:
    - source_folder                 = root folder containg subdirectorfolder containing good eeg channels (as .continuous files)
    - recordings_to_extract         = list of recordings for preprocessing
    - out_folder                    = root directory of
    - fs                            = sampling rate of the recording
    - low_cutoff_lpf                = low cut off for low pass filter
    - order_lpf                     = order for butterworth filter
    - new_fs                        = new sampling rate post downsampling
    - secs_per_bin                  = size of psd bins in seconds
    - operating_system              = operating system 'win' or 'unix'
    - noverlap                      = overlap parameter for spectrogram
    - downsample_method             = 'decimate' or 'fourier'
    - spectrum_method               = 'default'
    - verbose                       = True or False
'''


ops = Options(source_folder=r'D:\CIT_WAY\good_eegchans',
              recordings_to_extract=[
                  'CIT_WAY_02_2018-05-03_13-38-41_PRE'
              ],
              out_folder=r'D:\CIT_WAY\dfs\pds',
              fs=30000.0,
              low_cutoff_lpf=100,
              order_lpf=5,
              new_fs=250,
              secs_per_bin=4,
              operating_system='win',
              noverlap=0,
              downsample_method='decimate',
              spectrum_method='default',
              verbose=True
              )

if __name__ == '__main__':
    main(ops=ops)

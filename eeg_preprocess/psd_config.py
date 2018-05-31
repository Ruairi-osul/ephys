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


ops = Options(source_folder=r'C:\Users\Rory\raw_data\SERT_DREADD\good_eegchans',
              recordings_to_extract=[
                  '371a_2018-04-11_17-09-39_NO_CNO',
                  '371a_2018-04-11_17-48-20_NO_CNO_2',
                  '371a_2018-04-11_18-15-03_CNO',
                  '401a_2018-04-18_16-34-20_NO_CNO',
                  '401a_2018-04-18_17-40-36_CNO',
                  '401b_2018-04-16_14-25-14_NO_CNO',
                  '401b_2018-04-16_15-26-37_CNO',
                  '401c_2018-04-17_13-35-07_NO_CNO',
                  '401c_2018-04-17_14-38-53_CNO',
                  'unknown_2018-04-12_14-00-40_NO_CNO',
                  'unknown_2018-04-12_15-01-27_CNO'
              ],
              out_folder=r'C:\Users\Rory\raw_data\SERT_DREADD\dfs\pds',
              eeg_numpy_folder=r'C:\Users\Rory\raw_data\CIT_WAY\eeg_numpy',
              fs=30000.0,
              low_cutoff_lpf=100,
              order_lpf=5,
              new_fs=250,
              secs_per_bin=4,
              operating_system='win',
              noverlap=0,
              downsample_method='decimate',
              lpf=False,
              spectrum_method='default',
              verbose=True
              )

if __name__ == '__main__':
    main(ops=ops)

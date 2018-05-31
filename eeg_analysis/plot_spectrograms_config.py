from spectrograms.classes import Options
from spectrograms.logic import main
'''
Plots and saves a figure of the EEG data represented as a spectrogram
Requires a csv file of the power spectral density calculated every x seconds

Change the following parameters in the Options instantiation:
    pds_folder              = root folder in which subdirectories containing power spectral density csv files are located
    recordings_to_plot      = list of recordings to plot (names of subdirectories in pds_folder)
    fig_out_folder          = root folder in which figures will be saved
    operating_system        = operating system 'win' or 'unix'
    which                   = whether to plot all frequencies or 'low_freqs' or 'both'
    dpi                     = resolution of the picture produced e.g. 300
    vmin                    = minumum cutoff for colorbar
    vmax                    = maximum cutoff for colorbar
    verbose                 = True or False

ROS 2018
'''

ops = Options(pds_folder=r'C:\Users\Rory\raw_data\SERT_DREADD\dfs\pds',
              recordings_to_plot=[
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
              fig_out_folder=r'C:\Users\Rory\raw_data\SERT_DREADD\figures',
              operating_system='win',
              which='both',
              dpi=300,
              vmin=0,
              vmax=12,
              verbose=True)

if __name__ == '__main__':
  main(ops)

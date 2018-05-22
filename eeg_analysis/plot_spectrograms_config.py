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

ops = Options(pds_folder=r'D:\CIT_WAY\dfs\pds',
              recordings_to_plot=[
                  'CIT_WAY_02_2018-05-03_13-38-41_PRE'
              ],
              fig_out_folder=r'D:\CIT_WAY\figures',
              operating_system='win',
              which='both',
              dpi=300,
              vmin=0,
              vmax=12,
              verbose=True)

if __name__ == '__main__':
    main(ops)

from extract_waveforms.classes import Options
from extract_waveforms.logic import main
'''

This script extracts the waveforms of spikes marked as 'good' during spike sorting.
It plots the waveforms and calculates summary statistis related to the spike width.
All plots and statistics are saved in pre-specified folders



ROS 2018

'''


ops = Options(kilosort_folder=r'G:\Rawdata\SERT',
              recordings_to_analyse=['2018-04-18'],
              temp_folder=r'G:\Rawdata\SERT\csvs\temp',
              spike_selection_method='min',
              num_spikes=1100,
              num_channels=32,
              num_samples=240,
              fig_folder=r'G:\Rawdata\SERT\figures',
              last_spikes=False,
              thresh_udu=12,
              thresh_du=10,
              borken_channels=[22],
              fs=30000,
              verbose=True)

if __name__ == '__main__':
  main(ops)

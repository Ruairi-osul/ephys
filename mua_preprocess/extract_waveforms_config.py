from extract_waveforms.classes import Options
from extract_waveforms.logic import main
'''

This script extracts the waveforms of spikes marked as 'good' during spike sorting.
It plots the waveforms and calculates summary statistis related to the spike width.
All plots and statistics are saved in pre-specified folders



ROS 2018

'''


ops = Options(kilosort_folder=r'/home/ruairi/CIT_WAY',
              recordings_to_analyse=['CIT_09_2018-07-03', 'CIT_10_2018-07-04', 'CIT_11_2018-07-05', 'CIT_14_2018-07-06'],
              temp_folder=r'/home/ruairi/CIT_WAY/csvs/temp',
              spike_selection_method='min',
              num_spikes=1100,
              num_channels=32,
              num_samples=240,
              fig_folder=r'/home/ruairi/CIT_WAY/figures',
              last_spikes=False,
              thresh_udu=12,
              thresh_du=10,
              borken_channels=[22],
              fs=30000,
              verbose=True)

if __name__ == '__main__':
  main(ops)

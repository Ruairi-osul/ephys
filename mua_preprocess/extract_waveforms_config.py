from extract_waveforms.classes import Options
from extract_waveforms.logic import main
'''

This script extracts the waveforms of spikes marked as 'good' during spike sorting.
It plots the waveforms and calculates summary statistis related to the spike width.
All plots and statistics are saved in pre-specified folders



ROS 2018

'''

import numpy as np


ops = Options(kilosort_folder=r'C:\Users\Rory\raw_data\CIT_WAY\dat_files\cat',
              recordings_to_analyse=['2018-05-01_01'],
              spike_selection_method='min',
              num_spikes=1000,
              num_channels=32,
              num_samples=240,
              fig_folder=r'C:\Users\Rory\raw_data\CIT_WAY\figures',
              temp_folder=r'C:\Users\Rory\raw_data\CIT_WAY\temp',
              last_spikes=True,
              borken_channels=[7, 22],
              sw_out_dir=r'C:\Users\Rory\raw_data\CIT_WAY\dfs\spike_width',
              fs=30000,
              verbose=True)

if __name__ == '__main__':
    main(ops)

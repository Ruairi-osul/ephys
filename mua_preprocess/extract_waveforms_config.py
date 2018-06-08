from extract_waveforms.classes import Options
from extract_waveforms.logic import main
'''

This script extracts the waveforms of spikes marked as 'good' during spike sorting.
It plots the waveforms and calculates summary statistis related to the spike width.
All plots and statistics are saved in pre-specified folders



ROS 2018

'''


ops = Options(kilosort_folder=r'C:\Users\Rory\raw_data\CIT_WAY\dat_files\cat',
              recordings_to_analyse=['2018-05-01_01'],
              temp_folder=r'C:\Users\Rory\raw_data\CIT_WAY\temp',
              spike_selection_method='min',
              num_spikes=1100,
              num_channels=32,
              num_samples=240,
              fig_folder=r'C:\Users\Rory\raw_data\CIT_WAY\figures', ,
              last_spikes=False,
              thresh_udu=12,
              thresh_du=10,
              borken_channels=[7, 22],
              sw_out_dir=r'C:\Users\Rory\raw_data\CIT_WAY\dfs\spike_width',
              fs=30000,
              verbose=True)

if __name__ == '__main__':
    main(ops)

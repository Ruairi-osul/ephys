from extract_waveforms.classes import Options
from extract_waveforms.logic import main
'''

This script extracts the waveforms of spikes marked as 'good' during spike sorting.
It plots the waveforms and calculates summary statistis related to the spike width.
All plots and statistics are saved in pre-specified folders



ROS 2018

'''


ops = Options(kilosort_folder=r'E:\SERT_DREADD\dat_files\Combined_binary_files_probe',
              recordings_to_analyse=['2018-04-10_391b', '2018-04-11_371a',
                                     '2018-04-12_371b', '2018-04-16_401b',
                                     '2018-04-17_401c', '2018-04-18_40.1a'],
              temp_folder=r'E:\SERT_DREADD\temp',
              spike_selection_method='min',
              num_spikes=1100,
              num_channels=32,
              num_samples=240,
              fig_folder=r'E:\SERT_DREADD\figures\waveforms',
              last_spikes=False,
              thresh_udu=12,
              thresh_du=10,
              borken_channels=[22],
              fs=30000,
              verbose=True)

if __name__ == '__main__':
    main(ops)

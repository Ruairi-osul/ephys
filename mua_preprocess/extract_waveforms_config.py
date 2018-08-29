from extract_waveforms.classes import Options
from extract_waveforms.logic import main
'''

This script extracts the waveforms of spikes marked as 'good' during spike sorting.
It plots the waveforms and calculates summary statistis related to the spike width.
All plots and statistics are saved in pre-specified folders



ROS 2018

'''


ops = Options(kilosort_folder=r'E:\CIT_WAY\dat_files\cat',
              recordings_to_analyse=['Chronic_03_2018-07-29', 'Chronic_04_2018-08-05', 'Chronic_11_2018-08-04', 'Chronic_13_2018_08_08', 'Chronic_14_2018-08-14', 'Chronic_30_2018-07-28', 'Chronic_31_2018-08-10', 'Chronic_33_2018-07-30', 'Chronic_40_2018-08-13', 'Chronic_41_2018-08-09'],
              temp_folder=r'E:\CIT_WAY\dat_files\cat\temp',
              spike_selection_method='min',
              num_spikes=1100,
              num_channels=32,
              num_samples=240,
              fig_folder=r'/media/ruairi/Ephys_back_up_1/SERT_DREADD/figures/waveforms',
              last_spikes=False,
              thresh_udu=12,
              thresh_du=10,
              borken_channels='',
              fs=30000,
              verbose=True)

if __name__ == '__main__':
  main(ops)

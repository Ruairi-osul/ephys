from spiking_statistics.logic import main
from spiking_statistics.classes import Options

'''
Create temperary file with neuron stats.

method = 'elephant' or 'numpy'

averaging_method = 'mean', 'median', or 'ruairi_old_median'

experiment = 'CIT' or 'DREADD'
'''

ops = Options(recordings_to_analyse=['Chronic_03_2018-07-29', 'Chronic_04_2018-08-05', 'Chronic_11_2018-08-04', 'Chronic_13_2018_08_08', 'Chronic_14_2018-08-14', 'Chronic_30_2018-07-28', 'Chronic_31_2018-08-10', 'Chronic_33_2018-07-30', 'Chronic_40_2018-08-13', 'Chronic_41_2018-08-09'],
              data_dir=r'E:\CIT_WAY\dat_files\cat\spikes_time_series',
              experiment='CIT',
              temp_folder=r'E:\CIT_WAY\dat_files\cat\csvs\temp',
              fig_folder=r'E:\CIT_WAY\dat_files\cat\figures\cluster_over_time',
              mfr_method = 'notnull',
              averaging_method = 'mean',
              verbose=True)

if __name__ == '__main__':
    main(ops)

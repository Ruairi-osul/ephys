from spiking_statistics.logic import main
from spiking_statistics.classes import Options

'''
Create temperary file with neuron stats.

method = 'elephant' or 'numpy'

averaging_method = 'mean', 'median', or 'ruairi_old_median'

experiment = 'CIT' or 'DREADD'
'''

ops = Options(recordings_to_analyse=['2018-04-12_371b', '2018-04-16_401b', '2018-04-17_401c', '2018-04-18'],
              data_dir=r'G:\Rawdata\SERT\spikes_time_series',
              experiment='DREADD',
              temp_folder=r'G:\Rawdata\SERT\csvs\temp',
              fig_folder=r'G:\Rawdata\SERT\figures\cluster_over_time',
              mfr_method = 'notnull',
              averaging_method = 'mean',
              verbose=True)

if __name__ == '__main__':
    main(ops)

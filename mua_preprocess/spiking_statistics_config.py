from spiking_statistics.logic import main
from spiking_statistics.classes import Options

'''
Create temperary file with neuron stats.

method = 'elephant' or 'numpy'

averaging_method = 'mean', 'median', or 'ruairi_old_median'

experiment = 'CIT' or 'DREADD'
'''

ops = Options(recordings_to_analyse=['CIT_09_2018-07-03', 'CIT_10_2018-07-04', 'CIT_11_2018-07-05', 'CIT_14_2018-07-06'],
              data_dir=r'/home/ruairi/CIT_WAY/spikes_time_series',
              experiment='CIT',
              temp_folder=r'/home/ruairi/CIT_WAY/csvs/temp',
              fig_folder=r'/home/ruairi/CIT_WAY/figures/cluster_over_time',
              mfr_method = 'notnull',
              averaging_method = 'mean',
              verbose=True)

if __name__ == '__main__':
    main(ops)

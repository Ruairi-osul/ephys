from spiking_statistics.logic import main
from spiking_statistics.classes import Options

'''
Create temperary file with neuron stats.
'''

ops = Options(recordings_to_analyse=['2018-05-01_01'],
              data_dir=r'C:\Users\Rory\raw_data\CIT_WAY\spikes_df',
              experiment='CIT',
              temp_folder=r'C:\Users\Rory\raw_data\CIT_WAY\temp',
              fig_folder=r'C:\Users\Rory\raw_data\CIT_WAY\figures\cluster_over_time',
              verbose=True)

if __name__ == '__main__':
    main(ops)

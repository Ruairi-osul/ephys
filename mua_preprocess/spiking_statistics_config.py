from spiking_statistics.logic import main
from spiking_statistics.classes import Options

'''
Create temperary file with neuron stats.
'''

ops = Options(recordings_to_analyse=['2018-05-01_01'],
              data_dir=r'F:\CIT_WAY\spikes_time_series',
              experiment='CIT',
              temp_folder=r'F:\CIT_WAY\csvs\temp',
              fig_folder=r'F:\CIT_WAY\figures\cluster_over_time',
              verbose=True)

if __name__ == '__main__':
    main(ops)

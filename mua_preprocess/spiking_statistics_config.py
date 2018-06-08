from spiking_statistics.logic import main
from spiking_statistics.classes import Options

'''
Create temperary file with neuron stats.
'''

ops = Options(recordings_to_analyse=['2018-04-10_391b', '2018-04-11_371a',
                                     '2018-04-12_371b', '2018-04-16_401b',
                                     '2018-04-17_401c', '2018-04-18_40.1a'],
              data_dir=r'E:\SERT_DREADD\csvs\spikes_time_series',
              experiment='DREADD',
              temp_folder=r'E:\SERT_DREADD\temp',
              fig_folder=r'E:\SERT_DREADD\figures\cluster_over_time',
              verbose=True)

if __name__ == '__main__':
    main(ops)

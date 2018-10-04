from spiking_statistics.logic import main
from spiking_statistics.classes import Options

'''
Create temperary file with neuron stats.

method = 'elephant' or 'numpy'

averaging_method = 'mean', 'median', or 'ruairi_old_median'

experiment = 'CIT' or 'DREADD'
'''

ops = Options(recordings_to_analyse=['2018-10-02'],
              data_dir=r'/media/ruairi/UBUNTU/SERT_DREADD/csvs',
              experiment='DREADD',
              temp_folder=r'/media/ruairi/UBUNTU/SERT_DREADD/csvs/temp',
              fig_folder=r'/media/ruairi/UBUNTU/SERT_DREADD/figures/cluster_over_time',
              mfr_method='notnull',
              averaging_method='ruairi_old_median',
              verbose=True)

if __name__ == '__main__':
    main(ops)

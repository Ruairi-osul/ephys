from neuron_heatmap.classes import Options
from neuron_heatmap.logic import main

'''
This script plots a heatmap of neuronal firing over time (one row per neuron, x is time).
It relies of a spikes_df csv file (one row per spike, column for cluster id, column for time).
Saves one figure per recording in the fig_dir.

Parameters to change:
    recordings_to_analyse   = list of recordings to analyse (must be names of directories in data_dir)
    data_dir                = root directory of spikes_df csv files
    condition               = condition overwhich statistics are calculated for normalisation.
                              'Baseline'
    rolling                 = numper of periods over which rolling mean firing rate is calculated
    resample_period         = size of time bins over which
                              'sec' or 'min'; '10sec' or '10min'
    method                  = method for normalisation.
                              'zscore' or 'percent'
    dpi                     = resolution of the produced figure
    vmin                    = minimum value for color bar
    vmax                    = maximum value for color bar
    operating_system        = 'win' if windows otherwise 'unix'
    verbose                 = True or False
'''


ops = Options(recordings_to_analyse=['2018-05-01_01',
                                     '2018-05-07_03'],
              data_dir=r'C:\Users\Rory\raw_data\CIT_WAY\spikes_df',
              fig_dir=r'C:\Users\Rory\raw_data\CIT_WAY\figures',
              condition='Baseline',
              method='percent',
              dpi=300,
              vmin=0,
              vmax=200,
              verbose=True,
              resample_period='60sec',
              rolling=200,
              operating_system='win')

if __name__ == '__main__':
    main(ops)

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


ops = Options(recordings_to_analyse=['2018-04-10_391b', '2018-04-11_371a',
                                     '2018-04-12_371b', '2018-04-16_401b',
                                     '2018-04-17_401c', '2018-04-18_40.1a',
                                     '2018-04-18_391a'],
              data_dir=r'E:\SERT_DREADD\dfs\spikes_df',
              fig_dir=r'E:\SERT_DREADD\figures',
              condition='Baseline',
              method='zscore',
              dpi=300,
              vmin=-3,
              vmax=3,
              verbose=True,
              resample_period='60sec',
              rolling=200,
              operating_system='win')

if __name__ == '__main__':
    main(ops)

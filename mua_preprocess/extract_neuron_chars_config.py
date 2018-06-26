from extract_neuron_chars.classes import Options
from extract_neuron_chars.logic import main

'''
To be run following Spike Sorting with Kilosort and Phy
*** NeuroTools package must be installed!

Generates two csv files:
    spikes_df                = contains one  row for each spike arrising from 'good' clusters
    neruons_characteristics  = one row for each good cluster with columns
                               containing summary statistics of that clusters
                               firing properties

Parameters to change:
    recordings_to_extract    = list of recordings recordings
                               ** must be a list - even if a list of one recording
    kilosort_folder          = parent folder for dirs in which kilosort files are stored
    experiment               = 'DREADD' or 'CIT'
                                determines how to label the condition column of spikes_df
    spikes_df_csv_out_folder = root folder in which spikes_df csv files will be saved
    nrn_char_out_fol         = root folder in which neuron_characteristics csv files will be saved
    sampling_rate            = sampling rate of the recording
    chars_condition          = condition over which the summary statistics saved in
                               neuron_characteristics will be saved e.g. Baseline
    verbose                  = True or False
    operating_system         = 'win' if windows, otherwise 'unix'
'''

ops = Options(recordings_to_extract=['2018-05-01_01'],
              experiment='CIT',
              kilosort_folder=r'F:\CIT_WAY',
              spikes_df_csv_out_folder=r'F:\CIT_WAY\spikes_time_series',
              sampling_rate=30000,
              chars_condition='Baseline',
              verbose=True,
              operating_system='win'
              )

if __name__ == '__main__':
  main(ops)

from Fancy_traceview.classes import Options
from Fancy_traceview.logic import main

# time_span_chosen == total time available to scroll
# view_window == default time window displayed
# thumbs up to TT for color option



ops = Options(kilosort_folder=r'/media/ruairi/Ephys_back_up_1/CIT_WAY/dat_files/cat',
              recording='2018-05-01_01',
              chosen_cluster=122,
              time_span_chosen = [60, 61],
              num_channels=32,
              broken_chans=[22],
              view_window = 6, 
              num_spikes_for_averaging=3000,
              verbose=True,
              color='rgb(102, 153, 255)',
              operating_system='unix')

if __name__ == '__main__':
    main(ops)

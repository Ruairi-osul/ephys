from extract_traceview.classes import Options
from extract_traceview.logic import main


ops = Options(kilosort_folder=r'/Users/sharplab/tran/cat/Tran',
              recording='2018-04-12_371b',
              chosen_cluster=2,
              time_chosen=2250, time_span=3,
              num_channels=32,
              broken_chans=[22],
              num_spikes_for_averaging=3000,
              verbose=True,
              color='b',
              operating_system='unix')


if __name__ == '__main__':
    main(ops)

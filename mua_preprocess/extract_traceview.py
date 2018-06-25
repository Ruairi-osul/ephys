from extract_traceview.classes import Options
from extract_traceview.logic import main


<<<<<<< HEAD
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
=======
ops = Options(kilosort_folder=r'/Users/sharplab/tran/cat/Tran', recording='2018-04-12_371b', chosen_cluster=11, time_chosen=2250, time_span=3, num_channels=32, broken_chans=[22], num_spikes_for_averaging=3000, verbose=True, operating_system='unix')
>>>>>>> 073cf513f7d31bb90f4ee18413db72ac8103036c


if __name__ == '__main__':
    main(ops)

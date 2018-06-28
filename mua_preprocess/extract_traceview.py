from extract_traceview.classes import Options
from extract_traceview.logic import main


ops = Options(kilosort_folder=r'F:\CIT_WAY',
              recording='2018-05-01_01',
              chosen_cluster=33,
              time_chosen=60*100, time_span=10,
              num_channels=32,
              broken_chans=[22],
              num_spikes_for_averaging=3000,
              verbose=True,
              color='b',
              operating_system='win')



if __name__ == '__main__':
    main(ops)

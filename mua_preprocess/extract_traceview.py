from extract_traceview.classes import Options
from extract_traceview.logic import main


ops = Options(kilosort_folder=r'E:\CIT_WAY\dat_files\cat',
              recording='2018-05-01_01',
              chosen_cluster=59,
              time_chosen=60*6, time_span=5,
              num_channels=32,
              broken_chans=[22],
              num_spikes_for_averaging=3000,
              verbose=True,
              color='b',
              operating_system='win')



if __name__ == '__main__':
    main(ops)

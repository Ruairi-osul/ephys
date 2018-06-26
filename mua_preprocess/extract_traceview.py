from extract_traceview.classes import Options
from extract_traceview.logic import main


ops = Options(kilosort_folder=r'F:\SERT_DREAD\Combined_binary_files_probe',
              recording='2018-04-12_371b',
              chosen_cluster=134,
              time_chosen=60*80, time_span=60,
              num_channels=32,
              broken_chans=[22],
              num_spikes_for_averaging=3000,
              verbose=True,
              color='b',
              operating_system='win')



if __name__ == '__main__':
    main(ops)

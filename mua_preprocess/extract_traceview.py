from extract_traceview.classes import Options
from extract_traceview.logic import main


ops = Options(kilosort_folder=r'D:\SERT_DREADD\dat_files\cat',
              recording='2018-04-12_371b',
              chosen_cluster=119,
              time_chosen=60 * 10,
              time_span=5,
              num_channels=32,
              broken_chans=[22],
              num_spikes_for_averaging=3000,
              verbose=True,
              color='#CCCC00',
              operating_system='win')

if __name__ == '__main__':
    main(ops)

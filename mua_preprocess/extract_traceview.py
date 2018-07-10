from extract_traceview.classes import Options
from extract_traceview.logic import main


ops = Options(kilosort_folder=r'G:\Rawdata\SERT',
              recording='2018-04-12_371b',
              chosen_cluster=154,
              time_chosen=60*25, time_span=10,
              num_channels=32,
              broken_chans=[22],
              num_spikes_for_averaging=3000,
              verbose=True,
              color='#0392cf',
              operating_system='win')

if __name__ == '__main__':
    main(ops)

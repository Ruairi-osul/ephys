from Fancy_traceview.classes import Options
from Fancy_traceview.logic import main


ops = Options(kilosort_folder=r'G:\Rawdata\SERT',
              recording='2018-04-12_371b',
              chosen_cluster=154,
              time_span_chosen = [60, 61],
              num_channels=32,
              broken_chans=[22],
              view_window = 6, 
              num_spikes_for_averaging=3000,
              verbose=True,
              color='rgb(102, 153, 255)',
              operating_system='win')

if __name__ == '__main__':
    main(ops)
    

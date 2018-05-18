from pds.pds_logic import main
from pds.pds_classes import Options

'''

'''
ops = Options(source_folder=r'D:\CIT_WAY\good_eegchans',
              recordings_to_extract=[
                  'CIT_WAY_02_2018-05-03_13-38-41_PRE'

              ],
              out_folder=r'D:\CIT_WAY\dfs\pds',
              fs=30000.0,
              low_cutoff_lpf=100,
              order_lpf=5,
              new_fs=250,
              secs_per_bin=4,
              operating_system='win',
              noverlap=0,
              downsample_method='decimate',
              spectrum_method='default',
              verbose=True
              )

if __name__ == '__main__':
    main(ops=ops)

from pds.pds_logic import main
from pds.pds_classes import Options

'''

'''
ops = Options(source_folder=r'D:\SERT_DREADD\good_eegchans',
              recordings_to_extract=[
                  '371a_2018-04-11_17-09-39_NO_CNO',
                  '371a_2018-04-11_17-48-20_NO_CNO_2',
                  '371a_2018-04-11_18-15-03_CNO',
                  '401a_2018-04-18_16-34-20_NO_CNO',
                  '401a_2018-04-18_17-40-36_CNO',
                  '401b_2018-04-16_14-25-14_NO_CNO',
                  '401b_2018-04-16_15-26-37_CNO',
                  '401c_2018-04-17_13-35-07_NO_CNO',
                  '401c_2018-04-17_14-38-53_CNO',
                  'unknown_2018-04-12_14-00-40_NO_CNO',
                  'unknown_2018-04-12_15-01-27_CNO'

              ],
              out_folder=r'D:\SERT_DREADD\dfs\pds',
              fs=30000.0,
              low_cutoff_lpf=100,
              order_lpf=5,
              new_fs=250,
              secs_per_bin=4,
              operating_system='win',
              noverlap=None,
              downsample_method='decimate',
              verbose=True
              )

if __name__ == '__main__':
    main(ops=ops)

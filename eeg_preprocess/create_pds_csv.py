import pds_funcs as pds
from create_pds_main import main

ops = pds.Options(source_folder=r'D:\SERT_DREADD\good_eegchans',
                  recordings_to_extract=['371a_2018-04-11_17-09-39_NO_CNO'],
                  out_folder=r'D:\SERT_DREADD\dfs\pds',
                  fs=30000.0,
                  low_cutoff_lpf=100,
                  order_lpf=5,
                  new_fs=256,
                  secs_per_bin=4,
                  operating_system='win')

if __name__ == '__main__':
    main(ops=ops)

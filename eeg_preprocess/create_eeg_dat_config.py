
# coding: utf-8

from pack_todat_eeg.classes import Options
from pack_todat_eeg.logic import main


'''

This script converts many .continuous files to one .dat file
It does this with the purpose of creating one .dat file for all the EEG
channels of interest

Change the following parameters in the Options call:
    openephys_folder = root directory of subdirectories containing .continuous files

    recordings_to_pack = list of subfolder names (containing .continuous files)
        within openephys_folder of the recordings you wish to pack

    dat_folder = output folder for the packed .dat file

    chan_map = rearrange channel labels in the eeg_chan_nums variable

    operating_system = 'win' if windows, 'unix' if anything else

NOTE:
    OpenEphys.py must be in the working directory


ROS 2018

'''

eeg_chan_nums = [43, 44, 45,
                 46, 47, 48]

ops = Options(recordings_to_pack=['401b_2018-04-16_14-25-14_NO_CNO',
                                  '401c_2018-04-17_13-35-07_NO_CNO',
                                  'unknown_2018-04-12_14-00-40_NO_CNO'],
              openephys_folder=r'C:\Users\Rory\raw_data\SERT_DREADD\continuous',
              dat_folder=r'C:\Users\Rory\raw_data\SERT_DREADD\dat_files\eeg',
              operating_system='win',
              chan_map=eeg_chan_nums,
              ref_method=''
              )


if __name__ == '__main__':
    main(ops)

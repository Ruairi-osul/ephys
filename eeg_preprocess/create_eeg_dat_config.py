
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

eeg_chan_nums = [33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45,
                 46, 47, 48]

ops = Options(recordings_to_pack=['CIT_WAY_04_2018-05-17_14-30-50_PRE',
                                  'CIT_WAY_05_2018-05-20_16-16-49_PRE',
                                  'CIT_WAY_05_2018-05-20_17-17-39_CIT',
                                  'test_2018-05-17_13-50-28_occ',
                                  'test_2018-05-17_13-54-49_occ_fl'],
              openephys_folder=r'C:\Users\Rory\raw_data\CIT_WAY\continuous',
              dat_folder=r'C:\Users\Rory\raw_data\CIT_WAY\dat_files\eeg',
              operating_system='win',
              chan_map=eeg_chan_nums,
              ref_method='',
              verbose=True
              )


if __name__ == '__main__':
    main(ops)

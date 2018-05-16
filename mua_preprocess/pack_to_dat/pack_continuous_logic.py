
# coding: utf-8

import os
from OpenEphys import pack_2
from classes import Options

'''

This script converts many .continuous files to one .dat file

Change the following parameters:
    openephys_folder = folder containing folders of .continuous files

    recordings_to_pack = list of subfolder names (containing .continuous files)
        within openephys_folder of the recordings you wish to pack

    dat_folder = output folder for the packed .dat file

    chan_map = rearrange channel labels such that channels most physically
        close to each other have consecutive labels
        N.B. only use this if the channel map is not already configured during
        the recordings

NOTE:
    OpenEphys.py must be in the working directory


ROS 2018

'''

# params to change

recordings_to_pack = ['401b_2018-04-16_14-25-14_NO_CNO',
                      '401b_2018-04-16_15-26-37_CNO']

openephys_folder = r'C:\Users\Rory\raw_data\SERT_DREADD\continuous'
dat_folder = r'C:\Users\Rory\raw_data\SERT_DREADD\dat_files'
operating_system = 'win'
# for cambridge: linear from top of first shank to bottom of second shank


cambridge_chan_map = [22, 17, 28, 25, 29, 26, 20, 23,
                      21, 27, 31, 18, 30, 19, 24, 32,
                      6, 1, 12, 9, 13, 10, 4, 7, 5, 11,
                      15, 2, 14, 3, 8, 16]

chan_map = cambridge_chan_map

ref_method = 'ave'  # 'ave' for common average reference, otherwise chan nums


# pack files

sep = '\\' if operating_system == 'win' else '/'
for recording_to_pack in recordings_to_pack:
    print(recording_to_pack)
    raw_data = sep.join([openephys_folder, recording_to_pack])
    dat_file_outfolder = sep.join([dat_folder, recording_to_pack])
    dat_file_name = sep.join([dat_file_outfolder, recording_to_pack]) + '.dat'

    if not os.path.exists(dat_file_outfolder):
        os.makedirs(dat_file_outfolder)

    pack_2(folderpath=raw_data,
           filename=dat_file_name,
           channels=chan_map,
           chprefix='CH',
           dref=ref_method,
           session='0',
           source='100')

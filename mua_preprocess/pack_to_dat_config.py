from pack_to_dat.classes import Options
from pack_to_dat.pack_continuous_logic import main
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

    ref_method = Once the data is packed to a single dat file, a filter can be
                 applied to increase the quality of the signal. Choose an
                 integer to subtract that channel from all others. Use ave to
                 apply a common average reference.

    operating_system = the operating_system on which the sript is being run
                       choose 'win' or 'unix'


ROS 2018

'''
cambridge_chan_map = [22, 17, 28, 25, 29, 26, 20, 23,
                      21, 27, 31, 18, 30, 19, 24, 32,
                      6, 1, 12, 9, 13, 10, 4, 7, 5, 11,
                      15, 2, 14, 3, 8, 16]

ops = Options(recordings_to_pack=['CIT_WAY_05_2018-05-20_16-16-49_PRE',
                                  'CIT_WAY_05_2018-05-20_17-17-39_CIT'],
              openephys_folder=r'C:\Users\Rory\raw_data\CIT_WAY',
              dat_folder=r'C:\Users\Rory\raw_data\CIT_WAY\dat_files',
              chan_map=cambridge_chan_map,
              ref_method='ave',
              operating_system='win',
              verbose=True)

if __name__ == '__main__':
    main(ops)

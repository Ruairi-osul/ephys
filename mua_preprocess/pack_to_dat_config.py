'''
This script converts many .continuous files to one .dat file

Change the following parameters:
    openephys_folder = root directory containing subdirectories containing .continuous files

    recordings_to_pack = list of subdirecotry names (containing .continuous files)
                         within openephys_folder of the recordings you wish to pack

    dat_folder = root output folder for the packed .dat file

    chan_map = rearrange channel labels such that channels most physically
               close to each other have consecutive labels
               N.B. only use this if the channel map is not already configured during
               the recordings

    ref_method = Once the data is packed to a single dat file, a filter can be
                 applied to increase the quality of the signal. Choose an
                 integer to sls
                 ubtract that channel from all others. Use ave to
                 apply a common average reference.

    operating_system = the operating_system on which the sript is being run
                       choose 'win' or 'unix'
our code is located in one file, t

ROS 2018

'''


from pack_to_dat.classes import Options
from pack_to_dat.pack_continuous_logic import main


cambridge_chan_map = [22, 17, 28, 25, 29, 26, 20, 23,
                      21, 27, 31, 18, 30, 19, 24, 32,
                      6, 1, 12, 9, 13, 10, 4, 7, 5, 11,
                      15, 2, 14, 3, 8, 16]

ops = Options(recordings_to_pack=['Chronic_31_2018-08-10_13-49-50_PRE', 
                                  'Chronic_31_2018-08-10_14-52-27_CIT', 
                                  'Chronic_31_2018-08-10_15-52-52_WAY',
                                  'Chronic_33_2018-07-30_16-04-03_PRE',
                                  'Chronic_33_2018-07-30_17-07-11_CIT',
                                  'Chronic_33_2018-07-30_18-08-22_WAY',
                                  'Chronic_41_2018-08-09_15-34-14_PRE',
                                  'Chronic_41_2018-08-09_16-35-35_CIT',
                                  'Chronic_41_2018-08-09_17-36-56_WAY'],
              openephys_folder=r'/media/ruairi/UBUNTU/CIT_WAY/continuous',
              dat_folder=r'/media/ruairi/UBUNTU/CIT_WAY/dat_files',
              chan_map=cambridge_chan_map,
              ref_method='ave',
              operating_system='unix',
              verbose=True)

if __name__ == '__main__':
    main(ops)

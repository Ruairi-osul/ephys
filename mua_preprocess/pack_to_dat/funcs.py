import os


def gen_paths(openephys_folder, recording, dat_folder, sep, verbose):
    '''
    Generates absolute path to raw data and a direcory for the dat file
    Parameters:
        openephys_folder    = root directory of continuous files
        recording           = name of subdirectory in which continuous files are stored
        dat_folder          = root directory of dat files
        sep                 = os serporator e.g. '\\'
        verbose             = True or False
    '''
    if verbose:
        print('\n\n\nNow packing recording:\t{}'.format(recording))
        print('Creating Directories for Dat Files....')
    raw_data = sep.join([openephys_folder, recording])
    dat_out_folder = sep.join([dat_folder, recording])
    if not os.path.exists(dat_out_folder):
        os.mkdir(dat_out_folder)
    file_name = sep.join([dat_out_folder, recording]) + '.dat'

    return raw_data, file_name

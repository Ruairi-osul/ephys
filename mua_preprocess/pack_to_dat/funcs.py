import os


def gen_paths(openephys_folder, recording, dat_folder, sep, verbose):
    raw_data = sep.join([openephys_folder, recording])
    dat_out_folder = sep.join([dat_folder, recording])
    if not os.path.exists(dat_out_folder):
        os.mkdir(dat_out_folder)
    file_name = sep.join([dat_out_folder, recording]) + '.dat'

    return raw_data, file_name

from OpenEphys import pack_2
from funcs import gen_paths

'''
Logic for EEG pack to dat
    - generate paths to data and dat out folder
    - pack and save dat file
'''


def main(ops):
    for recording_to_pack in ops.recordings_to_pack:
        raw_data, dat_file_name = gen_paths(openephys_folder=ops.openephys_folder,
                                            recording=ops.recordings_to_pack,
                                            dat_folder=ops.dat_folder,
                                            sep=ops.sep,
                                            verbose=ops.verbose)

    pack_2(folderpath=raw_data,
           filename=dat_file_name,
           channels=ops.chan_map,
           chprefix='CH',
           dref=ops.ref_method,
           session='0',
           source='100')

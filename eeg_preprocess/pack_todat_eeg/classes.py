class Options:

    def __init__(self, recordings_to_pack, openephys_folder, dat_folder,
                 chan_map, ref_method, operating_system):
        self.recordings_to_pack = recordings_to_pack
        self.openephys_folder = openephys_folder
        self.dat_folder = dat_folder
        self.operating_system = operating_system
        self.chan_map = chan_map
        self.ref_method = ref_method
        self.sep = '\\' if self.operating_system == 'win' else '/'

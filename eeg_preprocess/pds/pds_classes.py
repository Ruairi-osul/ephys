class Options:

    def __init__(self, source_folder, recordings_to_extract, out_folder, fs,
                 low_cutoff_lpf, order_lpf, new_fs, secs_per_bin,
                 operating_system, noverlap, downsample_method, verbose=True):
        self.source_folder = source_folder
        self.recordings_to_extract = recordings_to_extract
        self.out_folder = out_folder
        self.fs = fs
        self.low_cutoff_lpf = low_cutoff_lpf
        self.order_lpf = order_lpf
        self.new_fs = new_fs
        self.secs_per_bin = secs_per_bin
        self.operating_system = operating_system
        self.noverlap = noverlap
        self.downsample_method = downsample_method
        self.verbose = verbose
        self.sep = '\\' if self.operating_system == 'win' else '/'

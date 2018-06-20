class Options:

    def __init__(self, recordings_to_analyse, data_dir, fig_dir, condition, rolling, resample_period, method, dpi, vmin, vmax, verbose, operating_system):
        self.recordings_to_analyse = recordings_to_analyse
        self.data_dir = data_dir
        self.fig_dir = fig_dir
        self.condition = condition
        self.rolling = rolling
        self.resample_period = resample_period
        self.method = method
        self.dpi = dpi
        self.vmin = vmin
        self.vmax = vmax
        self.verbose = verbose
        self.operating_system = operating_system
        self.sep = '\\' if self.operating_system == 'win' else '/'

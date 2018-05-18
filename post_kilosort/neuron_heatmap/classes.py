class Options:

    def __init__(self, recordings_to_analyse, data_dir, fig_dir, condition, rolling, method, dpi, vmin, vmax, operating_system):
        self.recordings_to_analyse = recordings_to_analyse
        self.data_dir = data_dir
        self.fig_dir = fig_dir
        self.condition = condition
        self.rolling = rolling
        self.method = method
        self.dpi = dpi
        self.vmin = vmin
        self.vmax = vmax
        self.operating_system = operating_system

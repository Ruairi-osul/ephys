class Options:

    def __init__(self, pds_folder, recordings_to_plot, fig_out_folder, operating_system, which, dpi, vmin, vmax, verbose):
        self.pds_folder = pds_folder
        self.recordings_to_plot = recordings_to_plot
        self.fig_out_folder = fig_out_folder
        self.operating_system = operating_system
        self.which = which
        self.dpi = dpi
        self.vmin = vmin
        self.vmax = vmax
        self.verbose = verbose
        self.sep = '\\' if self.operating_system == 'win' else '/'

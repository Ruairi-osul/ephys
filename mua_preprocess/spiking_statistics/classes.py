class Options:

    def __init__(self, recordings_to_analyse, data_dir, experiment, temp_folder, fig_folder, mfr_method, averaging_method, verbose):
        self.recordings_to_analyse = recordings_to_analyse
        self.data_dir = data_dir
        self.experiment = experiment
        self.temp_folder = temp_folder
        self.fig_folder = fig_folder
        self.mfr_method = mfr_method
        self.averaging_method = averaging_method
        self.verbose = verbose

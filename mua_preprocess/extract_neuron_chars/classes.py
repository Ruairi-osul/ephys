class Options():

    def __init__(self, recordings_to_extract, kilosort_folder, spikes_df_csv_out_folder, sampling_rate, verbose, operating_system, experiment,
                 chars_condition):
        self.recordings_to_extract = recordings_to_extract
        self.kilosort_folder = kilosort_folder
        self.spikes_df_csv_out_folder = spikes_df_csv_out_folder
        self.sampling_rate = sampling_rate
        self.verbose = verbose
        self.operating_system = operating_system
        self.experiment = experiment
        self.chars_condition = chars_condition
        self.sep = '\\' if self.operating_system == 'win' else '/'

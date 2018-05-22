class Options():

    def __init__(self, recordings_to_extract, kilosort_folder, spikes_df_csv_out_folder,
                 nrn_char_out_fol, sampling_rate, verbose, operating_system, experiment,
                 chars_condition):
        self.recordings_to_extract = recordings_to_extract
        self.kilosort_folder = kilosort_folder
        self.spikes_df_csv_out_folder = spikes_df_csv_out_folder
        self.nrn_char_out_fol = nrn_char_out_fol
        self.sampling_rate = sampling_rate
        self.verbose = verbose
        self.operating_system = operating_system
        self.experiment = experiment
        self.chars_condition = chars_condition
        self.sep = '\\' if self.operating_system == 'win' else '/'

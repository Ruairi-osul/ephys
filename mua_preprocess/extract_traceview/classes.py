class Options:

    def __init__(self, kilosort_folder, recording, chosen_cluster, time_chosen, time_span, operating_system, num_channels, broken_chans, num_spikes_for_averaging, verbose):
        self.kilosort_folder = kilosort_folder
        self.recording = recording
        self.chosen_cluster = chosen_cluster
        self.time_chosen = time_chosen
        self.time_span = time_span
        self.operating_system = operating_system
        self.num_channels = num_channels
        self.broken_chans = broken_chans
        self.num_spikes_for_averaging = num_spikes_for_averaging
        self.verbose = verbose

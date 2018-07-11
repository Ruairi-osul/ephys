class Options:

    def __init__(self, kilosort_folder, recording, chosen_cluster, time_span_chosen, operating_system, num_channels, broken_chans, view_window, num_spikes_for_averaging, color, verbose):
        self.kilosort_folder = kilosort_folder
        self.recording = recording
        self.chosen_cluster = chosen_cluster
        self.time_span_chosen = time_span_chosen
        self.operating_system = operating_system
        self.num_channels = num_channels
        self.view_window = view_window
        self.color = color
        self.broken_chans = broken_chans
        self.num_spikes_for_averaging = num_spikes_for_averaging
        self.verbose = verbose
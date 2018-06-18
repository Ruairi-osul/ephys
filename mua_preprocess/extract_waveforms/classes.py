import numpy as np


class Options:

    def __init__(self, kilosort_folder, recordings_to_analyse, spike_selection_method, num_spikes, num_channels, num_samples, fig_folder, temp_folder, last_spikes, thresh_udu, thresh_du, borken_channels, fs, verbose):
        self.kilosort_folder = kilosort_folder
        self.recordings_to_analyse = recordings_to_analyse
        self.num_spikes = num_spikes
        self.num_channels = num_channels
        self.num_samples = num_samples
        self.fig_folder = fig_folder
        self.temp_folder = temp_folder
        self.last_spikes = last_spikes
        self.fs = fs
        self.thresh_udu = thresh_udu
        self.thesh_du = thresh_du
        self.verbose = verbose
        self.spike_selection_method = spike_selection_method
        self.borken_channels = borken_channels

        self.waveform_window = np.arange(-self.num_samples / 2, num_samples / 2)

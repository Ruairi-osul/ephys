import argparse
import json
import sys
import os
sys.path.append('/home/ruairi/repos')  #path to parent folder to ephys
from ephys.package._classes.options import options_from_args
from ephys.package.IO import mkdir, load_kilosort_arrays


def get_options():
    parser = argparse.ArgumentParser(description= '''Probe preprocessing scipt.
    Given Kilosort-generated arrays, extracts spike times and spike waveforms of 'good' units.''')
    parser.add_argument('-c', '--config_file', required=True,
                        help='path to options configurations [.json] file.')
    parser.add_argument('-u', '--update', help='True if appending to current                                             results file. False [default]                                            to create new files                                                      (deleting previous)',                                                    default=False)
    args = parser.parse_args()
    ops = options_from_args(args)
    return ops

def create_spiketimes_df(recording_dir):
    spike_clusters, spike_times, cluster_groups = load_kilosort_arrays(recording_dir)
    good_cluster_numbers = get_good_cluster_numbers(cluster_groups)
            data = [spike_clusters.flatten(), spike_times.flatten()]



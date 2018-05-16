from pds.pds_funcs import *


def main(ops):
    verbose = ops.verbose
    for recording in ops.recordings_to_extract:
        chans, chan_labels = load_data(ops.source_folder, recording,
                                       sep=ops.sep)
        if verbose:
            print('Loaded:\t{}'.format(recording))
        for ind, chan in enumerate(chans):
            raw_data = chan['data']
            label = chan_labels[ind]
            data = butter_lowpass_filter(data=raw_data,
                                         low_cutoff=ops.low_cutoff_lpf,
                                         fs=ops.fs)
            data = downsample(data=data,
                              fs=ops.fs,
                              new_fs=ops.new_fs)
            df = bin_psd_combine(data, ops.new_fs,
                                 secs_per_bin=4)
            save(recording=recording,
                 chan_lab=label,
                 df=df,
                 out_folder=ops.out_folder,
                 sep=ops.sep,
                 verbose=True)

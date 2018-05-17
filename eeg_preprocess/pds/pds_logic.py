from pds.pds_funcs import *


def main(ops):
    verbose = ops.verbose
    for recording in ops.recordings_to_extract:
        if verbose:
            print('Loading:\t{}'.format(recording))
        chans, chan_labels = load_data(ops.source_folder, recording,
                                       sep=ops.sep)

        for ind, chan in enumerate(chans):
            raw_data = chan['data']
            label = chan_labels[ind]

            if ops.downsample_method == 'fourier':
                data = downsample_fourier(data=raw_data,
                                          fs=ops.fs,
                                          new_fs=ops.new_fs)
            else:
                data = downsample_decimate(data=raw_data)

            data = butter_lowpass_filter(data=data,
                                         low_cutoff=ops.low_cutoff_lpf,
                                         fs=ops.new_fs)
            if ops.spectrum_method == 'default':
                df = compute_spectrum(data=data,
                                      new_fs=ops.new_fs,
                                      noverlap=ops.noverlap,
                                      secs_per_bin=ops.secs_per_bin,
                                      verbose=ops.verbose)
            elif ops.spectrum_method == 'welch':
                print('Not yet coded')

            save(recording=recording,
                 chan_lab=label,
                 df=df,
                 out_folder=ops.out_folder,
                 sep=ops.sep,
                 verbose=True)

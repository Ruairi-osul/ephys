from pds.pds_funcs import *


def main(ops):
    verbose = ops.verbose
    for recording in ops.recordings_to_extract:
        array_list = []
        lab_list = []
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
            if ops.lpf:
                data = butter_lowpass_filter(data=data,
                                             low_cutoff=ops.low_cutoff_lpf,
                                             fs=ops.new_fs)

            df = compute_spectrum(data=data,
                                  new_fs=ops.new_fs,
                                  noverlap=ops.noverlap,
                                  secs_per_bin=ops.secs_per_bin,
                                  verbose=ops.verbose)

            save(recording=recording,
                 chan_lab=label,
                 df=df,
                 out_folder=ops.out_folder,
                 sep=ops.sep,
                 verbose=ops.verbose)

            lab_list.append(label.split('.')[0][-4:])
            array_list.append(data)

        write_eeg_files(a_list=array_list,
                        lab_list=lab_list,
                        eeg_numpy_folder=ops.eeg_numpy_folder,
                        recording=recording)

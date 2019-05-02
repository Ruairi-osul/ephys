import argparse


def _get_options():
    parser = argparse.ArgumentParser(
        description='')

    parser.add_argument('-', '--', required=False,
                        help='')

    parser.add_argument('-', '--', required=,
                        help='')
    return parser.parse_args()


def get_waveforms(spike_data, rd):
    '''Given a pandas df of spike times and the path to
    a the parent directory of the .dat file containing the raw
    data for that recording, extracts waveforms for each cluester
    and the channel on which that cluster had the highest amplitude

    params:
        spike_data: pandas df of spike times and cluster ids as cols
        rid
    '''
    raw_data = _load_dat_data(p=os.path.join(
        rd, os.path.basename(rd)) + '.dat')
    f1 = partial(_extract_waveforms, raw_data=raw_data, ret='data')
    f2 = partial(_extract_waveforms, raw_data=raw_data, ret='')
    waveforms = spike_data.groupby('cluster_id')['spike_times'].apply(
        f1, raw_data=raw_data).apply(pd.Series).reset_index()
    chans = spike_data.groupby('cluster_id')[
        'spike_times'].apply(f2,
                             raw_data=raw_data).apply(pd.Series).reset_index()
    chans.columns = ['cluster_id', 'channel']
    waveforms.columns = ['cluster_id', 'sample', 'value']
    return waveforms, chans


def _extract_waveforms(spk_tms, raw_data, ret='data',
                       n_spks=800, n_samps=240, n_chans=32):
    assert len(spk_tms) > n_spks, 'Not ennough spikes'
    spk_tms = spk_tms.values
    window = np.arange(int(-n_samps / 2), int(n_samps / 2))
    wvfrms = np.zeros((n_spks, n_samps, n_chans))
    for i in range(n_spks):
        srt = int(spk_tms[i] + window[0])
        end = int(spk_tms[i] + window[-1] + 1)
        srt = srt if srt > 0 else 0
        try:
            wvfrms[i, :, :] = raw_data[srt:end, :]
        except ValueError:
            filler = np.empty((n_samps, n_chans))
            filler[:] = np.nan
            wvfrms[i, :, :] = filler
    wvfrms = pd.DataFrame(np.nanmean(wvfrms, axis=0),
                          columns=range(1, n_chans + 1))
    norm = wvfrms - np.mean(wvfrms)
    tmp = norm.apply(np.min, axis=0)
    good_chan = tmp.idxmin()
    wvfrms = wvfrms.loc[:, good_chan]
    if ret == 'data':
        return wvfrms
    else:
        return good_chan


def main():
    pass


if __name__ == "__main__":
    main()

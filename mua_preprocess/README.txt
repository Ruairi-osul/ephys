Scrips in this directory are for preprocessing of MUA data

TO DO:
    Set up bash script to run preprocessing in order

Run scripts in this order:
    pack_to_dat:
        create binary .dat file for kilosort/phy spike sorting

    **** Spike sort with kilosort/phy ****

    extract_neuron_chars
        create csv file containing one row per spike with information regarding the identity of the responsible neuron (only neurons marked as 'good' during spike sorting)

    ectract_waveforms
        extract waveforms and calculate average waveform for all good neurons. Caculates spike width statistics and saves to temperary csv file. Creates waveform figures.

    spiking_statistics
        calculates spiking statistics for all neurons marked as good during spike sorting. Saves results in temperary csv file.

    merge_data
        merge the two temperary files created by extract_waveforms and spiking_statistics into one file containing all spiking information.

    add+groups

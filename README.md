# ephys
Set up for code sharing between sharplab, Oxford and the lab of Dr Kongfatt Wong-Lin, Ulster University

Contains code scripts for preprocessing and analysis of EEG and silicon probe data.

Ruairi O'Sullivan and Tran Tran 2018

## How to run the python code

### Dependencies: 
Requires libraries associated with an anaconda python install: https://conda.io/docs/user-guide/install/download.html

Some scripts also require the Neo and Elephant libraries http://neuralensemble.org/NeuroTools/


### Steps to run a scipt
  - Clone the repository and install anaconda / other packages ('pip install neo' and 'pip install elephant' at the command line)
  - Find the script you would like to run and open its associated \*_\_config.py*_ in a text editor
  - Edit the parameters of the Options object
  - Save and run the config file at the command line

## Directories

Note: Some scripts in analysis directories are dependant on intemetiary .csv files created by the preprocessessing scripts. Make sure to read the README inside each directory.

### mua_preprocess
Contains scirpts for converting raw data (saved in .dat format) and files created during manual spike sorting in phy into meaningful .csv files. Also extracts characteristics of clusters marked as single units such during spike sorting. Creates some plots of neuron waveforms, spiking activity over time.

### mua_analysis
Create plots of the raw trace of individual neurons over time. Plot the activity of many neurons at once in a neuron heatmap. Use labels to separate the neurons into groups.

### eeg_preprocess
A work in progress. Currently contains scripts for some preprocessing of raw EEG data stored in .continuous files.

### eeg_analysis
Plot spectrograms, mean power density plots etc. 


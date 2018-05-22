# ephys
Set up for code sharing between sharplab, Oxford and the lab of Dr Kongfatt Wong-Lin, Ulster University

Contains code scripts for preprocessing and analysis of EEG and silicon probe data.

Ruairi O'Sullivan and Tran Tran 2018

## How to run the python code
Requires libraries associated with an anaconda python install: https://conda.io/docs/user-guide/install/download.html

  - Clone the repository and install anaconda
  - Find the script you would like to run and open its associated \*_config.py*_ in a text editor
  - Edit the parameters in the options file
  - Save and run the config file at the command line

## Directories

### eeg_preprocess
scirpts for reading raw EEG data stored in .continuous files and creating spectrogram data stored in .csv files

### mua_preprocess
scirpts for reading raw EEG data stored in .continuous files, applying filters and writing to a .dat file

### post_kilosort
read output of kilosort into tidy .csv files. Extract characteristics of good clusters and describe their firing patterns

### eeg_analysis
Plot spectrograms, mean power density plots etc. 


import os
from visbrain import Sleep
from glob import glob
import numpy as np

fs = 250

source_dir = r'C:\Users\Rory\raw_data\CIT_WAY\eeg_numpy\CIT_WAY_1_2018-05-01_15-59-19_PRE'
data = np.load(glob(os.path.join(source_dir, '*.npy'))[0])
path_to_txt = glob(os.path.join(source_dir, '*.txt'))[0]
with open(path_to_txt) as f:
    labs = np.array(f.read().splitlines())

Sleep(data=data, sf=fs, channels=labs).show()

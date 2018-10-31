from elephant.statistics import instantaneous_rate
from quantities import s
from utils import chunks
from functools import partial


def ifr(st_list):
    return list(map(partial(instantaneous_rate, sampling_period=s), st_list))


def ifr2(st_list, chunk_size=4):
    '''convert a list of neo spike trains for a list of neo analog
    signals of instantaneous firing rate sampled every 60 seconds.
    chunk size is for computational lag'''
    out = []
    for seg in chunks(st_list, chunk_size):
        out.append(
            list(map(partial(instantaneous_rate,
                             sampling_period=120 * s),
                     st_list)))
    return [item for sublist in out for item in sublist]

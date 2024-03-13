from pathlib import Path
from itertools import count
import pickle
import re

import pandas as pd


def get_saving_filename_safely(save_filedir):
    """find available filename iteratively.

    if example.pkl exists, then return example-2.pkl.
    if example-2.pkl exists, then return example-3.pkl.
    must be saved with '.pkl' extension."""
    # force .pkl extension
    save_filedir = Path(save_filedir)
    assert save_filedir.name.endswith('.pkl'), 'savefile name must be .pkl file.'

    # try to find available filename iteratively. (like asdf.txt, asdf-1.txt, asdf-2.txt, ...)
    if re.findall(r".+-(\d+)\.pkl", save_filedir.name):
        current_num = re.findall(r".+-(\d+)\.pkl", save_filedir.name)[0]
        counter = count(current_num + 1)
    else:
        counter = count(2)  # increasing integer generator from 2
    while Path(save_filedir).exists():
        s = re.sub(r"(-\d+)?\.pkl", "", save_filedir.name)
        s = f"{s}-{next(counter)}.pkl"
        save_filedir = save_filedir.parent / s
    return save_filedir


def pickle_bobj(bobj, save_filedir):
    """bobj means binary object"""
    with open(save_filedir, 'wb') as f:
        pickle.dump(bobj, f)


def load_bobj(save_filedir):
    with open(save_filedir, 'rb') as f:
        bobj = pickle.load(f)
    return bobj


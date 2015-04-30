""" Generate some data
"""

import numpy as np
import h5py

FILE = "sample.hd5"
GROUP0 = "/1/2"
GROUP1 = "/A/B/C/D"


x = np.random.random(100);
fh = h5py.File(FILE)
dset = fh.create_dataset("sample0", data=x)
grp0 = fh.create_group(GROUP0)
grp1 = fh.create_group(GROUP1)
grp0.create_dataset("sample1", data=x)
grp1.create_dataset("sample2", data=x)
fh.flush()
fh.close()

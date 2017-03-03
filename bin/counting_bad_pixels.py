# trying to count the non-zero entries in the pixel mask

import dataHandler as dh
import numpy as np

f = "/home/rosem/workspace/diffraction_p06_start/test_data/run_16538_master.h5"
p = "entry/instrument/detector/detectorSpecific/pixel_mask"
# f = "/home/rosem/workspace/diffraction_p06_start/test_data/run_16538_data_000012.h5"
# p = "/entry/data/data"

fhandle = dh.DataHandler()
data = fhandle.create_reader(f,p)

for d in data:
    pass

mask = np.invert(d.array().astype(bool))


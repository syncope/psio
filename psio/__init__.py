try:
    import h5py
except ImportError("h5py is not installed. Please install for full functionality in reading hdf5 data files."):
    pass

try:
    import six
except ImportError("six is not installed. The package will probably not work without it."):
    pass

try:
    import fabio
except ImportError("fabio is not installed. Several file types will not be supported."):
    pass

try:
    import numpy
except ImportError("numpy is not installed. The package will not work without it."):
    pass

try:
    import pyqtgraph
except ImportError("pyqtgraph is not installed. No display will be available."):
    pass

from .dataHandler import DataHandler
from .hdf5Output import HDF5Output

__version__ = "0.2.0"

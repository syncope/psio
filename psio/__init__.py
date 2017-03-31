try:
    import h5py
except ImportError("h5py is not installed. Please install for full functionality."):
    pass

try:
    import six
except ImportError("six is not installed. The package will not work without it."):
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
    import pni.io.nx.h5
except ImportError("pni nexus handler is not installed. The package will not fully work without it."):
    pass

try:
    import re
except ImportError("re is not installed. PSIO will not fully work without it."):
    pass

try:
    import pyqtgraph
except ImportError("pyqtgraph is not installed. No display will be available."):
   pass

====
PSIO
====

Photon Science Input Output
---------------------------

A simple wrapper library that allows unified read access to most common data formats in use at X ray synchrotron facilities.
In it's most simple form it simple delivers an iterator to the data numpy array(s) for the given files.
This interface is very similar to reading of standard files in Python.
For container data (e.g. hdf5) random access ("indexing") is possible.

Internally it uses several existing libraries: 
   h5py, python-pni (by E. Wintersberger, DESY) and fabio (by J.Kieffer, ESRF).
Inclusion of fio files and plain numpy array files is in progress.

For data storage solely hdf5 is used.

A simple graphical data viewer is also included.

In order to use the full functionality, the following requirements need to be met:
numpy
six
abc
h5py
fabio
pyqtgraph
re
pni
unittest

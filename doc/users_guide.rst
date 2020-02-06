Users Guide
===========

Overview
------------

This user guide describes how to use the psio library.

In a nutshell the library is an utility to facilitate and unify access to persistent data.
Regardless of the actual underlying data format, the interface remains the same.

It builds heavily on a number of other libraries:
  * numpy (mostly arrays)
  * h5py
  * fabio by J. Kieffer et al., ESRF
  
Core data format
----------------

The common data format that is handled in each transaction is the numpy array.
If data is read or written, this is the type on the user end.

In case of additional information data is usually represented as dictionary.
Please refer to the specific documentation of the functions.

Using the library: Reading data
-------------------------------

The first most important part of the library: reading in data.
In order to use it, the module needs to be in the current Python path; then include the line

.. code-block:: python
    
    import dataHandler

The usage of the reading capabilities is intended to be similar to standard file input in Python.
First create an instance of a DataHandler object.
Files to be read can be supplied either as a list or a string:

.. code-block:: python

    DataHandler TiffReader()
    filenames = ['001.tif', '002.tif', '003.tif']
    
    images = TiffReader(filenames)

The images are then an iterator over the supplied files and the respective images in the files.
One can directly iterate over the images, where the individual elements are numpy arrays:

.. code-block:: python

    for image in images:
        doSomething(image)

In case of binary image files, usually indicated by suffices like .tif, .cbf, .edf, etc., the fabio library is used to read the data.
The assumption is that the data is single data per file; multi-tif is not supported.

In case of reading hdf5 or NeXus data, the h5py library is used.
This is inherently assumed to be multiple data.
The iteration is therefore such, that first all data from the current file is issued.
Then the next file is iterated over, until all data in all files is exhausted.
Due to the different structure, for hdf5/NeXus data a path must be given:

.. code-block:: python

    DataHandler NexusReader()
    filenames = ['001.ndf', '002.ndf', '003.ndf']
    
    path = "/entry/instrument/pilatus/data"

    data = NexusReader(filenames, path)
 
    for image in data:
        calculateFunction(image)

In addition to this, random access of individual images/data elements in a hdf5/NeXus file is possible.

.. code-block:: python

    DataHandler NexusReader()
    filenames = ['001.ndf', '002.ndf', '003.ndf']
    
    path = "/entry/instrument/pilatus/data"

    data = NexusReader(filenames, path)
    
    imageA = data[23]



Using the library: Writing data
-------------------------------

The output format for data is hdf5.
It is emulated to be NeXus - like, that is the names, attributes and structure are identical to NeXus.

The first step is as usual the module import:

.. code-block:: python
    
    import HDF5Output

Please confirm the NeXus manual for more details, but in short a NeXus file is organized similar to a file system.
There are directories (named groups) and files (named fields).
Fields are numpy arrays, whereas groups can be either without a parent (the root group) or have a parent, allowing arbitrary nesting.

Fields and groups can have attributes, which can be thought of as dictionaries.
For the wrapper code here, string attributes are called comments, whereas numerical attributes retain the name.

A full example showing all capabilities is:

.. code-block:: python

    import numpy as np
    import HDF5Output

    # create the output object with a name, and overwrite any existing file with the same name
    no = HDF5Output("output.h5", recreate=True)
    
    # add some fields, the first will store several images of size 2x2, the second only one image
    no.addField("firstField", (0, 2, 2))
    no.addField("secondField", (2, 2))
    
    # add a string attribute to the first field, and a numerical one to the second
    no.addCommentToField("firstField", "comment","collection of matrices")
    no.addAttributeToField("secondField", "average_number", 42.)

    # now store some data into these fields
    d = np.array([1, 2, 3, 4])

    # in case of a stack of data, the command reads like
    no.addDataToField("firstField", d)
    
    # for single 2D data the command is
    no.addSingleImageToField("secondField", d)

    # at the end it's good practice to close the file
    no.close()

Please note the difference between single element (image) data to multiple element data.
In order to make the difference between e.g. 3D data and a stack of 2D data more prominent this option has been made explicit.


.. toctree::
    :maxdepth: 2 
   

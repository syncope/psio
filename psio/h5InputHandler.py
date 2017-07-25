# Copyright (C) 2016-17  Christoph Rosemann, DESY, Notkestr. 85, D-22607 Hamburg
# email contact: christoph.rosemann@desy.de
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation in  version 2
# of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA  02110-1301, USA.


'''Implementation for handling files based on HDF5 file format.
   For more information on HDF5 and Python visit http://www.h5py.org/'''


import h5py
from . import inputHandler


class H5InputHandler(inputHandler.InputHandler):

    '''This is the implementation of the InputHandler for NeXus.'''

    def __init__(self):
        '''The constructor defines an empty set of member variables.'''
        self._fileList = None
        self._fileIter = None
        self._dataset = None
        self._dataIter = None
        self._nentries = None
        self._attribute = None
        self._singleValue = False
        self._currentFile = None
        self._imageDataDimension = 2

    def inputList(self, filenames, path, attribute):
        '''Creates the iterator object from the given list of files.

            :param filenames: the list of file names
            :param path: the location of the data element
            :param attribute: optional, if an attribute is to be accessed
            :type filenames: list of str
            :type path: str
            :type attribute: str'''
        self._fileList = filenames
        self._fileIter = iter(self._fileList)
        self._dataset = path
        self._attribute = attribute

    def __iter__(self):
        '''Implementation of the iterator protocol, part I.'''
        return self

    def __next__(self):
        '''The second part for the iterator implementation.'''
        # There are two iterations:
        #  (1) the outer iteration over the files
        #  (2) the inner over the data within the file

        # two cases: no file open -> None, then advance to next in list
        # - h5py doesn't supply info the file, therefore act only
        #   if there isn't a file
        if(self._currentFile is None):
            self.advanceFile()

        try:
            # the actual data fetch command, read:
            #  1) fetch the numpy array/object
            #  2) from the data object residing at the given path
            #  3) and the element that the current iterator points to
            currentField = self._currentFile.get(self._dataset)

            if(self._attribute is None and self._singleValue is False):

                if(len(currentField.shape) == self._imageDataDimension):
                    self._singleValue = True
                    self._ddata = currentField
                    return self._ddata
                elif(len(currentField.shape) != (self._imageDataDimension + 1)):
                    raise ValueError(
                        "The dimension of the data is not correct.")
                if(inputHandler.six.PY2):
                    self._ddata = currentField[self._dataIter.next()]
                else:
                    self._ddata = currentField[self._dataIter.__next__()]
            else:
                # in case of attribute read it once, then skip
                try:
                    if(self._singleValue is False):
                        self._ddata = currentField.attrs.get(self._attribute)
                        self._singleValue = True
                        return self._ddata
                    else:
                        raise StopIteration
                except KeyError:
                    self._ddata = None
                    print("Attribute", self._attribute, "doesn't exist.")

        except StopIteration:
            self._currentFile.close()
            self._currentFile = None
            self.__next__()

        except IOError:
            self._ddata = None
        return self._ddata

    def _nextFile(self):
        '''Helper function to navigate through a list of files.'''

        self._singleValue = False
        if(inputHandler.six.PY2):
            self._currentFile = h5py.File(self._fileIter.next(), "r")
        else:
            self._currentFile = h5py.File(self._fileIter.__next__(), "r")
        # by convention the first entry in the stored data
        # is always the number of elements
        try:
            self._nentries = self._currentFile.get(self._dataset).shape[0]
            # create an iterator for the elements
        except(AttributeError):
            self._nentries = -1
        self._dataIter = iter(range(self._nentries))

    if(inputHandler.six.PY2):
        def next(self):
            '''Specific syntax for Python2.x since the call syntax of the iterator is different.'''

            return self.__next__()

    def getNumberOfEntries(self):
        '''Helper function to obtain the number of elements to be processed.

            :return: number of entries'''

        return self._nentries

    def getEntry(self, entrynumber):
        '''Random access to the specified element.

            :param entrynumber: the index of the element
            :type entrynumber: int
            :return: a data element, numpy array
            :raises: IndexError if given element cannot be found'''

        if(self._currentFile is None):
            self.advanceFile()
        if(entrynumber >= self._nentries):
            raise IndexError(
                "There are only " +
                repr(
                    self._nentries) +
                " elements in the current file; requested was " +
                repr(
                    entrynumber) +
                ".")
        try:
            # access the current dataset
            currentField = self._currentFile.get(self._dataset)
            return currentField[entrynumber]
        except:
            print("An exception occurred while trying to access the data.")

    def advanceFile(self):
        # advance the file iterator
        self._nextFile()

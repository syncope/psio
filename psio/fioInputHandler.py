# Copyright (C) 2019  Christoph Rosemann, DESY, Notkestr. 85, D-22607 Hamburg
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


'''Implementation for handling fio files.'''


from . import fioFileReader
from . import inputHandler


class fioInputHandler(inputHandler.InputHandler):

    '''This is the implementation of the InputHandler for FIO files.'''

    def __init__(self):
        '''The constructor defines an empty set of member variables.'''
        self._fileList = files
        # abuse the attribute for now -- use as marker for start and end position
        self._reader = None
        self._currentFile = None
        self._currentData = None

        if(files is not None):
            self._fileIter = iter(files)

    def inputList(self, filenames, path, attribute=None):
        '''Creates the iterator object from the given list of files.

            :param filenames: the list of file names
            :param path: the location of the data element
            :param attribute: optional, if an attribute is to be accessed
            :type filenames: list of str
            :type path: str
            :type attribute: str'''
        self._fileList = filenames
        self._fileIter = iter(self._fileList)

    def __iter__(self):
        '''Implementation of the iterator protocol, part I.'''
        return self

    def __next__(self):
        '''The second part for the iterator implementation.'''
        # There are two iterations:
        #  (1) the outer iteration over the files
        #  (2) the inner over the data within the file

        # two cases: no file open -> None, then advance to next in list
        if(self._currentFile is None):
            self.advanceFile()

        try:
            # the actual data fetch command, read:
            #  1) fetch the numpy array/object
            #  2) from the data object residing at the given path
            #  3) and the element that the current iterator points to
            if(inputHandler.six.PY2):
                return self._dataIter.next()
            else:
                return self._dataIter.__next__()

        except StopIteration:
            self._currentFile.close()
            self._currentFile = None
            self.__next__()

    if(inputHandler.six.PY2):
        def next(self):
            '''Specific syntax for Python2.x since the call syntax of the iterator is different.'''

            return self.__next__()
 
    def getTotalNumberOfEntries(self):
        '''Helper function to obtain the number of elements to be processed.

            :return: number of entries'''
        # simple with FIO files: one scan per file
        return len(self._fileList)

    def getEntry(self, entrynumber):
        '''Random access to the specified element.

            :param entrynumber: the index of the element
            :type entrynumber: int
            :return: a data element
            :raises: IndexError if given element cannot be found'''

        if(self._currentFile is None):
            self.advanceFile()
            self.indexData()
        try:
            return self._indexedData[entrynumber]
        except KeyError:
            raise KeyError("[FioInputHandler::FioFileReader::getEntry] Entry of index " + repr(entrynumber) + " does not exist.")

    def advanceFile(self):
        # advance the file iterator
        self._nextFile()
    
    def _nextFile(self):
        '''Helper function to navigate through a list of files.'''

        # directly use an instance of the spec file reader
        if(inputHandler.six.PY2):
            self._currentFile = fioFileReader.FioFileReader(self._fileIter.next())
        else:
            self._currentFile = fioFileReader.FioFileReader(self._fileIter.__next__())

        # unusual approach: read all data first into memory!
        self._currentData = self._currentFile.read()

        try:
            self._nentries = len(self._currentData)

        # create an iterator for the elements
        except(AttributeError):
            self._nentries = -1
        self._dataIter = iter(self._currentData)

    def indexData(self):
        # with spec files there is distinct possibility to contain empty scans
        # so create a dictionary that maps indeces to scanData elements
        self._indexedData = {scan.getScanNumber(): scan for scan in self._currentData}

    def getAll(self, scanlist=None):
        returnObject = []
        for f in self._fileList:
            returnObject += fioFileReader.fioFileReader(f).read(scanlist)
        return returnObject

# Copyright (C) 2016  Christoph Rosemann, DESY, Notkestr. 85, D-22607 Hamburg
# email contact: christoph.rosemann@desy.de
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation in version 2
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

'''This is the test for the h5py input module.'''

import unittest
import h5InputHandler


class TestH5InputHandler(unittest.TestCase):

    def setUp(self):
        self.ih1 = h5InputHandler.H5InputHandler()
        self.ih2 = h5InputHandler.H5InputHandler()
        self.ih3 = h5InputHandler.H5InputHandler()

    def test_constructor(self):
        self.assertIsNone(self.ih1._fileList)
        self.assertIsNone(self.ih1._fileIter)
        self.assertIsNone(self.ih1._field)
        self.assertIsNone(self.ih1._dataIter)
        self.assertIsNone(self.ih1._nentries)
        self.assertIsNone(self.ih1._attribute)
        self.assertFalse(self.ih1._singleValue)
        self.assertIsNone(self.ih1._currentFile)
        self.assertEqual(self.ih1._dataDimension, 2)

    def test_listInput(self):
        pass

    def test_setDimension(self):
        pass

    def test_nextFile(self):
        pass

    def test_nofEntries(self):
        pass


if __name__ == '__main__':
    unittest.main()


    #~ def inputList(self, filenames, path, attribute):
        #~ '''Pass the list of files that are to be opened.'''
        #~ self._fileList = filenames
        #~ self._fileIter = iter(self._fileList)
        #~ self._field = path
        #~ self._attribute = attribute
#~ 
    #~ def setDimension(self, dimension):
        #~ self._dataDimension = dimension
#~ 
    #~ def __iter__(self):
        #~ '''Implementation of the iterator protocol, part I.'''
        #~ return self
#~ 
    #~ def __next__(self):
        #~ '''The second part for the implementation of the iterator.'''
        #~ # There are two iterations:
        #~ #  (1) the outer iteration over the files
        #~ #  (2) the inner over the data within the file
#~ 
        #~ # two cases: no file open -> None, then advance to next in list
        #~ # - h5py doesn't supply info the file, therefore act only
        #~ #   if there isn't a file
        #~ if(self._currentFile is None):
            #~ # advance the file iterator
            #~ self._nextFile()
#~ 
        #~ try:
            #~ # the actual data fetch command, read:
            #~ #  1) fetch the numpy array/object
            #~ #  2) from the data object residing at the given path
            #~ #  3) and the element that the current iterator points to
            #~ currentField = self._currentFile.get(self._field)
            #~ 
            #~ if(self._attribute is None and self._singleValue is False):
                #~ if(len(currentField.shape) == self._dataDimension):
                    #~ self._singleValue = True
                    #~ self._ddata = currentField
                    #~ return self._ddata
                #~ elif(len(currentField.shape) != (self._dataDimension + 1)):
                    #~ raise ValueError("The dimension of the data is not correct.")
                #~ if(inputHandler.six.PY2):
                    #~ self._ddata = currentField[self._dataIter.next()]
                #~ else:
                    #~ self._ddata = currentField[self._dataIter.__next__()]
            #~ else:
                #~ # in case of attribute read it once, then skip
                #~ try:
                    #~ if(self._singleValue is False):
                        #~ self._ddata = currentField.attrs.get(self._attribute)
                        #~ self._singleValue = True
                        #~ return self._ddata
                    #~ else:
                        #~ raise StopIteration
                #~ except KeyError:
                    #~ self._ddata = None
                    #~ print("Attribute", self._attribute, "doesn't exist.")
#~ 
        #~ except StopIteration:
            #~ self._currentFile.close()
            #~ self._currentFile = None
            #~ self.__next__()
#~ 
        #~ except IOError:
            #~ self._ddata = None
        #~ return self._ddata
        #~ 
    #~ def _nextFile(self):
        #~ self._singleValue = False
        #~ if(inputHandler.six.PY2):
            #~ self._currentFile = h5py.File(self._fileIter.next(), "r")
        #~ else:
            #~ self._currentFile = h5py.File(self._fileIter.__next__(), "r")
        #~ # by convention the first entry in the stored data
        #~ # is always the number of elements
        #~ try:
            #~ self._nentries = self._currentFile.get(self._field).shape[0]
            #~ # create an iterator for the elements
        #~ except(AttributeError):
            #~ self._nentries = 1
        #~ self._dataIter = iter(range(self._nentries))        
#~ 
    #~ if(inputHandler.six.PY2):
        #~ def next(self):
            #~ return self.__next__()
#~ 
    #~ def getNumberOfEntries(self):
        #~ return self._nentries



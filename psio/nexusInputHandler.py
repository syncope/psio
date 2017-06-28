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


'''Implementation for handling files based on NeXus file format.
For more information on NeXus visit www.nexusformat.org'''


import pni.io.nx.h5 as nexus
import inputHandler


class NexusInputHandler(inputHandler.InputHandler):

    '''This is the implementation of the InputHandler for NeXus.'''

    def __init__(self):
        '''The constructor defines an empty set of member variables.'''
        self._fileList = None
        self._fileIter = None
        self._field = None
        self._dataIter = None
        self._nentries = None
        self._attribute = None
        self._attributeRead = True
        self._currentFile = nexus.nxfile()
        self._imageDataDimension = 2

    def inputList(self, filenames, path, attribute):
        '''Pass the list of files and path that are to be opened.'''
        self._fileList = filenames
        self._fileIter = iter(self._fileList)
        self._field = path
        self._attribute = attribute

    def __iter__(self):
        '''Implementation of the iterator protocol, part I.'''
        return self

    def __next__(self):
        '''The second part for the implementation of the iterator.'''
        # There are two iterations:
        #  (1) the outer iteration over the files
        #  (2) the inner over the data within the file
        try:
            # the first setting of the f: test if the file is open ('valid')
            if(not(self._currentFile.is_valid)):
                # if not, then open the next file in the list
                self._nextFile()
            try:
                # now return the data object, constructed from
                # the current data field element, as given by the iterator
                # or just the attribute
                if(self._attribute is None):
                    if(inputHandler.six.PY2):
                        self._ddata = self._dat[self._dataIter.next(), ...]
                    else:
                        self._ddata = self._dat[self._dataIter.__next__(), ...]
                else:
                    # in case of attribute read it once, then skip
                    try:
                        if(self._attributeRead):
                            # first pick field/group/element:
                            obj = nexus.get_object(
                                self._currentRoot,
                                self._field)
                            self._ddata = obj.attributes[
                                self._attribute].read()
                            self._attributeRead = False
                            return self._ddata
                        else:
                            raise StopIteration
                    except KeyError:
                        self._ddata = None
                        print("Attribute", self._attribute, "doesn't exist.")
            except StopIteration:
                # if this loop has ended, advance the file iterator
                self._currentFile.close()
                # and call the function in recursion
                self.__next__()

        except IOError:
            return self._ddata

    def _nextFile(self):
        self._attributeRead = True
        if(inputHandler.six.PY2):
            self._currentFile = nexus.open_file(
                self._fileIter.next(),
                readonly=True)
        else:
            self._currentFile = nexus.open_file(
                self._fileIter.__next__(),
                readonly=True)
        # nexus code -> first get the root of the file
        self._currentRoot = self._currentFile.root()
        if(self._field is not None):
            self._dat = nexus.get_object(self._currentRoot, self._field)
            try:
                self._nentries = self._dat.shape[0]
            except(AttributeError):
                self._nentries = 1
            # finally create an integer based iterator for the data
            # by convention (!) the first entry is the number of elements
            self._dataIter = iter(range(self._nentries))
        else:
            self._dat = self._currentRoot

    if(inputHandler.six.PY2):
        def next(self):
            return self.__next__()

if __name__ == "__main__":
    files = ["test/test_data/lambda750ksi/Calli_align_00004.ndf"]
    path = "/entry/instrument/detector/data"
    attribute = None

    io = NexusInputHandler()
    io.inputList(files, path, attribute)

    for i in io:
        print(i)
        if(inputHandler.six.PY2):
            c = raw_input('please press enter first.\n')
        else:
            c = input('please press enter first.\n')
    if(inputHandler.six.PY2):
        c = raw_input('please press enter 2nd time.\n')
    else:
        c = input('please press enter 2nd time.\n')

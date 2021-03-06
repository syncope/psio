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


'''The data handler is the central object for data access.
   It abstracts data access on two levels.
   The usage pattern is straightforward:
   - a single file name or a list of filenames is passed
   - an iterator over all data in that files is returned.'''


from . import inputHandlerFactory


class DataHandler():

    def __init__(self, filenames=None, path=None, attribute=None, typehint=None):
        '''The constructor instantiates a factory.'''
        self.readerFactory = inputHandlerFactory.InputHandlerFactory()
        self.fileHandler = None
        if filenames is not None:
            self._create_reader(filenames, path, attribute, typehint)

    def _create_reader(self, filenames, path=None, attribute=None, typehint=None):
        '''Creates a file reader object. First argument has to be either
           a single filename or a list of filenames.
           Second argument is only needed for path in NeXus/hdf5 files.

           :param filenames: a single or more file name/s (as a list)
           :param path: (optional) the location inside a hdf5 file
           :param attribute: (optional) the name of an attribute in a hdf5 file
           :type filenames: str or list of str
           :type path: str
           :type attribute: str
           :raises: IOError if file(s) cannot be opened
           :raises: TypeError if file type is unkown or cannot be recognized
           :return: iterable DataHandler instance object'''
        if(not isinstance(filenames, list)):
            filenames = [filenames]
        try:
            self.fileHandler = self.readerFactory.create(
                filenames, path=path, attribute=attribute, typehint=typehint)
            self.fileHandler.inputList(filenames, path, attribute)
        except IOError:
            print("Error opening the file, bailing out.")
        except TypeError:
            print("Wrong type for creating a reader, will not work.")
        return

    def __next__(self):
        return self.fileHandler.__next__()

    def __iter__(self):
        return self.fileHandler

    def getTotalNumberOfEntries(self):
        return self.fileHandler.getTotalNumberOfEntries()

    def getEntry(self, index):
        return self.fileHandler.getEntry(index)

    def getFileHandler(self):
        return self.fileHandler

    def getAll(self):
        return self.fileHandler.getAll()

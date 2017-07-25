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


'''The data  handler is the central object for the user.
It abstracts data access on two levels.
The usage pattern is straightforward:
 - a list (!) of filenames is passed
 - an iterator over all data in that files is returned.'''

from . import inputHandlerFactory


class DataHandler():

    def __init__(self, filenames=None, path=None, attribute=None):
        '''The constructor instantiates a factory.'''
        self.readerFactory = inputHandlerFactory.InputHandlerFactory()
        self.fileHandler = None
        if filenames is not None:
            self.create_reader(filenames, path, attribute)

    def create_reader(self, filenames, path=None, attribute=None):
        '''Creates a file reader object. First argument has to be either
           a single filename or a list of filenames.
           Second argument is only needed for path in NeXus/hdf5 files.'''
        if(not isinstance(filenames, list)):
            filenames = [filenames]
        try:
            self.fileHandler = self.readerFactory.create(
                filenames, path, attribute)
            self.fileHandler.inputList(filenames, path, attribute)
        except IOError:
            print("Error opening the file, bailing out.")
        except TypeError:
            print ("Wrong type for creating a reader, will not work.")
        return self.fileHandler

    def __next__(self):
        return self.fileHandler.__next__()

    def __iter__(self):
        return self.fileHandler

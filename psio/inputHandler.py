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

'''Abstract interface class for reading data.
   These functions are used in the also abstract data handler class.'''

# compatibility stuff:
import six  # compatibility to make it work under python 2.7


class InputHandler():
    # std::py3 is:  class InputHandler(metaclass=ABCMeta):

    def inputList(self, files, path, attribute):
        '''Creates the iterator object on the given item.

            :param files: a list of files
            :param path: optional string for hdf5 data files
            :param attribute: optional string for hdf5 data files
            :type files: list of str
            :type path: str
            :type attribute: str
            :return: InputHandler object instance'''
        pass

    def __next__(self):
        '''Implements the iteator protocol for the call of the next element.

            :raises: StopIteration at the end of the sequence'''
        pass

    def __iter__(self):
        '''Returns the InputHandler object instance as part of the iterator protocol.'''
        pass

    def getTotalNumberOfEntries(self):
        '''Calculates the total number of entries for the given files.'''
        pass

    def getEntry(self, index):
        '''If case of a multi-image file, the entry at the given index is returned.'''
        pass

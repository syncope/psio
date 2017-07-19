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

'''This is the abstract class for reading data.
There are no implemented functions, just the interface.
These functions are used in the abstract data handler class.'''

# compatibility stuff:
import six  # compatibility to make it work under python 2.7


class InputHandler():
    # std::py3 is:  class InputHandler(metaclass=ABCMeta):

    def inputList(self, files, path, attribute):
        '''Pass the list of files that are to be opened for reading.'''
        pass

    def __next__(self):
        '''If available, the (next) detector data item is returned.'''
        pass

    def __iter__(self):
        pass

if __name__ == "__main__":
    print("No functionality, just an abstract base class definition.")

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

# fabio authors and citation:
# Knudsen, E. B., Sorensen, H. O., Wright, J. P., Goret, G.
#   & Kieffer, J. (2013). J. Appl. Cryst. 46, 537-539.
# http://dx.doi.org/10.1107/S0021889813000150


'''This is an implementation of the file handler based on fabio.
Please find more information on fabio in the source code of this file.
Or take a look at http://dx.doi.org/10.1107/S0021889813000150 .'''


import fabio
import inputHandler


class FabioInputHandler(inputHandler.InputHandler):

    def __init__(self):
        '''Construct by creating empty member variables.'''
        self._fileList = None
        self._ddata = None

    def inputList(self, filenames, paths=None, attribute=None):
        '''Pass and store the list of files that are to be opened.'''
        self._fileList = filenames
        self._fileIter = iter(self._fileList)

    def __iter__(self):
        '''Part one of iterator protocol implementation.'''
        return self

    def __next__(self):
        '''Part two of iterator protocol implementation.'''
        # advance the file iterator
        if(inputHandler.six.PY2):
            aFile = self._fileIter.next()
        else:
            aFile = self._fileIter.__next__()
        # try to read the file and its data
        try:
            imagestream = fabio.open(aFile)
            self._ddata = imagestream.data
        except IOError:
            self._ddata = None
        return self._ddata

    if(inputHandler.six.PY2):
        def next(self):
            self.__next__()

if __name__ == "__main__":
    print("Do simple testing by running as a script.")
    print("Requires the test data to be present.\n")

    print("Trying to read different file formats and print its contents:")
    files = ["test/test_data/pilatus1m/calib_agbeh_andre_00001_00001.cbf",
             "test/test_data/hamamatsu_c4880_maxim/c_02.tif",
             "test/test_data/hamamatsu_c4880_maxim/im_cont2_038.tif"]

    io = FabioInputHandler()
    io.inputList(files)
    for i in io:
        print(repr(i))

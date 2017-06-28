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

import inputHandlerFactory


class DataHandler():

    def __init__(self):
        '''The constructor instantiates a factory.'''
        self.readerFactory = inputHandlerFactory.InputHandlerFactory()
        self.fileHandler = None

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
            print("Error with opening the file, bailing out.")
        except TypeError:
            print ("WTF?")
        return self.fileHandler

    def setDimension(self, dimension):
        self.fileHandler.setDimension(dimension)

if __name__ == "__main__":
    files = [
        "test/test_data/hamamatsu_c4880_maxim/c_02.tif",
        "test/test_data/hamamatsu_c4880_maxim/im_cont2_038.tif"]

    files2 = [
        "test/test_data/lambda750ksi/Calli_align_00004.ndf"]

    path = "/entry/instrument/detector/data"

    dh = DataHandler()
    ndg = DataHandler()
    
    k = dh.create_reader(files)
    print(k)
    for f in k:
        print ("reading tif")

    k2 = ndg.create_reader(files2, path)
    print(k2)
    for j in k2:
        print("reading nexus")
    

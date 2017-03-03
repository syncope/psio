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


'''This is the test for the dataHandler module.'''


import unittest
import dataHandler

class TestDataHandler(unittest.TestCase):

    def setUp(self):
        self.dh1 = dataHandler.DataHandler()
        self.dh2 = dataHandler.DataHandler()
        self.dh3 = dataHandler.DataHandler()
    
    def test_whatever(self):
        self.assertEqual('ja','ja')

if __name__ == '__main__':
    unittest.main()


#~ class DataHandler():
    #~ def __init__(self):
        #~ '''The constructor instantiates a factory.''' 
        #~ self.readerFactory = inputHandlerFactory.InputHandlerFactory() 
        #~ self.fileHandler = None
#~ 
    #~ def create_reader(self, filenames, path=None, attribute=None):
        #~ '''Creates a file reader object. First argument has to be either
           #~ a single filename or a list of filenames.
           #~ Second argument is only needed for path in NeXus/hdf5 files.'''
        #~ if(not isinstance(filenames, list)):
            #~ filenames = [filenames]
        #~ try:
            #~ self.fileHandler = self.readerFactory.create(filenames, path, attribute)
            #~ self.fileHandler.inputList(filenames, path, attribute)
        #~ except IOError:
            #~ print("Error with opening the file, bailing out.")
        #~ except TypeError:
            #~ print ("WTF?")
        #~ return self.fileHandler
            #~ 
    #~ def setDimension(self, dimension):
        #~ self.fileHandler.setDimension(dimension)

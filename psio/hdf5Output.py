# Copyright (C) 2017  Christoph Rosemann, DESY, Notkestr. 85, D-22607 Hamburg
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


'''Implementation of OutputBase for handling files based on HDF5.
   Creates a file structure compatible to the NeXus data format.'''

from . import outputBase
import h5py
import numpy as np


class HDF5Output(outputBase.OutputBase):

    def __init__(self, filename, mode='w'):
        '''Creates a file structure that is equivalent to NeXus data format.
           The default structure is group/data.
           Attributes are added to this:
            {"NX_class":"NXentry", "NX_class":"NXdata"}

           :param filename: name of the file
           :param mode: creation mode, fixed to recreate for now
           :type filename: str
           :type mode: char'''

        self._file = h5py.File(filename, mode=mode)
        self._entry = self._file.create_group("entry")
        self._entry.attrs["NX_class"] = "NXentry"
        self._defaultGroup = self._entry.create_group("data")
        self._defaultGroup.attrs["NX_class"] = "NXdata"
        # datasets are called fields in nexus
        self._datasets = {}

    def write(self):
        '''Commits the current state to permanent storage.'''
        self._file.flush()

    def close(self):
        '''Closes the underlying file **after writing**.'''
        self.write()
        self._file.close()

    def addDataField(self, name, data):
        '''Adds data to the default location.

            :param name: location name for the data
            :param data: the actual data
            :type name: str
            :type data: numpy data type
            :raises: ValueError if the location already exists
            :raises: AttributeError if the location cannot be accessed '''
        # size and shape are taken directly from data
        try:
            if name in self._datasets:
                raise ValueError("Trying to create a field/dataset"
                                 " that already exists.")
            else:
                self._datasets[name] = self._defaultGroup.create_dataset(
                    name=name, data=data)
        except AttributeError:
            print("Could not create a field to hold images/data.")

    def addAttributeToField(self, fieldname, title, value):
        '''Adds an attribute to the given holding structure.

            :param fieldname: location  name for the attribute to be added
            :param title: the name of the attribute
            :param value: the value of the attribute
            :type fieldname: string
            :type title: string
            :type value: any numpy data type
            :return: nothing
            :raises: KeyError if no structure of the given name is found'''
        try:
            self._datasets[fieldname].attrs.create(title, value)
        except KeyError:
            print("Field " + fieldname + " doesn't exist.")

    def addCommentToField(self, fieldname, title, comment):
        '''Convenience function to overload the attribute creation for strings.

            :param fieldname: the location name for the comment to add
            :param title: the name of the attribute
            :param comment: the actual comment
            :type fieldname: string
            :type title: string
            :type value: a string
            :return: nothing
            :raises: KeyError if no structure of the given name is found'''
        try:
            self._datasets[fieldname].attrs.create(title, np.string_(comment))
        except KeyError:
            print("Field " + fieldname + " doesn't exist.")

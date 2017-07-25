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


'''Implementation for handling files based on HDF without pni library.
Structure is the same, as well as the functionality.'''

from . import outputBase
import h5py
import numpy as np


class HDF5Output(outputBase.OutputBase):

    def __init__(self, filename, mode='w'):
        self._file = h5py.File(filename, mode=mode)
        self._entry = self._file.create_group("entry")
        self._entry.attrs["NX_class"] = "NXentry"
        self._defaultGroup = self._entry.create_group("data")
        self._defaultGroup.attrs["NX_class"] = "NXdata"
        # datasets are called fields in nexus
        self._datasets = {}

    def write(self):
        self._file.flush()

    def close(self):
        self.write()
        self._file.close()

    def addDataField(self, name, data):
        '''Add data to the default location.'''
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
        pass
        try:
            self._datasets[fieldname].attrs.create(title, value)
        except KeyError:
            print("Field " + fieldname + " doesn't exist.")

    def addCommentToField(self, fieldname, title, comment):
        pass
        try:
            self._datasets[fieldname].attrs.create(title, np.string_(comment))
        except KeyError:
            print("Field " + fieldname + " doesn't exist.")


if(__name__ == "__main__"):
    print("Testing the output capabilities.")

    no = HDF5Output("test.h5", mode='w')
    no.addDataField("test", (0, 2, 2))
    no.addDataField("test2", (2, 2))
    no.addCommentToField("test", "com2", "we dont need no")
    no.addAttributeToField("test2", "answer", 42.)

    no.close()
    print("In case of success a new file called test.h5 should have been created.")

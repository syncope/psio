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

import outputBase
import h5py
import numpy as np


class HDF5Output(outputBase.OutputBase):

    def __init__(self, filename, mode='w'):
        self._file = h5py.File(filename,mode=mode)
        self._entry = self._file.create_group("entry")
        self._entry.attrs["NX_class"] = "NXentry"
        self._defaultGroup = self._entry.create_group("data")
        self._defaultGroup.attrs["NX_class"] = "NXdata"
        self._datasets = {} # called fields in nexus

    def write(self):
        self._file.flush()

    def close(self):
        self.write()
        self._file.close()

    def addField(self, name, dimension, dtype="float32"):
        '''Adding a field to hold data at the default location.'''
        try:
            correctedDimension = dimension[1:]
        except TypeError:
            correctedDimension = (dimension, )
        chunk = (1,) + correctedDimension
        try:
            if name in self._datasets:
                raise ValueError("Trying to create a field/dataset that already exists.")
            else:
                print(" CREATE DS with chunks = " + str(chunk))
                self._datasets[name] = self._defaultGroup.create_dataset(
                    name=name, dtype=dtype, shape=chunk, chunks=chunk, maxshape=(None, correctedDimension))
        except AttributeError:
            print(
                "Could not create a field to hold images/data.")

    def addSingleImageField(self, name, dimension, dtype="float32"):
        pass
        '''Adding a field to hold a single image.'''
        try:
            self._fields[name] = self._defaultGroup.create_field(
                name, dtype, dimension)
        except AttributeError:
            print(
                "Could not create a single image field element.")

    def addDataToField(self, name, data):
        try:
            initialshape = self._datasets[name].shape
            print("shape bf: " + repr(initialshape))
            newlength = initialshape[0]+1
            temptpl = (newlength, ) + initialshape[1:]
            print(" trying hard to create: " + repr(temptpl))
            self._datasets[name].resize(temptpl)
            print(" shape af: " + repr(self._datasets[name].shape))
            self._datasets[name][-1, ...] = data
        except KeyError:
            print("Field " + name + " doesn't exist.")

    def addSingleImageToField(self, name, data):
        pass
        try:
            self._fields[name].write(data)
        except KeyError:
            print("Field " + name + " doesn't exist.")

    def addAttributeToField(self, fieldname, title, value):
        pass
        try:
            self._fields[fieldname].attributes.create(
                title, "float64")[...] = value
        except KeyError:
            print("Field " + fieldname + " doesn't exist.")

    def addCommentToField(self, fieldname, title, comment):
        pass
        try:
            self._fields[fieldname].attributes.create(
                title, "str")[...] = comment
        except KeyError:
            print("Field " + fieldname + " doesn't exist.")


if(__name__ == "__main__"):
    print("It's working.")
    no = HDF5Output("test.h5", mode='w')
    no.addField("test", (0, 2, 2))
    no.addField("test2", (2, 2))
    #~ no.addCommentToField("test", "com2", "we dont need no")
    #~ no.addAttributeToField("test2", "answer", 42.)

    import numpy as np
    d = np.array([1, 2, 3, 4])
    print(d)
    no.addDataToField("test", d)
    no.addSingleImageToField("test2", d)
    no.close()

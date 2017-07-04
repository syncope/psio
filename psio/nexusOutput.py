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


'''Implementation for handling files based on NeXus file format.
For more information on NeXus visit www.nexusformat.org'''

import outputBase
import pni.io.nx.h5 as nexus


class NexusOutput(outputBase.OutputBase):

    def __init__(self, filename, recreate):
        self._file = nexus.create_file(filename, overwrite=recreate)
        self._root = self._file.root()
        temp = self._root.create_group("entry:NXentry")
        self._defaultGroup = temp.create_group("data:NXdata")
        self._fields = {}

    def write(self):
        self._file.flush()

    def close(self):
        self.write()
        self._file.close()

    def getRoot(self):
        return self._root

    def addField(self, name, dimension, dtype="float32"):
        '''Adding a field to hold data at the default location.'''
        try:
            chunk = (1,) + dimension[1:]
        except TypeError:
            chunk = (1,) + (dimension, )
        try:
            self._fields[name] = self._defaultGroup.create_field(
                name, dtype, dimension, chunk)
        except AttributeError:
            print(
                "something bad happened while trying to add a default field.")

    def addSingleImageField(self, name, dimension, dtype="float32"):
        '''Adding a field to hold a single image.'''
        try:
            self._fields[name] = self._defaultGroup.create_field(
                name, dtype, dimension)
        except AttributeError:
            print(
                "something bad happened while trying to add a default field.")

    def addDataToField(self, name, data):
        try:
            self._fields[name].grow(0, 1)
            self._fields[name][-1, ...] = data
        except KeyError:
            print("Field " + name + " doesn't exist.")

    def addSingleImageToField(self, name, data):
        try:
            self._fields[name].write(data)
        except KeyError:
            print("Field " + name + " doesn't exist.")

    def addAttributeToField(self, fieldname, title, value):
        try:
            self._fields[fieldname].attributes.create(
                title, "float64")[...] = value
        except KeyError:
            print("Field " + fieldname + " doesn't exist.")

    def addCommentToField(self, fieldname, title, comment):
        try:
            self._fields[fieldname].attributes.create(
                title, "str")[...] = comment
        except KeyError:
            print("Field " + fieldname + " doesn't exist.")


if(__name__ == "__main__"):
    print("It's working.")
    no = NexusOutput("test.ndf", recreate=True)
    no.addField("test", (0, 2, 2))
    no.addField("test2", (2, 2))
    no.addCommentToField("test", "com2", "we dont need no")
    no.addAttributeToField("test2", "answer", 42.)

    import numpy as np
    d = np.array([1, 2, 3, 4])
    print(d)
    no.addDataToField("test", d)
    no.addSingleImageToField("test2", d)
    no.close()

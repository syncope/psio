# Copyright (C) 2017 Christoph Rosemann, DESY, Notkestr. 85, D-22607 Hamburg
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

'''This is the test for the hdf5 output module.'''

import unittest
import os
from psio import hdf5Output


class TestHDF5Output(unittest.TestCase):

    def test_constructor(self):
        o = hdf5Output.HDF5Output("hdf5test.h5", mode='w')
        o.close()

    def test_write(self):
        out2 = hdf5Output.HDF5Output("hdf5test2.h5", mode='w')
        out2.addDataField("test", (0, 2, 2))
        out2.write()
        out2.close()

    def test_close(self):
        out2 = hdf5Output.HDF5Output("hdf5test2.h5", mode='w')
        out2.close()

    def test_addAttribute(self):
        out2 = hdf5Output.HDF5Output("hdf5test2.h5", mode='w')
        out2.addDataField("test", (0, 2, 2))
        out2.addDataField("test2", (2, 2))
        out2.addAttributeToField("test2", "answer", 42.)
        out2.close()

    def test_addComment(self):
        out2 = hdf5Output.HDF5Output("hdf5test2.h5", mode='w')
        out2.addDataField("test", (0, 2, 2))
        out2.addDataField("test2", (2, 2))
        out2.addCommentToField("test", "com2", "we dont need no")
        out2.close()

    def test_addDataField(self):
        out2 = hdf5Output.HDF5Output("hdf5test2.h5", mode='w')
        out2.addDataField("test", (0, 2, 2))
        out2.close()

if __name__ == '__main__':
    unittest.main()

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

'''This is the test for the fabio based input module.'''

import unittest
import os
from psio import fabioInputHandler


class TestFabioInputHandler(unittest.TestCase):

    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"
        f1 = "test_data/pilatus1m/calib_agbeh_andre_00001_00001.cbf"
        f2 = "test_data/hamamatsu_c4880_maxim/c_02.tif"
        f3 = "test_data/hamamatsu_c4880_maxim/im_cont2_038.tif"

        img1 = os.path.join(dir_path, f1)
        img2 = os.path.join(dir_path, f2)
        img3 = os.path.join(dir_path, f3)

        self.files = [img1, img2, img3]
        self.dataHandle = fabioInputHandler.FabioInputHandler()
        self.dataHandle2 = fabioInputHandler.FabioInputHandler(files=self.files)

    def test_emptyConstructor(self):
        self.assertIsNone(self.dataHandle._fileList)
        self.assertIsNone(self.dataHandle._fileIter)

    def test_fileConstructor(self):
        self.assertEqual(self.dataHandle2._fileList, self.files)
        self.assertIsNotNone(self.dataHandle2._fileIter)

    def test_inputList(self):
        self.dataHandle.inputList(self.files)
        self.assertEqual(self.dataHandle._fileList, self.files)
        self.assertIsNotNone(self.dataHandle._fileIter)

    def test_getEntry(self):
        with self.assertRaises(TypeError):
            self.dataHandle2.getEntry(1)

    def test_getNofEntries(self):
        self.assertEqual(self.dataHandle2.getTotalNumberOfEntries(), 3)


if __name__ == '__main__':
    unittest.main()

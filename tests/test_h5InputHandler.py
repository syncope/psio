# Copyright (C) 2017  Christoph Rosemann, DESY, Notkestr. 85, D-22607 Hamburg
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

'''This is the test for the h5py input module.'''

import unittest
import os
from psio import h5InputHandler


class TestH5InputHandler(unittest.TestCase):

    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"
        f1 = "test_data/lambda750ksi/Calli_align_00004.ndf"
        img1 = os.path.join(dir_path, f1)

        self.dataHandle = h5InputHandler.H5InputHandler()
        self.dAttHandle = h5InputHandler.H5InputHandler()
        self.files = [img1, ]
        self.path = "entry/instrument/detector/"
        self.dataName = "data"
        self.dPath = self.path+self.dataName
        self.dDim = (516, 1556)
        self.dAtt = "count_time"
        self.dAttKey = "units"
        self.dAttVal = "millisecond"
        self.dataHandle2 = h5InputHandler.H5InputHandler(
            files=self.files, path=self.dPath)
        self.dAttHandle2 = h5InputHandler.H5InputHandler(
            files=self.files, path=self.dPath, attribute=self.dAtt)

    def test_emptyConstructor(self):
        self.assertIsNone(self.dataHandle._fileList)
        self.assertIsNone(self.dataHandle._fileIter)
        self.assertIsNone(self.dataHandle._dataset)
        self.assertIsNone(self.dataHandle._dataIter)
        self.assertIsNone(self.dataHandle._nentries)
        self.assertIsNone(self.dataHandle._attribute)
        self.assertFalse(self.dataHandle._singleValue)
        self.assertIsNone(self.dataHandle._currentFile)
        self.assertEqual(self.dataHandle._imageDataDimension, 2)

    def test_pathConstructor(self):
        self.assertEqual(self.dataHandle2._fileList, self.files)
        self.assertIsNotNone(self.dataHandle2._fileIter)
        self.assertIsNone(self.dataHandle2._dataIter)
        self.assertIsNone(self.dataHandle2._nentries)
        self.assertIsNone(self.dataHandle2._attribute)
        self.assertFalse(self.dataHandle2._singleValue)
        self.assertIsNone(self.dataHandle2._currentFile)
        self.assertEqual(self.dataHandle2._imageDataDimension, 2)

    def test_attributeConstructor(self):
        self.assertEqual(self.dAttHandle2._fileList, self.files)
        self.assertIsNotNone(self.dAttHandle2._fileIter)
        self.assertIsNotNone(self.dAttHandle2._dataset)
        self.assertIsNone(self.dAttHandle2._dataIter)
        self.assertIsNone(self.dAttHandle2._nentries)
        self.assertIsNotNone(self.dAttHandle2._attribute)
        self.assertFalse(self.dAttHandle2._singleValue)
        self.assertIsNone(self.dAttHandle2._currentFile)
        self.assertEqual(self.dAttHandle2._imageDataDimension, 2)

    def test_inputList(self):
        self.dataHandle.inputList(self.files, self.dPath)
        self.assertEqual(self.dataHandle._fileList, self.files)
        self.assertIsNotNone(self.dataHandle._fileIter)
        self.assertIsNone(self.dataHandle._dataIter)
        self.assertIsNone(self.dataHandle._nentries)
        self.assertIsNone(self.dataHandle._attribute)
        self.assertFalse(self.dataHandle._singleValue)
        self.assertIsNone(self.dataHandle._currentFile)
        self.assertEqual(self.dataHandle._imageDataDimension, 2)

        self.dAttHandle.inputList(self.files, self.dPath, self.dAtt)
        self.assertEqual(self.dAttHandle._fileList, self.files)
        self.assertIsNotNone(self.dAttHandle._fileIter)
        self.assertIsNotNone(self.dAttHandle._dataset)
        self.assertIsNone(self.dAttHandle._dataIter)
        self.assertIsNone(self.dAttHandle._nentries)
        self.assertIsNotNone(self.dAttHandle._attribute)
        self.assertFalse(self.dAttHandle._singleValue)
        self.assertIsNone(self.dAttHandle._currentFile)
        self.assertEqual(self.dAttHandle._imageDataDimension, 2)

    def test_getEntry(self):
        self.assertIsNotNone(self.dataHandle2.getEntry(0))
        self.assertIsNotNone(self.dAttHandle2.getEntry(0))
        with self.assertRaises(IndexError):
            self.dataHandle2.getEntry(1)
        with self.assertRaises(IndexError):
            self.dAttHandle2.getEntry(1)

    def test_getNofEntries(self):
        self.assertEqual(self.dataHandle2.getTotalNumberOfEntries(), 1)
        self.assertEqual(self.dAttHandle2.getTotalNumberOfEntries(), 1)


if __name__ == '__main__':
    unittest.main()

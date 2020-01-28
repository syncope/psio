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

'''This is the test for the dataHandler module.'''

import unittest
import os
from psio import dataHandler


class TestDataHandler(unittest.TestCase):

    def setUp(self):
        
        dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"
        f1 = "test_data/pilatus1m/calib_agbeh_andre_00001_00001.cbf"
        f2 = "test_data/hamamatsu_c4880_maxim/c_02.tif"
        f3 = "test_data/hamamatsu_c4880_maxim/im_cont2_038.tif"
        f4 = "test_data/lambda750ksi/Calli_align_00004.ndf"
        f5 = "test_data/spec/MnCo15.spc"
        f6 = "test_data/fio/EuPtIn4_remeasured_00349.fio"

        img1 = os.path.join(dir_path, f1)
        img2 = os.path.join(dir_path, f2)
        img3 = os.path.join(dir_path, f3)
        img4 = os.path.join(dir_path, f4)
        img5 = os.path.join(dir_path, f5)
        img6 = os.path.join(dir_path, f6)

        self.dh = dataHandler.DataHandler()
        self.dhFAB = dataHandler.DataHandler([img1, img2, img3])
        self.dhH5 = dataHandler.DataHandler(img4,path="entry/instrument/detector/data")
        self.dhSPC = dataHandler.DataHandler(img5, typehint="spec")
        self.dhFIO = dataHandler.DataHandler(img6, typehint="fio")

    def test_getters(self):
        self.assertEqual(self.dhH5.getTotalNumberOfEntries(), 1)
        self.assertEqual(self.dhFAB.getTotalNumberOfEntries(), 3)
        self.assertIsNotNone(self.dhH5.getEntry(0))
        with self.assertRaises(TypeError):
            self.dhFAB.getEntry(1)
        with self.assertRaises(IndexError):
            self.dhH5.getEntry(1)

    def test_Iteration(self):
        for d in self.dhFAB:
            pass
        for k in self.dhH5:
            pass
        for j in self.dhSPC:
            pass
        for n in self.dhFIO:
            pass

    def tearDown(self):
        self.dhFAB = None
        self.dhH5 = None
        self.dhSPC = None
        self.dhFIO = None
        self.dh = None

if __name__ == '__main__':
    unittest.main()

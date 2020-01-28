# Copyright (C) 2019  Christoph Rosemann, DESY, Notkestr. 85, D-22607 Hamburg
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

'''This is the test for the fio file reading input module.'''

import unittest
import os
from psio import fioInputHandler


class TestfioInputHandler(unittest.TestCase):

    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"
        f1 = "test_data/fio/EuPtIn4_remeasured_00349.fio"
        f2 = "test_data/fio/EuPtIn4_remeasured_00356.fio"
        f3 = "test_data/fio/EuPtIn4_remeasured_00361.fio"
        img1 = os.path.join(dir_path, f1)
        img2 = os.path.join(dir_path, f2)
        img3 = os.path.join(dir_path, f3)

        self.dataHandle = fioInputHandler.FioInputHandler()
        self.dhFIO = fioInputHandler.FioInputHandler([ img1, img2, img3 ])

    def test_emptyConstructor(self):
        self.assertIsNotNone(self.dataHandle)

    def test_getAll(self):
        self.assertEqual(len(self.dhFIO.getAll()), 3)

    def test_getEntry(self):
        scan = self.dhFIO.getEntry(356)
        self.assertEqual(scan.getMotorName(), "del")

    def test_getNofEntries(self):
        self.assertEqual(self.dhFIO.getTotalNumberOfEntries(), 3)

if __name__ == '__main__':
    unittest.main()

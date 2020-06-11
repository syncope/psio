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

'''This is another test for the spec file reading module.'''

import unittest
import os
from psio import specInputHandler


class TestspecInputHandler2(unittest.TestCase):

    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"
        f = "test_data/spec/cro05_2.spc"
        img = os.path.join(dir_path, f)

        self.dataHandle = specInputHandler.SpecInputHandler()
        self.dhSPC = specInputHandler.SpecInputHandler([img,])

    def test_emptyConstructor(self):
        self.assertIsNotNone(self.dataHandle)

    def test_getAll(self):
        self.assertEqual(len(self.dhSPC.getAll()), 2724)

    def test_getEntry(self):
        scan = self.dhSPC.getEntry(383)
        self.assertEqual(scan.getMotorName(), "h_position")

    def test_getNofEntries(self):
        self.assertEqual(self.dhSPC.getTotalNumberOfEntries(), 2724)

if __name__ == '__main__':
    unittest.main()

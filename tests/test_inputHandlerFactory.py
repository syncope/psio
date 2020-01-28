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


'''This is the test for the input handler factory module.'''

import unittest
import os
from psio import inputHandlerFactory


class TestInputHandlerFactory(unittest.TestCase):

    def setUp(self):
        self.factory = inputHandlerFactory.InputHandlerFactory()

    def test_fabio(self):
        fabobj = self.factory.create("bla.cbf", path=None, attribute=None)
        self.assertIsInstance(fabobj, inputHandlerFactory.fabioInputHandler.FabioInputHandler)

    def test_h5(self):
        h5obj = self.factory.create("bla.ndf", path="here/is/now", attribute=None)
        self.assertIsInstance(h5obj, inputHandlerFactory.h5InputHandler.H5InputHandler)

    def test_spec(self):
        spcobj = self.factory.create("bla.spc",typehint="spec")
        self.assertIsInstance(spcobj, inputHandlerFactory.specInputHandler.SpecInputHandler)

    # for now the test makes no sense; everything is mapped to fabio
    # unless there is a path given, which means that it is a hdf5 file
    # def test_unknown(self):
    #   with self.assertRaises(TypeError):
    #       unknownobj = self.factory.create("some.txt", path=None, attribute=None)


if __name__ == '__main__':
    unittest.main()

# Copyright (C) 2020  Christoph Rosemann, DESY, Notkestr. 85, D-22607 Hamburg
# email contact: christoph.rosemann@desy.de
#
# psio :: photon science input ouput is a library to facilitate the 
# access to file based data by offering unified services to different
# data formats
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

import numpy as np



class MultiModuleObject():

    def __init__(self, module_id=None):
        self._module_id = module_id
        self._error_code = None
        self._sequence_number = None

    def error_code(self):
        return self._error_code

    def module_id(self):
        return self._module_id

    def sequence_number(self):
        return self._sequence_number

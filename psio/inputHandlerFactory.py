# Copyright (C) 2016 Christoph Rosemann, DESY, Notkestr. 85, D-22607 Hamburg
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

'''This a factory that creates implementation objects of an InputHandler.'''


from . import fabioInputHandler
from . import h5InputHandler


class InputHandlerFactory():

    '''Simple factory class that creates implementation objects.'''

    def __init__(self):
        pass

    def create(self, filenames, path, attribute):
        handlertype = self._determine_handlertype(
            filenames[0], path, attribute)
        if(handlertype == "fabio"):
            return fabioInputHandler.FabioInputHandler()
        elif (handlertype == "h5"):
            return h5InputHandler.H5InputHandler()
        else:
            raise TypeError("Unrecognized IOHandler type.\
            Please chose an existing implementation.")

    def _determine_handlertype(self, filename, path, attribute):
        if(path is None):
            return "fabio"
        elif(attribute is None):
            return "h5"
        else:
            return "h5"

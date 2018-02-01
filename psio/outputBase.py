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


'''Base class for output. Functionality is implemented by children classes.'''


class OutputBase():
    def __init__(self):
        pass

    def write(self):
        '''Commits the current state to permanent storage.'''
        pass

    def close(self):
        '''Closes the underlying file **after writing**.'''
        pass

    def addDataField(self, name, data):
        '''Creates the holding structure and adds the data to it.

            :param name: the name of the data, acts as key
            :param data: the actual numpy data type
            :type name: string
            :type data: any numpy data type
            :return: nothing
            :raises: AttributeError if the structure cannot be created
            :raises: ValueError if the name is already in use'''
        pass

    def addAttributeToField(self, fieldname, title, value):
        '''Adds an attribute to the given holding structure.

            :param fieldname: location name for the attribute to be added
            :param title: the name of the attribute
            :param value: the value of the attribute
            :type fieldname: string
            :type title: string
            :type value: any numpy data type
            :return: nothing
            :raises: KeyError if no structure of the given name is found'''
        pass

    def addCommentToField(self, fieldname, title, comment):
        '''Convenience function to overload the attribute creation for strings.

            :param fieldname: location name for the comment to be added
            :param title: the name of the attribute
            :param comment: the actual comment
            :type fieldname: string
            :type title: string
            :type value: a string
            :return: nothing
            :raises: KeyError if no structure of the given name is found'''
        pass

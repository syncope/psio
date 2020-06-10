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


'''The Lambda NeXus Reader facilitates the access to the hdf5 format 
   files written by the lambda detector family.'''


from . import dataHandler


class LambdaNeXusReader():

    def __init__(self, afile='', detectorpath='/entry/instrument/detector'):
        '''The constructor.'''
        self._detectorpath = detectorpath
        self._sequencenumbername = 'sequence_number'
        self._errorname = 'collection/error_code'
        self._translationname = 'translation/distance'
        self._pixelmaskname = 'pixel_mask'
        self._pixalmaskappliedname = 'pixel_mask_applied'
        self._flatfieldname = 'flatfield'
        self._flatfieldappliedname = 'flatfield_applied'

    def getTranslation(self):
        '''Returns the translation.'''
        pass

    def getPixelSize(self):
        '''Returns the pixel size.'''
        pass

    def getFlatfield(self):
        '''Returns the flat field.'''
        pass

    def isFlatfieldApplied(self):
        '''Returns wether the flatfield has been applied.'''
        pass

    def getPixelMask(self):
        '''Returns the pixel mask.'''
        pass

    def isPixelMaskApplied(self):
        '''Returns wether the pixel mask has been applied.'''
        pass

    def getCountTime(self):
        '''Returns the integration time.'''
        pass

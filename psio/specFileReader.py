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


# general idea:
# a) read in the file, decompose into individual scans:
#    !!! the separation is asserted to be a blank line !!!
# b) create a list of raw scan objects
# c) convert the raw objects into scan data objects


import numpy as np
try:
    # StringIO behaves like a file object
    from cStringIO import StringIO
except ImportError:
    # no more StringIO in Python3 -> different module
    from io import StringIO

from psio.specFileScanData import SpecFileScanData
from . import psioException


class SpecFileReader():
    def __init__(self, fname=None):
        self._fname = fname
        self._rawScanList = []
        self._scanList = None
        self._scanDataList = []
        self._file = None

    def open(self, fname):
        self._fname = fname

    def close(self):
        try:
            if(not self._file.closed):
                self._file.close()
        except:
            pass

    def read(self, scanlist=None):
        with open(self._fname, 'r') as f:
            self.checkIntegrity(f.readline())

        try:
            self._file = open(self._fname, 'r')
        except(IOError):
            print("[SpecFileReader]:: Can't open the file '" + str(self._fname) + "'. Exiting.")
            raise psioException.PSIONoFileException()

        # convert the scanlist string to a real list of integers
        self._scanList = self.convertToList(scanlist)

        # start iteration to create individual scan objects
        nextScan = rawScan()
        for line in self._file:
            if line in ['\n', '\r\n']:
                if nextScan is not None:
                    self._rawScanList.append(nextScan)
                    nextScan = rawScan()
            else:
                nextScan.addLine(line)
        if nextScan is not None:
            self._rawScanList.append(nextScan)

        # convert the raw objects into scan data
        for rawS in self._rawScanList:
            converted = rawS.convertToScanData()
            if converted is not None:
                if self.checkValidScanID(converted.getScanNumber()):
                    self._scanDataList.append(converted)
        self._file.close()
        return self._scanDataList

    def checkValidScanID(self, scanNumber):
        if self._scanList is not None:
            return scanNumber in self._scanList
        else:
            return True

    def convertToList(self, obj):
        if obj is None:
            return

        retlist = []
        # first divide into elements from comma-separated list
        try:
            elements = obj.split(',')
        except AttributeError:
            return None

        # iterate over elements: either range (with or without stride) and single values
        for element in elements:
            #  check for stride mark
            if element.find(':') != -1:
                elementstride = int(element.split(':')[-1])
                elem = element.split(':')[0]
                tmp = elem.split('-')
                for i in range(int(tmp[0]), int(tmp[1]) + 1, elementstride):
                    retlist.append(i)
            else:
                tmp = element.split('-')
                if(len(tmp) == 2):
                    for i in range(int(tmp[0]), int(tmp[1]) + 1):
                        retlist.append(i)
                else:
                    # if there is no split, then the elements will be lists!
                    if(len(tmp) != 1):
                        print("Error in preparing the input selection of spec file scan lists.")
                    else:
                        retlist.append(int(tmp[0]))

        retlist.sort()
        return retlist

    def checkIntegrity(self, firstline):
        words = firstline.rstrip('\n')
        splitWords = words.split(' ')
        keyword = splitWords[0]
        if keyword != "#S":
            raise psioException.PSIOSPECFileException()


class rawScan():
    '''Placeholder object for disassembling the spec file'''

    def __init__(self):
        self._lines = []
        self._dataString = ""

    def addLine(self, line):
        self._lines.append(line)
        if line.split(' ')[0][0] == '@':
            pass
        elif line.split(' ')[0][0] != '#':
            self._dataString += line

    def checkFileHeader(self, line):
        # search for a starting '#F' in the given line
        words = line.rstrip('\n')
        splitWords = words.split(' ')
        keyword = splitWords[0]
        return keyword == '#F'

    def convertToScanData(self):
        '''Create the scanData object from the raw file objects.'''
        # get the different comment fields, as specified
        sd = SpecFileScanData()
        rawKeys = []
        rawValues = []

        # !!! Workaround: some files contain a file header at the beginning
        # the keyword is then '#F'
        # SKIP THIS ATM --
        if(self.checkFileHeader(self._lines[0])):
            print("found one!")
            return None

        for line in self._lines:
            words = line.rstrip('\n')
            splitWords = words.split(' ')
            keyword = splitWords[0]
            if keyword == '#S':
                sd.setStartline(splitWords[1:])
            elif keyword == '#U':
                sd.addUserData(splitWords[1:])
            elif keyword == '#D':
                sd.setDate(splitWords[1:])
            elif keyword == '#C':
                sd.addComment(splitWords[1:])
            elif keyword == '#N':
                sd.setNumberOfColumns(splitWords[1])
            elif keyword == '#L':
                for w in splitWords[1:]:
                    if w != '':
                        sd.addLabel(w)
            elif keyword[0:2] == '#O':
                for w in splitWords[1:]:
                    if w != '':
                        rawKeys.append(w)
            elif keyword[0:2] == '#P':
                for w in splitWords[1:]:
                    if w != '':
                        rawValues.append(w)
            elif keyword[0:8] == "#@MCA_NB":
                if(splitWords[1] != "1"):
                    print("In reading MCA data more than one detector is present.")
            elif keyword[0:7] == "#@DET_0":
                sd.setMCAName(splitWords[1])
            elif keyword[0:2] == "@A":
                sd.addMCA(np.asarray(splitWords[1:-1], dtype=float))

        sd.addCustomdataDict({rawKeys[i]: rawValues[i] for i in range(len(rawValues))})

        # check if everything is there
        if not sd.checkSanity():
            return

        labels = sd.getLabels()
        noc = sd.getNumberOfColumns()

        if(self._dataString == ''):
            # logger.info("[SpecFileReader] No data to read in scan number " + str(sd.getScanNumber()))
            return None

        # get the data into numpy arrays
        sio = StringIO(self._dataString)
        multi = np.loadtxt(sio, unpack=True)

        sd.addDataDict({labels[i]: multi[i] for i in range(noc)})
        return sd

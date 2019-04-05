# Copyright (C) 2019  Christoph Rosemann, DESY, Notkestr. 85, D-22607 Hamburg
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


'''fioFileReader implementation for Python3 and v2.'''



import numpy as np
try:
    # StringIO behaves like a file object
    from cStringIO import StringIO
except ImportError:
    # no more StringIO in Python3 -> different module
    from io import StringIO

from psio.asciiFileScanData import AsciiFileScanData


class FioFileReader():
    def __init__(self, fname=None):
        self._fname = fname
        self._file = None
        self._scandata = AsciiFileScanData()

    def open(self, fname):
        self._fname = fname

    def close(self):
        try:
            if(self._file.closed):
                self._file.close()
        except:
            pass

    def read(self):
        try:
            self._file = open(self._fname, 'r')
        except(IOError):
            print("[FioFileReader]:: Can't open the file '" + str(self._fname) + "'. Exiting.")
            exit(255)
        rawdict = {'comment': [], 'param': [], 'data': []}
        mode = ''
        for line in self._file.readlines():
            if line.find('%c') == 0:
                mode = 'comment'
                continue
            elif line.find('%p') == 0:
                mode = 'param'
                continue
            elif line.find('%d') == 0:
                mode = 'data'
                continue
            elif line[0] == '!':
                continue
            if mode is not '':
                rawdict[mode].append(line)
        self._getScanNumber()
        self._getComments(rawdict['comment'])
        self._getParameters(rawdict['param'])
        self._getData(rawdict['data'])
        return self._scandata

    def _getScanNumber(self):
        import re
        import os
        fname = os.path.splitext(self._fname)[0]
        sn = re.search(r'\d+$', fname)
        self._scandata.setScanNumber(int(sn.group(0)) if sn else None)

        return self._scandata.getScanNumber()

    def _getComments(self, clist):
        self._scandata.setScanCommand(clist[0].strip())
        self._scandata.addComment(clist[1])
        return self._scandata.getScanCommand()

    def _getParameters(self, plist):
        rawKeys = []
        rawValues = []
        for element in plist:
            param = element.split( "=")
            rawKeys.append(param[0].strip())
            rawValues.append(param[1].strip())
        self._scandata.addCustomdataDict({rawKeys[i]: rawValues[i] for i in range(len(rawValues))})

    def _getData(self, dlist):
        pass
        # Col 1 del DOUBLE



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
        sd = FioFileScanData()
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
                if( splitWords[1] != "1"):
                    print("In reading MCA data more than one detector is present.")
            elif keyword[0:7] == "#@DET_0":
                sd.setMCAName(splitWords[1])
            #~ elif keyword[0:2] == "#@":
                #~ print("Illegal start characters: #@. Skip for now until issue is resolved.")
                #~ pass
            elif keyword[0:2] == "@A":
                sd.addMCA(np.asarray(splitWords[1:-1], dtype=float))

        sd.addCustomdataDict({rawKeys[i]: rawValues[i] for i in range(len(rawValues))})

        # check if everything is there
        if not sd.checkSanity():
            return

        labels = sd.getLabels()
        noc = sd.getNumberOfColumns()

        if(self._dataString == ''):
            # logger.info("[FioFileReader] No data to read in scan number " + str(sd.getScanNumber()))
            return None

        # get the data into numpy arrays
        sio = StringIO(self._dataString)
        multi = np.loadtxt(sio, unpack=True)

        sd.addDataDict({labels[i]: multi[i] for i in range(noc)})
        sd.addLabelDict({i: labels[i] for i in range(noc)})

        return sd

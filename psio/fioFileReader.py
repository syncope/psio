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
            if(not self._file.closed):
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
        self.close()
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
            param = element.split("=")
            rawKeys.append(param[0].strip())
            rawValues.append(param[1].strip())
        self._scandata.addCustomdataDict({rawKeys[i]: rawValues[i] for i in range(len(rawValues))})

    def _getData(self, dlist):
        tmplabels = []
        tmptmpdata = []
        self._scandata.addLabel("Pt_No")
        for elem in dlist:
            e = elem.strip()
            if "Col" in e:
                cs = e.split(" ")
                tmplabels.append(str(cs[2]))
                self._scandata.addLabel(str(cs[2]))
            else:
                tmptmpdata.append(elem)
        # add "Pt_No" to fio data, not originally there
        tmplabels.insert(0, "Pt_No")
        li = []
        for i, el in enumerate(tmptmpdata):
            li.append(str(i) + str(el))
        tmpdata = np.loadtxt(li, unpack=True)
        self._scandata.addDataDict({tmplabels[i]: tmpdata[i] for i in range(len(tmplabels))})

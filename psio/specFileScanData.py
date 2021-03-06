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

from . import psioException

class SpecFileScanData():
    '''This is the atomic data exchange object. It consists of all
       information that is needed for a scan.'''

    def __init__(self):
        self._startline = ''
        self._number = 0
        self._userdata = []
        self._date = ''
        self._comments = []
        self._customdata = {}
        self._noc = 0
        self._labels = []
        self._dataDict = {}
        self._mcaname = ''
        self._mca = []

    def getScanNumber(self):
        return self._number

    def getLabels(self):
        return self._labels

    def getNumberOfColumns(self):
        return self._noc

    def getArray(self, key):
        return self._dataDict[key]

    def getCustomKeys(self):
        return self._customdata.keys()

    def getCustomVar(self, key):
        return self._customdata[key]

    def getStartline(self):
        return self._startline

    def getScanCommand(self):
        return self._startline[1:]

    def getScanType(self):
        return self._startline[1]

    def getStartIdentifier(self, num):
        return self._startline[num]

    def setStartline(self, sl):
        self._startline = sl
        self.setScanNumber(int(sl[0]))

    def getMotorName(self):
        # highly specific to DESY/PETRA III type of spec data
        scantype = self.getScanType()
        if(scantype == "ascan" or scantype == "dscan"):
            return self.getStartIdentifier(2)
        elif (scantype == "hscan"):
            return "h_position"
        elif (scantype == "kscan"):
            return "k_position"
        elif(scantype == "lscan"):
            return "l_position"
        elif(scantype == "hklscan"):
            return "h_position"
        elif(scantype == "d2scan"):
            return self.getStartIdentifier(2)
        else:
            print("[specFileScanData] scan not recognized, identifier is: " + self.getStartIdentifier(2))
            raise psioException.PSIOUnknownScanTypeException()

    def getRanges(self):
        # helper function for identifying different range settings
        # again very specific for PETRA III
        scantype = self.getScanType()
        if(scantype == "ascan" or scantype == "dscan"):
            motor = self._startline[2]
            motorrange = abs(float(self._startline[4]) - float(self._startline[3]))
            return {motor : motorrange}
        elif(scantype == "hscan"):
            motor = "h_position"
            motorrange = abs(float(self._startline[3]) - float(self._startline[2]))
            return {motor : motorrange}
        elif(scantype == "kscan"):
            motor = "k_position"
            motorrange = abs(float(self._startline[3]) - float(self._startline[2]))
            return {motor : motorrange}
        elif(scantype == "lscan"):
            motor = "l_position"
            motorrange = abs(float(self._startline[3]) - float(self._startline[2]))
            return {motor : motorrange}
        elif(scantype == "hklscan"):
            motor1 = "e6cctrl_h"
            motor2 = "e6cctrl_k"
            motor3 = "e6cctrl_l"
            motor1range = abs(float(self._startline[3]) - float(self._startline[2]))
            motor2range = abs(float(self._startline[5]) - float(self._startline[4]))
            motor3range = abs(float(self._startline[7]) - float(self._startline[6]))
            return {motor1 : motor1range, motor2 : motor2range, motor3 : motor3range}
        elif(scantype == "d2scan"):
            motor1 = self._startline[2]
            motor1range = abs(float(self._startline[4]) - float(self._startline[3]))
            motor2 = self._startline[5]
            motor2range = abs(float(self._startline[7]) - float(self._startline[6]))
            return {motor1 : motor1range, motor2 : motor2range}
        elif (scantype == "hscan"):
            return {self._startline[1]: abs(float(self._startline[3]) - float(self._startline[2]))}
        else:
            raise psioException.PSIOUnknownScanTypeException()

    def getMCA(self):
        return self._mca

    def getMCAName(self):
        return self._mcaname

    def setScanNumber(self, number):
        self._number = int(number)

    def addUserData(self, userdata):
        self._userdata.append(userdata)

    def setDate(self, date):
        self._date = date

    def addComment(self, comment):
        self._comments.extend(comment)

    def addCustomdataDict(self, dic):
        self._customdata = dic

    def setNumberOfColumns(self, noc):
        self._noc = int(noc)

    def addLabel(self, label):
        self._labels.append(label)

    def addDataDict(self, dic):
        self._dataDict = dic

    def addMCA(self, data):
        self._mca.append(data)

    def setMCAName(self, name):
        self._mcaname = name

    def checkSanity(self):
        '''Tests whether the minimal requirements are met.'''
        if (self._noc is not len(self._labels)):
            return False
        return (self._startline and self._labels and self._noc)

    def info(self):
        print("[SpecFileScanData] Values are: ")
        print(self._startline)
        print(self._number)
        print(self._userdata)
        print(self._date)
        print(self._comments)
        print(self._customdata)
        print(self._noc)
        print(self._labels)
        print(self._dataDict)
        print(self._mcaname)
        print(str(self._mca))

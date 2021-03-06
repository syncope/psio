# Copyright (C) 2019  Christoph Rosemann, DESY, Notkestr. 85, D-22607 Hamburg
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


class AsciiFileScanData():
    '''Base class for exchange data objects read from ACII files.'''

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
        self._scancommand = ''
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
        if self._scancommand == '':
            self._scancommand = self._startline[1:]
        return self._scancommand

    def getScanType(self):
        if self._scancommand == '':
            return self._startline[1:]
        else:
            return self._scancommand.split(' ')[0]

    def getStartIdentifier(self, num):
        return self._startline[num]

    def setStartline(self, sl):
        self._startline = sl
        self.setScanNumber(int(sl[0]))

    def getMotorName(self):
        # highly specific stuff to DESY/PETRA III
        scantype = self.getScanType()
        if(scantype == "ascan" or scantype == "dscan"):
            return self._scancommand.split(' ')[1]
        elif(scantype == "d2scan"):
            return self._scancommand.split(' ')[1]
        elif (scantype == "hscan"):
            return "e6cctrl_h"

    def getRanges(self):
        # helper function for identifying different range settings
        # example line:
        # d2scan del -0.4 0.4 th -0.2 0.2 30 2.0
        scantype = self.getScanType()
        if(scantype == "ascan" or scantype == "dscan"):
            motor = self._scancommand.split(' ')[1]
            motorrange = abs(float(self._scancommand.split(' ')[3]) - float(self._scancommand.split(' ')[2]))
            return {motor : motorrange}
        elif(scantype == "d2scan"):
            motor1 = self._scancommand.split(' ')[1]
            motor1range = abs(float(self._scancommand.split(' ')[3]) - float(self._scancommand.split(' ')[2]))
            motor2 = self._scancommand.split(' ')[4]
            motor2range = abs(float(self._scancommand.split(' ')[6]) - float(self._scancommand.split(' ')[5]))
            return {motor1 : motor1range, motor2 : motor2range}
        elif (scantype == "hscan"):
            motor = self._scancommand.split(' ')[1]
            motorrange = abs(float(self._scancommand.split(' ')[3]) - float(self._scancommand.split(' ')[2]))
            return {motor : motorrange}

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

    def setScanCommand(self, sc):
        self._scancommand = sc

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
        print("[AsciiFileScanData] Values are: ")
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

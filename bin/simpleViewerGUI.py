# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simpleViewerG.ui'
#
# Created: Thu Apr 14 09:19:27 2016
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(928, 453)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.xyz = QtGui.QTextBrowser(self.centralwidget)
        self.xyz.setObjectName(_fromUtf8("xyz"))
        self.horizontalLayout.addWidget(self.xyz)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 1, 1, 1)
        self.displaypart = ImageView(self.centralwidget)
        self.displaypart.setObjectName(_fromUtf8("displaypart"))
        self.gridLayout_2.addWidget(self.displaypart, 0, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 928, 19))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.uvw = QtGui.QMenu(self.menubar)
        self.uvw.setObjectName(_fromUtf8("uvw"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.uvw.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.uvw.setTitle(_translate("MainWindow", "&File", None))

from pyqtgraph import ImageView

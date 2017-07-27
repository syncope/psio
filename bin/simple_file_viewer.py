import sys
from PyQt4 import QtCore, QtGui

from simpleViewerGUI import Ui_MainWindow

import psio

import json

class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        openfile = QtGui.QAction(QtGui.QIcon('open.png'), 'Open', self)
        openfile.setShortcut('Ctrl+O')
        openfile.setStatusTip('Open new File')
        openfile.triggered.connect(self.showDialog)

        self.ui.uvw.addAction(openfile)       
 
    def showDialog(self):

        fname = str(QtGui.QFileDialog.getOpenFileName(self, 'Open file', 
                '.'))
                
        if (fname == ''):
            return
        io = psio.dataHandler.DataHandler(fname)
        #self.head = io.getHeader()
        #info = json.dumps(self.head)
        #self.ui.xyz.setText(info)

        self.nda = None
        for d in io:
            self.nda = d
            self.ui.displaypart.setImage(self.nda)
    

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())

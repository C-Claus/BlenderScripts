import sys 
sys.path.append('C:\Python 39\Lib\site-packages')
import bpy

from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
                             QAction, QFileDialog,QMenu, QApplication,
                             QGridLayout, QLabel, QLineEdit, QWidget, QPushButton)
                             
from PyQt5.QtGui import QIcon
import sys
from pathlib import Path


from blenderbim.bim.ifc import IfcStore


class ExportWindow(QMainWindow, QWidget):
    def __init__(self, parent=None):
        super(ExportWindow, self).__init__(parent)
        
        self.initUI()
        
     
    def initUI(self):
  

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        open_file = QAction('Open Excel', self)
        open_file.triggered.connect(self.open_excel)
        fileMenu.addAction(open_file)
 
        self.setGeometry(1200, 100, 350, 600)
        self.setWindowTitle('BlenderBIM Excel')
        self.show()


    def open_excel(self):
        print("Open Excel")
        
        home_dir = str(IfcStore.path)
        fname = QFileDialog.getOpenFileName(self, 'Open file', home_dir)
        
                

try:
    app = QtWidgets.QApplication(sys.argv) 
    window = ExportWindow()
    window.show()

    # https://stackoverflow.com/questions/28060218/where-is-pyqt-event-loop-running

except Exception as e:
    print ('error')
    print (e)
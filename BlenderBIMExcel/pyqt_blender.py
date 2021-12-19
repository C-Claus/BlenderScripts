import sys 
sys.path.append('C:\Python 39\Lib\site-packages')
import bpy

from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QWidget, QPushButton


from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
                             QAction, QFileDialog, QApplication)
from PyQt5.QtGui import QIcon
import sys
from pathlib import Path


from blenderbim.bim.ifc import IfcStore

def get_ifc_file_path():
    
    ifc_file_location = IfcStore.path
    
    print (ifc_file_location)
    
    return (str(ifc_file_location))

class ExportWindow(QWidget):
    def __init__(self, parent=None):
        super(ExportWindow, self).__init__(parent)

        mainLayout = QGridLayout()
        
        
        """

        test1Label = QLabel("IFcProduct")
        test1Line = QLineEdit()
        mainLayout.addWidget(test1Label, 0, 0)
        mainLayout.addWidget(test1Line, 0, 1)

        test2Label = QLabel("Test 2:")
        test2Line = QLineEdit()
        mainLayout.addWidget(test2Label, 1, 0, Qt.AlignTop)
        mainLayout.addWidget(test2Line, 1, 1)
        
        """

        button_export = QPushButton('Export to Excel', self)
        button_export.clicked.connect(self.export_to_excel)
        mainLayout.addWidget(button_export, 2, 0)
        
 
        
        
        
        self.setGeometry(1200, 100, 350, 600)

        self.setLayout(mainLayout)
        self.setWindowTitle("BlenderBIM Excel")

    def export_to_excel(self):
        print("Export to Excel")
        
        home_dir = str(IfcStore.path)
        fname = QFileDialog.getOpenFileName(self, 'Open file', home_dir)
        
        #get_ifc_file_path()
        #app.beep()
        #window.hide()
        # note that at this point, I think the Qt app
        # is technically still 'running'
        
        

                

try:
    app = QtWidgets.QApplication(sys.argv) 
    window = ExportWindow()
    window.show()

    # I was surprised to see that it wasn't necessary to 
    # somehow start the Qt event loop.  Normally something like
    # app.exec() would need to be called, but that of course
    # would hang blender. I found some info on why
    # event loop likely works from within blender without
    # additional setup here:
    # https://stackoverflow.com/questions/28060218/where-is-pyqt-event-loop-running

except Exception as e:
    print ('error')
    print (e)
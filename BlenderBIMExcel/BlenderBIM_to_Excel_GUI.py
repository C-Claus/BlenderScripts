import os
import sys 
sys.path.append('C:\Python 39\Lib\site-packages')

import bpy
import logging
import blenderbim.bim.import_ifc
from blenderbim.bim.ifc import IfcStore
import blenderbim.tool as tool

import openpyxl
from openpyxl import load_workbook

from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
                             QAction, QFileDialog,QMenu, QApplication, 
                             QHBoxLayout, QVBoxLayout,
                             QGridLayout, QLabel, QLineEdit, QWidget, QPushButton)
                             


#from pathlib import Path





class ExportWindow(QMainWindow, QWidget):
    def __init__(self, parent=None):
        super(ExportWindow, self).__init__(parent)
        
        self.initUI()
        
     
    def initUI(self):
        #mainLayout = QGridLayout()
  

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        open_file_button = QAction('Open Excel', self)
        open_file_button.triggered.connect(self.open_excel)
        fileMenu.addAction(open_file_button)
        
        self.button_filter = QPushButton('Filter IFC elements', self)
        self.button_filter.setEnabled(False)
        self.button_filter.setGeometry(0, 560, 350, 40)
        #button_filter.clicked.connect(self.get_filtered_data_from_excel())
        #mainLayout.addWidget(button_export, 3, 0)
 
        self.setGeometry(1200, 100, 350, 600)
        self.setWindowTitle('BlenderBIM Excel')
        self.show()


    def open_excel(self):
        print("Open Excel")
        
        
        file_name = QFileDialog.getOpenFileName(self, 'Open file', str(IfcStore.path))
        
        global excel_file
        excel_file = file_name[0]
        os.startfile(file_name[0])
        self.button_filter.setEnabled(True)
        
        self.button_filter.clicked.connect(self.get_filtered_data_from_excel)
        
        #os.startfile(str(IfcStore.path))
        
        #if file_name[0] is not None:
        #    os.startfile(str(file_name[0]))
        
        #if fname is not None:
        #    #print ((fname[0])) 
        #    os.startfile(fname[0])

           
            
            #button_filter = QPushButton('Filter IFC elements', self)
            #button_filter.setGeometry(0, 560, 350, 40)
            #button_filter.clicked.connect(self.get_filtered_data_from_excel()
            
            
 
    def get_filtered_data_from_excel(self):
        workbook_openpyxl = load_workbook(excel_file)
        worksheet_openpyxl = workbook_openpyxl['IfcProduct'] 
        print ('hallo')
     
      
        global_id_filtered_list = []

        for row in worksheet_openpyxl:     
            if worksheet_openpyxl.row_dimensions[row[0].row].hidden == False:
                for cell in row:  
                    if cell in worksheet_openpyxl['A']:  
                        global_id_filtered_list.append(cell.value)
                        
              
              
              
        print (global_id_filtered_list)
        

        #blender crasht hierop
        #print (bpy.context.screen)
        
        """    
        outliner = next(a for a in bpy.context.screen.areas if a.type == "OUTLINER") 
        outliner.spaces[0].show_restrict_column_viewport = not outliner.spaces[0].show_restrict_column_viewport
        
        bpy.ops.object.select_all(action='DESELECT')
      
        for obj in bpy.context.view_layer.objects:
            element = tool.Ifc.get_entity(obj)
            if element is None:        
                obj.hide_viewport = True
                continue
            data = element.get_info()
          
            obj.hide_viewport = data.get("GlobalId", False) not in global_id_filtered_list

        bpy.ops.object.select_all(action='SELECT')
        
        """
          
          
                

try:
    app = QtWidgets.QApplication(sys.argv) 
    window = ExportWindow()
    window.show()

    # https://stackoverflow.com/questions/28060218/where-is-pyqt-event-loop-running

except Exception as e:
    print ('error')
    print (e)
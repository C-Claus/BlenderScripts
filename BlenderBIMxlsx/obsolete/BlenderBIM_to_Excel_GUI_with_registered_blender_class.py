import os
import bpy
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import  QPushButton, QFileDialog

class QtModalOperator(bpy.types.Operator):
    """A base class for Operators that run a Qt interface."""

    def modal(self, context, event):

        if self._app:
            self._app.processEvents()
            return {'PASS_THROUGH'}

        return {"FINISHED"}

    def execute(self, context):
        """Execute the Operator.
        The child class must implement execute() and call super to trigger this
        class' execute() at the beginning. The execute() method must finally
        return {'RUNNING_MODAL"}
        Note that the Qt code should *not* call QApplication.exec_() as it
        seems that magically the Qt application already processes straight
        away in Blender. Maybe due to:
        https://stackoverflow.com/questions/28060218/where-is-pyqt-event
        -loop-running
        """

        self._app = QtWidgets.QApplication.instance()
        if not self._app:
            self._app = QtWidgets.QApplication(["blender"])


class BlenderBIMExcelGUI(QtModalOperator):

    bl_idname = "object.qt_blenderbim_excel"
    bl_label = "BlenderBIM Excel QT UI"

    def execute(self, context):
        # Initialize Qt operator execution
        
        global widget
        
        widget = QtWidgets.QWidget()
        
        button_open_excel = QPushButton(widget)
        button_open_excel.setText("Open Excel")
        button_open_excel.move(64,0)
        button_open_excel.clicked.connect(self.open_excel)
        
        button_filter = QPushButton(widget)
        button_filter.setText("Filter IFC Elements")
        button_filter.move(64,32)
        #button_filter.clicked.connect(self.filter_IFC_elements)
        

        widget.resize(800, 600)
        widget.move(800, 200)
        widget.setWindowTitle('BlenderBIM Excel')
        widget.show()
        
 
        return {'RUNNING_MODAL'}
    
    def open_excel(self):
       
        
        print("Open Excel")
        
        #options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        #file_name, _ = QFileDialog.getOpenFileName(self,"-", "IfcStore.path","All Files (*);;Excel Files (*.xlsx)", options=options)
        #if file_name:
        #    print(file_name)
        
     
    



        

bpy.utils.register_class(BlenderBIMExcelGUI)
bpy.ops.object.qt_blenderbim_excel()

import bpy
from PyQt5 import QtWidgets


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


class QtTestOperator(QtModalOperator):
    """Launch Avalon Creator.."""


    bl_idname = "object.qt_test"
    bl_label = "Test Qt UI.."


    def execute(self, context):
        # Initialize Qt operator execution
        super(QtTestOperator, self).execute(context)
        
        global widget
        #widget = QtWidgets.QPushButton("Hello")
        widget = QtWidgets.QWidget()
        widget.resize(250, 150)
        widget.move(800, 200)
        #window.setWindowTitle('BlenderBIM Excel')
        widget.show()
        return {'RUNNING_MODAL'}
        

bpy.utils.register_class(QtTestOperator)


bpy.ops.object.qt_test()




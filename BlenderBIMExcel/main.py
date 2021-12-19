import sys
from PySide2 import QtWidgets

class Ui_Form(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Ui_Form, self).__init__(parent)
        
        self.setFixedSize(300,300)

        self.camera_CB = QtWidgets.QComboBox()
        self.create_camera_PB = QtWidgets.QPushButton(text="Create a camera")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.camera_CB)
        layout.addWidget(self.create_camera_PB)

        self.setLayout(layout)
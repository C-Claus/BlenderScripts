import sys
from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

app = QApplication(sys.argv)
def Start():
    m = myWindow()
    m.showWid()
    sys.exit(app.exec())

class myWindow:
  def __init__(self):
    self.window = QWidget()
    self.window.setWindowTitle("BlenderBIM <-> Excel")
    self.window.setFixedWidth(600)
    self.window.setStyleSheet("background: #18BEBE;")

  def showWid(self):
    self.window.show()

if __name__ == "__main__":
    Start()
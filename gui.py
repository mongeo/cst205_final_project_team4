import soundToImage
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QToolTip, QMessageBox, QLabel)

class ImageWindow(QtWidgets.QMainWindow):
    a = [[0,0,0]]
    def work(self):
        #nparr = np.array(self.soundObj.tupleArr)
        for i in range(0,self.nparr[0]):
            test = self.hilbert.coordinates_from_distance(abs(self.nparr[1][i,0] + self.nparr[1][i,1]))
            self.a.append([test[0],test[1],abs(self.nparr[1][i,0]*self.nparr[1][i,1])%255])
            print(test)

    #@numba.jit(parallel=True)
    def setImg(self):
        for i in self.a:
            self.canvas.setPixel(i[0],i[1],int(1000))
            self.canvas.setPixelColor(i[0],i[1],QtGui.QColor(i[2] + i[0] % 255, i[2] + i[1] % 255, i[2]))
        self.label.setPixmap(QtGui.QPixmap.fromImage(self.canvas.scaled(1000,1000, Qt.KeepAspectRatioByExpanding)))
        self.label.show()
    def __init__(self, filePath):

        super().__init__()
        self.soundObj = soundToImage.Curve(filePath)
        self.hilbert = self.soundObj.getHilbert()
        self.nparr = np.array(self.soundObj.normalizeCurve())
        self.label = QtWidgets.QLabel()
        self.canvas = QtGui.QPixmap(300, 300).toImage()
        self.work()
        self.setImg()
        self.label.show()

class Window2(QMainWindow):                           # <===
    def __init__(self):
        super().__init__()
        self.setWindowTitle("file_select")
        self.openFileNamesDialog()
    def openFileNamesDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(self,"Select your wav file to visualize!", "","Wav Files (*.wav)", options=options)
        self.file = ""
        if files:
            self.file = files[0]
class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "audio_visualizer"
        self.top = 400
        self.left = 400
        self.width = 400
        self.height = 100

        self.pushButton = QPushButton("choose_file", self)
        self.pushButton.move(50, 50)
        self.pushButton.setToolTip("<h3>Start the Session</h3>")

        self.pushButton.clicked.connect(self.window2)              # <===

        self.main_window()

    def main_window(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def window2(self):                                             # <===
        self.w = Window2()
        self.w.show()
        self.w.hide()
        self.imageWindow = ImageWindow(self.w.file)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())
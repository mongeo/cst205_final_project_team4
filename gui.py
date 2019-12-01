import sys
import soundToImage
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import multiprocessing
from joblib import Parallel, delayed
from tqdm import tqdm

from PyQt5.QtCore import Qt
from hilbertcurve.hilbertcurve import HilbertCurve

filename = "audio_files/test.wav"
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(100,100).toImage()
        soundObj = soundToImage.Curve(filename)
        hilbert = soundObj.getHilbert()
        '''
        for i in soundObj.wf[1]:
            test = hilbert.coordinates_from_distance(abs(i[0]))
            canvas.setPixel(test[0], test[1], 255)
        '''
        #test = soundObj.normalizeCurve()
        for i in soundObj.tupleArr:
            #TODO Overflows
            if i < 0:
                continue
            test = hilbert.coordinates_from_distance(abs(i))
            canvas.setPixel(test[0], test[1], 255)
        self.label.setPixmap(QtGui.QPixmap.fromImage(canvas))
        self.setCentralWidget(self.label)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
#window.draw_something()

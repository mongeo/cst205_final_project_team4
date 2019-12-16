#ONLY WORKS WITH 3 CHANNEL WAVE
import numpy as np
import sys
from hilbertcurve.hilbertcurve import HilbertCurve
import scipy.io.wavfile as wf2

class Curve:
    #Can set size based off of how accurate we want to be
    TIMEPERIOD = 11026 * 100000
    BUFFSIZE = sys.getsizeof(int()) * TIMEPERIOD
    #Set during constructor
    aAmp = []
    aFreq = []
    points = []
    wf = []
    intensityList = []
    tupleArr = np.array([0,0])

    def getFreq(self, y: np.ndarray, fs: int):
        spec = np.abs(np.fft.rfft(y))
        freq = np.fft.rfftfreq(len(y), d=1 / fs)
        amp = spec / spec.sum()
        mean = (freq * amp).sum()
        return int(np.average(mean))

    def getAmp(self, y: np.ndarray, fs: int):
        spec = np.abs(np.fft.rfft(y))
        return np.average(spec / spec.sum())

    def spectral_statistics(y: np.ndarray, fs: int) -> int:
        """
        Compute mean frequency

        :param y: 1-d signal
        :param fs: sampling frequency [Hz]
        :return: mean frequency
        """
        spec = np.abs(np.fft.rfft(y))
        freq = np.fft.rfftfreq(len(y), d=1 / fs)
        amp = spec / spec.sum()
        mean = (freq * amp).sum()
        return int(mean)

    def getAverageAmp(self, buff):
        aBuff = [i for i in buff]
        total = 0
        for i in aBuff:
            total += i
        return int(total/self.BUFFSIZE)

    def getHilbert(self):
        # Arbitrary length, should never go above 99 in most cases.
        return HilbertCurve(99, 2)

    def normalizeCurve(self):
        return self.wf


    def __init__(self, wavFilePath):
        #Returns sample [FPS,Data]
        self.wf = wf2.read(wavFilePath)
        self.normalizeCurve()
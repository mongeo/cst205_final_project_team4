import pyaudio
import numpy.fft
#ONLY WORKS WITH 3 CHANNEL WAVE
import wave
import numpy as np
import struct
import array
import sys
import math
import PyQt5
from hilbertcurve.hilbertcurve import HilbertCurve
from scipy.ndimage.interpolation import shift

from scipy import signal
import scipy.io.wavfile as wf2

class Curve:
    #Can set size based off of how accurate we want to be
    TIMEPERIOD = 11026
    BUFFSIZE = sys.getsizeof(int()) * TIMEPERIOD
    #Set during constructor
    aAmp = []
    aFreq = []
    points = []
    wf = []
    intensityList = []
    tupleArr = []

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
        return HilbertCurve(200, 2)#len(self.wf[1]))

    #TODO: Make tuple array. Loc, Amplitude(Intensity)
    def normalizeCurve(self):
        tempCurve = np.array(self.wf[1], dtype=np.intc)
        min = tempCurve.min()
        for i in tempCurve:
            self.tupleArr.append(abs(i[0] + abs(min)))
            self.tupleArr.append(abs(i[1] + abs(min)))
            self.intensityList.append(i[0])
            self.intensityList.append(i[1])
        return tempCurve


    def __init__(self, wavFilePath):
        #Returns sample [FPS,Data]
        self.wf = wf2.read(wavFilePath)
        self.normalizeCurve()
        #Creating our graph
        '''
        #12 is size of int, so we want to make sure we have an int of data left
        while len(buff) > sys.getsizeof(int()):
            numpArr = np.frombuffer(buff)
            self.aAmp.append(self.getAmp(numpArr,sampleFreq))
            self.aFreq.append(self.getFreq(numpArr,sampleFreq))
            buff = wf.readframes(self.BUFFSIZE)
        '''
# -*- coding: utf-8 -*-
import sys
sys.path.append('..')  # help python find open_bci_v3.py
import open_bci_v3 as bci
# import os
# import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import time

from multiprocessing import Process, Queue

############################################
#
# ACQUISITION SECTION
#
############################################


def acquisition_proc(eeg_sig):

    def plotData(sample):
        eeg_sig.put(sample.channel_data[0])
        print(sample.channel_data[0])

    if __name__ == '__main__':
        port = '/dev/ttyUSB0'
        # baud = 115200
        board = bci.OpenBCIBoard(port=port)
        board.start_streaming(plotData)

if __name__ == '__main__':

    # it can be started at the bottom as well
    eeg_sig = Queue()
    p = Process(target=acquisition_proc, args=(eeg_sig,))
    p.start()

############################################
#
# PLOTTING SECTION
#
############################################

app = QtGui.QApplication([])

win = pg.GraphicsWindow()

p1 = win.addPlot(title="FP1")
p1.setYRange(-8, 8, padding=0)
curve_01 = p1.plot()
ptr = 0

win.nextRow()

y_min = -1
y_max = 1

p2 = win.addPlot(title="FP2")
p2.setYRange(y_min, y_max, padding=0)
curve_02 = p2.plot()
ptr = 0

# readData = [0.0, 0.0]

eeg_01 = [0] * 1000
eeg_02 = [0] * 1000


def update():
    global curve_01, curve_02, data_01, data_02, ptr, p1, p2, y_min, y_max
    data = eeg_sig.get()
    eeg_01.append(data)
    del eeg_01[0]
    eeg_02.append(data)
    del eeg_02[0]
    if data > y_max:
        y_max = data
        p1.setYRange(y_min, y_max, padding=0)
        p2.setYRange(y_min, y_max, padding=0)
    if data < y_min:
        y_min = data
        p1.setYRange(y_min, y_max, padding=0)
        p2.setYRange(y_min, y_max, padding=0)

    curve_01.setData(eeg_01)
    curve_02.setData(eeg_02)
    if ptr == 0:
        p1.enableAutoRange('xy', False)
        p2.enableAutoRange('xy', False)
    ptr += 1

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(10)

# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

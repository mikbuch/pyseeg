# -*- coding: utf-8 -*-
"""
This example demonstrates many of the 2D plotting capabilities
in pyqtgraph. All of the plots may be panned/scaled by dragging with 
the left/right mouse buttons. Right click on any plot to show a context menu.
"""

# import initExample ## Add path to library (just for examples; you do not need this)


from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import random
import time

app = QtGui.QApplication([])

win = pg.GraphicsWindow()

p1 = win.addPlot(title="FP1")
p1.setYRange(-8, 8, padding=0)
curve_01 = p1.plot()
data_01 = np.random.normal(size=(10,1000))
ptr = 0

win.nextRow()

p2 = win.addPlot(title="FP2")
p2.setYRange(-8, 8, padding=0)
curve_02 = p2.plot()
data_02 = np.random.normal(size=(10,1000))
ptr = 0

readData = [0.0, 0.0]

def readfun():
    readData[0] = random.uniform(-6, 6)
    readData[1] = random.uniform(-6, 6)
    return readData

eeg_01 = [0] * 1000
eeg_02 = [0] * 1000

fps_counter = 0

start_time = time.time()

def update():
    global curve_01, curve_02, data_01, data_02, ptr, p1, p2, fps_counter
    data = readfun()
    eeg_01.append(data[0])
    del eeg_01[0]
    eeg_02.append(data[1])
    del eeg_02[0]
#     curve_01.setData(data[0])
#     curve_02.setData(data[1])

    # lane used for benchmarking
    fps_counter += 1
    print(fps_counter)
    if fps_counter == 24000:
        elapsed_time = time.time() - start_time
        print('')
        print(elapsed_time)
        pg.exit()

    curve_01.setData(eeg_01)
    curve_02.setData(eeg_02)
    if ptr == 0:
        p1.enableAutoRange('xy', False)
        p2.enableAutoRange('xy', False)    
    ptr += 1

    print(len(eeg_01))

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)



## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

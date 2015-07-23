#!/usr/bin/python


from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

import time
import numpy as np

import random


app = QtGui.QApplication([])

win = pg.GraphicsWindow()

p1 = win.addPlot()
p2 = win.addPlot()
p3 = win.addPlot()


curve1 = p1.plot()
curve2 = p2.plot()
curve3 = p3.plot()

readData = [0.0, 0.0, 0.0]
y1=np.zeros(1000,dtype=float)
y2=np.zeros(1000,dtype=float)
y3=np.zeros(1000,dtype=float)

def readfun():
    readData[0] = random.uniform(-6, 6)
    readData[1] = random.uniform(-6, 6)
    readData[2] = random.uniform(-6, 6)
    return readData


indx = 0
def update():
    global curve1, curve2, curve3, indx, y1,y2,y3

    readData= readfun()        #function that reads data from the sensor it returns a list of 3 elements as the y-coordinates for the updating plots
    y1[indx]=readData[0]
    y2[indx]=readData[1]
    y3[indx]=readData[2]

    if indx==999:
       y1=np.zeros(1000,dtype=float)
       y2=np.zeros(1000,dtype=float)
       y3=np.zeros(1000,dtype=float)
    else:
       indx+=1
    curve1.setData(y1)
    curve2.setData(y2)
    curve3.setData(y3)
    app.processEvents()



timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)




if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_'):
        QtGui.QApplication.instance().exec_()

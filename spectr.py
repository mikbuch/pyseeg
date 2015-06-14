#!/usr/bin/env python
from pylab import *
from modules.read_csv import read

z = read('data/dane.txt')
# z = read('data/201506111722.csv')
x = [float(i[0]) for i in z]

NFFT = 251

# the sampling frequency
Fs = 250  

Pxx, freqs, bins, im = specgram(x, NFFT=NFFT, Fs=Fs, noverlap=250,
                                cmap=cm.Accent)

plt.ylim(0, 50)
plt.xlim(0, len(x)/Fs)
show()

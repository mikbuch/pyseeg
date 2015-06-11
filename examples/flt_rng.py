#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    name:
        flt_rng.py
    # # #

    desc:
        This example shows filtering EEG data.
        Butterworth Bandpass filter 8 - 13 Hz (alpha waves).
        8th to 10th second is plotted (time and frequency domain).
'''

import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append('../modules/')
from read_csv import read
import filterlib as flt


# sampling frequency (how many samples per second)
fs = 256.0

# bandpass values
lowcut = 8.0
highcut = 13.0

# file with eeg data location
eeg_file = '../data/128.csv'

# read the eeg file to array
data = read(eeg_file)[20]
data = [float(i) for i in data]

# time analyzed
sec_begin = 8
sec_end = 10

# range (in seconds) of signal analyzed
rng = [sec_begin*int(fs), sec_end*int(fs)]

# raw data from specified range
# rng_data = data[sec_begin*fs:sec_end*fs]

# required for futher plotting appropriate x axis (samples)
time_axis = range(len(data))

# filter data (using butt bandpass filter)
flted = flt.butter_bandpass_filter(data, lowcut, highcut, fs, order=4)

# plot time domain of the signal
plt.plot([i/fs for i in time_axis[rng[0]:rng[1]]], flted[rng[0]:rng[1]])
plt.show()

# plot frequency domain of the signal
flt_rng = flted[rng[0]:rng[1]]
freq = abs(2 * np.fft.fft(flt_rng))/512
freq = freq[:fs]
plt.plot(freq)
plt.show()

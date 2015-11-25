#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    name:
        correlate_eeg_ref.py

'''

# remove two following lines if you are in the main folder of the repo
import sys
sys.path.append('../..')

import numpy as np
import matplotlib.pyplot as plt
import argparse
import csv

from modules.filterlib import filter_eeg
from modules.fft import *

parser = argparse.ArgumentParser()
parser.add_argument("data_file")
args = parser.parse_args()

############################################
#                                          #
#           VARIABLES INIT                 #
#                                          #
############################################
# sampling frequency (how many samples per second)
fs = 250.0

# file with eeg data location
eeg_file = args.data_file

############################################
#                                          #
#          GET DATA FROM FILE              #
#                                          #
############################################
channel = 0
data = []
# read the eeg file to the list
with open(eeg_file, 'rb') as f:
    csvread = csv.reader(f)
    for sample in csvread:
        data.append(float(sample[channel]))

# required for futher plotting appropriate x axis (samples)
x_time = [i/fs for i in range(len(data))]

############################################
#                                          #
#               FILTERING                  #
#                                          #
############################################
# filter data using butt bandstop 49-51 Hz filter (50Hz)
# then filter prefiltered  data using 1-50 Hz bandpass filter
flt = filter_eeg(data, fs)
flt = filter_eeg(flt, fs)
# flt_10 = filter_eeg(data, fs, lowpass=9.5, highpass=10.5)
# flt_20 = filter_eeg(data, fs, lowpass=19.5, highpass=20.5)
# flt_30 = filter_eeg(data, fs, lowpass=29.5, highpass=30.5)
# flt_40 = filter_eeg(data, fs, lowpass=39.5, highpass=40.5)

# sec_20 = flt_20[20*fs:21*fs]
# sec_30 = flt_30[30*fs:31*fs]

############################################
#                                          #
#                SIN COS                   #
#                                          #
############################################

import matplotlib.pyplot as plt
from numpy import arange, sin, cos, pi

sampling_interval = 250
fs = 1./sampling_interval
# fs = 0.004

# create n values in range <0,1> corresponding to time points
t = arange(0.0, 1.0, fs)
# we take one second
# len(t) == 250 ==> 250 time points, as we will have 250 samples

# functions frequency (dependent on frequency of the stimulus)
hz = 20

sin_20 = np.array([sin(2*pi*i*hz) for i in t])
cos_20 = np.array([cos(2*pi*i*hz) for i in t])

hz = 30

sin_30 = np.array([sin(2*pi*i*hz) for i in t])
cos_30 = np.array([cos(2*pi*i*hz) for i in t])

from scipy.stats import pearsonr
print("sin_20 vs flt_20_sec_20_21: %s" % (pearsonr(sin_20, flt[20*sampling_interval:21*sampling_interval]))[0])
print("sin_20 vs flt_20_sec_30_31: %s" % (pearsonr(sin_20, flt[30*sampling_interval:31*sampling_interval]))[0])
print('\n')
print("sin_30 vs flt_30_sec_20_21: %s" % (pearsonr(sin_30, flt[20*sampling_interval:21*sampling_interval]))[0])
print("sin_30 vs flt_30_sec_30_31: %s" % (pearsonr(sin_30, flt[30*sampling_interval:31*sampling_interval]))[0])

plt.plot(sin_20)
plt.plot(flt[20*sampling_interval:21*sampling_interval])
plt.show()
plt.plot(sin_30)
plt.plot(flt[30*sampling_interval:31*sampling_interval])
plt.show()

# freq = transform(flt)
# plot_frequency(freq, 250)
# freq_10 = transform(flt_10)
# plot_frequency(freq_10, 250)
# plt.show()

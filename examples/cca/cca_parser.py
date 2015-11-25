#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
name:
    cca_parser.py

'''


import numpy as np
import matplotlib.pyplot as plt
import csv


############################################
#                                          #
#           VARIABLES INIT                 #
#                                          #
############################################
# sampling frequency (how many samples per second)
fs = 250.0

# file with eeg data location
eeg_files = ['../example_data/e1.txt', '../example_data/e2.txt']

############################################
#                                          #
#          GET DATA FROM FILE              #
#                                          #
############################################
channel = 0
data = [[], []]
# read the eeg file to the list
for i in range(len(eeg_files)):
    with open(eeg_files[i], 'rb') as f:
        csvread = csv.reader(f, delimiter='.')
        for sample in csvread:
            data[i].append(float(sample[channel]))

channel_01 = np.array(data[0])
channel_02 = np.array(data[1])

summed_signal = channel_01 + channel_02

data = summed_signal

# required for futher plotting appropriate x axis (samples)
x_time = [i/fs for i in range(len(data))]

############################################
#                                          #
#               FILTERING                  #
#                                          #
############################################
# filter data using butt bandstop 49-51 Hz filter (50Hz)
# then filter prefiltered  data using 1-50 Hz bandpass filter

# # bandstop filter
# bandstop=(49,51)

# bandpass=(1,50)

from pyseeg.modules.filterlib import filter_eeg
flt = filter_eeg(data, fs, lowstop=48, highstop=52, lowpass=1, highpass=50, order=6)
# flt = flt[fs*5:]

# 10.8, 11, 11.2


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
hz = 10.8

sin_10_8 = np.array([sin(2*pi*i*hz+0.28*pi) for i in t])
cos_10_8 = np.array([cos(2*pi*i*hz+0.28*pi) for i in t])

hz = 11

sin_11 = np.array([sin(2*pi*i*hz+0.56*pi) for i in t])
cos_11 = np.array([cos(2*pi*i*hz+0.56*pi) for i in t])

hz = 11.2

sin_11_2 = np.array([sin(2*pi*i*hz+0.84*pi) for i in t])
cos_11_2 = np.array([cos(2*pi*i*hz+0.84*pi) for i in t])


from scipy.stats import pearsonr

r_corr = np.zeros(shape=(28,3))
sec_num = 0
for i in range(len(flt)):
    if i % 250 == 0 and i+250 <= len(flt):

        print(sec_num)
        flt_sec = flt[i:i+250]

        score_10_8 = max(
            pearsonr(sin_10_8, flt_sec)[0], pearsonr(cos_10_8, flt_sec)[0])
        score_11 = max(
            pearsonr(sin_11, flt_sec)[0], pearsonr(cos_11, flt_sec)[0])
        score_11_2 = max(
            pearsonr(sin_11_2, flt_sec)[0], pearsonr(cos_11_2, flt_sec)[0])

        r_corr[sec_num][0] = score_10_8
        r_corr[sec_num][1] = score_11
        r_corr[sec_num][2] = score_11_2

        sec_num +=1

r_corr = abs(r_corr)
plt.plot(r_corr.T[0], label='10_8')
plt.plot(r_corr.T[1], label='11')
plt.plot(r_corr.T[2], label='11_2')
plt.legend()
plt.show()


# Savicky-Goly filter
       



# ############################################
# #                                          #
# #              SPECTROGRAM                 #
# #                                          #
# ############################################
# import pyseeg.modules.spectrogram as sg
# sg.spectrogram(flt, int(fs))

# ############################################
# #                                          #
# #             FFT TRANSFORM                #
# #                                          #
# ############################################
# # transform data to get power spectrum of the signal

# from pyseeg.modules.fft import *
# freq = transform(flt)
# plot_frequency(freq, fs)
# plt.show()

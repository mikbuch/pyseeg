#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

'''

import numpy as np
import matplotlib.pyplot as plt

from modules.read_csv import read
import modules.filterlib as flt
import modules.spectrogram as sg

############################################
#                                          #
#           VARIABLES INIT                 #
#                                          #
############################################
# sampling frequency (how many samples per second)
fs = 250.0

# bandpass values
lowcut = 1.0
highcut = 50.0

# bandstop values
lowstop = 49.0
highstop = 51.0

# file with eeg data location
# eeg_file = 'data/201506111703.csv'
eeg_file = 'data/201506111744.csv'
# eeg_file = 'data/dane.txt'

# seconds analysed
sec_beg = 15
sec_end = 20
sec_rng = sec_end-sec_beg

# lower and higher range values
rng = [sec_beg*int(fs), sec_end*int(fs)]

############################################
#                                          #
#          GET DATA FROM FILE              #
#                                          #
############################################
# read the eeg file to array
data = read(eeg_file, delimiter=',', header=1)
data = [float(i[0]) for i in data]

data_rng = data[rng[0]:rng[1]]

# required for futher plotting appropriate x axis (samples)
x_time = range(len(data))
x_time = [i/fs for i in x_time]
x_time_rng = x_time[rng[0]:rng[1]]

############################################
#                                          #
#               FILTERING                  #
#                                          #
############################################
# filter data using butt bandstop 49-51 Hz filter (50Hz)
flted_50_stop = flt.butter_bandstop_filter(
    data, lowstop, highstop, fs, order=2
    )
# bandpass filter only
flted_1_50_pass_only = flt.butter_bandpass_filter(
    data, lowcut, highcut, fs, order=2
    )
# filter prefiltered 50_stop data
flted_1_50_pass = flt.butter_bandpass_filter(
    flted_50_stop, lowcut, highcut, fs, order=2
    )

############################################
#                                          #
#            FOURIER TRANSFORM             #
#                                          #
############################################
# choose filtered data type
flted = flted_1_50_pass
# get from the filtered data range (in seconds)
flted_rng = flted[rng[0]:rng[1]]
3
# fourier transform, abs
freq = abs(2 * np.fft.fft(flted_rng))/sec_rng*fs
# cut spectrum half
freq = freq[:len(freq)/2]

# create time frequency axis
x_freq = [i/float(5) for i in range(len(freq))]

# fourier transform for complete data
freq_all = abs(2 * np.fft.fft(flted))/len(flted)
freq_all = freq_all[:len(freq_all)/2]

# create time frequency axis (for complete data)
x_freq_all = [i/float(5) for i in range(len(freq_all))]

############################################
#                                          #
#             PLOTTING DATA                #
#                                          #
############################################
# raw signal time domain plot
plt.subplot(2, 3, 1)
plt.plot(x_time, data)

# filtered signal time domain plot
plt.subplot(2, 3, 2)
plt.plot(x_time, flted)

# frequency domain of the signal (power spectrum) plot
plt.subplot(2, 3, 3)
plt.plot(x_freq_all, freq_all)

# raw signal time domain in range
plt.subplot(2, 3, 4)
plt.plot(x_time_rng, data_rng)

# filtered time domain in range
plt.subplot(2, 3, 5)
plt.plot(x_time_rng, flted_rng)

# frequency domain of the signal (power spectrum) in range
plt.subplot(2, 3, 6)
plt.plot(x_freq, freq)
plt.show()


sg.spectrogram(flted, int(fs))

rtf = flt.FltRealTime()
flted_rt = []
for i in data:
    flted_rt.append(rtf.filterIIR(i,0))

plt.plot(flted_rt)
plt.show()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

'''

import numpy as np
import matplotlib.pyplot as plt

from modules.read_csv import read
import modules.filterlib as flt

# sampling frequency (how many samples per second)
fs = 250.0

# bandpass values
lowcut = 7.0
highcut = 13.0

# file with eeg data location
eeg_file = 'data/flt_no_flt.txt'

# read the eeg file to array
data = read(eeg_file, delimiter='\t', header=1)
data_pre_flted = [float(i[1]) for i in data]
data = [float(i[0]) for i in data]

# raw data from specified range
# rng_data = data[sec_begin*fs:sec_end*fs]

# required for futher plotting appropriate x axis (samples)
time_axis = range(len(data))

# filter data (using butt bandpass filter)
flted = flt.butter_bandpass_filter(data, lowcut, highcut, fs, order=2)

# plot time domain of the signal
plt.plot(time_axis, flted)
plt.plot(time_axis, data_pre_flted, '-r')
plt.show()

# plot frequency domain of the signal
freq = abs(2 * np.fft.fft(flted))/512
freq = freq[:fs]
plt.plot(freq)
freq_pre_flted = abs(2 * np.fft.fft(data_pre_flted))/512
freq_pre_flted = freq_pre_flted[:fs]
plt.plot(freq_pre_flted, '-r')
plt.show()

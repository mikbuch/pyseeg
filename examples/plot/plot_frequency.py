#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
name: plot_frequency.py
type: script
example use: python plot_frequency.py
'''

import matplotlib.pyplot as plt

from pyseeg.modules.csvlib import read_csv
from pyseeg.modules.filterlib import filter_eeg
from pyseeg.modules.fft import transform, plot_frequency


############################################
#                                          #
#           VARIABLES INIT                 #
#                                          #
############################################

# Sampling frequency (how many samples per second).
fs = 250.0


############################################
#                                          #
#          GET DATA FROM FILE              #
#                                          #
############################################

# Get data form channel X.
channel = 0

# Read requested data form csv file.
data = read_csv('../example_data/ssvep_00.csv', channel)


############################################
#                                          #
#              FILTER DATA                 #
#                                          #
############################################

# Filter data using first, bandstop filter, then bandpass filter.
filtered_data = filter_eeg(data, fs, bandstop=(49, 51), bandpass=(1, 50))

# Get signal for 2nd second - how many you have to cut depends on the order
# of the digital filter you apply to the signal (remove first second
# fs=X samples (one second)).
filtered_data = filtered_data[int(fs):]


############################################
#                                          #
#               PLOT DATA                  #
#                                          #
############################################

# Transform data using fft.
frequency_data = transform(filtered_data)

# Plot data's power spectrum (transformed data).
plot_frequency(frequency_data, fs)
plt.show()

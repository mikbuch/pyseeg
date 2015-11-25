#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Filter eeg data and the plot time domain

Name:
    filtration_time.py

Example use:
    python filtration_freq_parse.py ../data/blink_00.csv
"""

# remove two following lines if you are in the main folder of the repo
import sys
sys.path.append('..')

import matplotlib.pyplot as plt
import argparse

from pyseeg.modules.csvlib import read_csv
from pyseeg.modules.filterlib import filter_eeg


# parser initialization
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


############################################
#                                          #
#          GET DATA FROM FILE              #
#                                          #
############################################

# location of the file with eeg data
eeg_file = args.data_file

# get data form channel X
channel = 0

# read requested data form csv file
data = read_csv(eeg_file, channel)


############################################
#                                          #
#              FILTER DATA                 #
#                                          #
############################################

# filter data using first, bandstop filter, then bandpass filter
filtered_data = filter_eeg(data, fs, bandstop=(49, 51), bandpass=(1, 50))

# get signal for 2nd second - how many you have to cut depends on the order
# of the digital filter you apply to the signal
filtered_data = filtered_data[fs:]


############################################
#                                          #
#               PLOT DATA                  #
#                                          #
############################################

# plot data, remember that now len(data)=len(filtered_data)-1*fs
# because the begining of the filtered signal (first second) has been removed
plt.subplot(2, 1, 1)
plt.plot(data, '-r')
plt.title('signal time domain before filtration')

# plot filtered data
plt.subplot(2, 1, 2)
plt.title('signal time domain after filtration')
plt.plot(filtered_data)

plt.show()

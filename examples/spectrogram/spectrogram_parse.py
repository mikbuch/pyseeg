#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
name:
    spectrogram.py

'''

import argparse

from pyseeg.modules.csvlib import read_csv
from pyseeg.modules.filterlib import filter_eeg
import pyseeg.modules.spectrogram as sg

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
filtered_data = filtered_data[int(fs):]


############################################
#                                          #
#              SPECTROGRAM                 #
#                                          #
############################################
sg.spectrogram(filtered_data, int(fs))

#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    name:
        spectrogram.py

'''

# remove two following lines if you are in the main folder of the repo
import sys
sys.path.append('..')

import numpy as np
import matplotlib.pyplot as plt
import argparse

from modules.read_csv import read
import modules.filterlib as flt
import modules.spectrogram as sg

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

# bandpass values
lowcut = 1.0
highcut = 50.0

# bandstop values
lowstop = 49.0
highstop = 51.0

# file with eeg data location
eeg_file = args.data_file

############################################
#                                          #
#          GET DATA FROM FILE              #
#                                          #
############################################
# read the eeg file to the list
data = read(
    eeg_file, delimiter=',', header=1, to_float=True, transpose=True
    )

# choose the channel (in this example its 1st channel - 0)
data = data[0]

# required for futher plotting appropriate x axis (samples)
x_time = [i/fs for i in range(len(data))]

############################################
#                                          #
#               FILTERING                  #
#                                          #
############################################
# filter data using butt bandstop 49-51 Hz filter (50Hz)
flted_50_stop = flt.butter_bandstop_filter(
    data, lowstop, highstop, fs, order=2
    )
# filter prefiltered 50_stop data using 1-50 Hz bandpass filter
flted_1_50_pass = flt.butter_bandpass_filter(
    flted_50_stop, lowcut, highcut, fs, order=2
    )

flted = flted_1_50_pass

############################################
#                                          #
#              SPECTROGRAM                 #
#                                          #
############################################
sg.spectrogram(flted, int(fs))

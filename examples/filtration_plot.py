#!/usr/bin/env python
# -*- coding: utf-8 -*-

# remove two following lines if you are in the main folder of the repo
import sys
sys.path.append('..')

import matplotlib.pyplot as plt

from modules.read_csv import read
from modules.filterlib import filter_eeg


############################################
#                                          #
#          GET DATA FROM FILE              #
#                                          #
############################################

# file with eeg data location
eeg_file = '../data/blink_00.csv'

# specify your sampling frequency
fs = 250

# read the eeg file to the list
data = read(eeg_file)

# choose the channel (here it's 1st channel, with index 0)
data = data[0]


############################################
#                                          #
#              FILTER DATA                 #
#                                          #
############################################

filtered_data = filter_eeg(data, fs)


############################################
#                                          #
#               PLOT DATA                  #
#                                          #
############################################

plt.subplot(2 ,1, 1)
plt.plot(data, '-r')
plt.title('before filtration')

plt.subplot(2, 1, 2)
plt.title('after filtration')
plt.plot(filtered_data)

plt.show()

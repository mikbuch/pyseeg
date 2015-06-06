#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
beeg test.py

test script for beeg
'''

# sampling frequency (how many samples per second)
fs = 250

# time analyzed
sec_begin = 8
sec_end = 10

# file with eeg data location
eeg_file = 'data/128.csv'

# read the eeg file to array
data = read(eeg_file)

# plot time domain of the signal
plot_time(data)

# plot frequency domain of the signal
plot_frequency(data)

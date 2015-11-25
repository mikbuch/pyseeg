#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    name:
        freq.py
    # # #

    description:
        Show frequency domain of complete data or just in some range.

'''

# remove two following lines if you are in the main folder of the repo
import sys
sys.path.append('..')

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
eeg_file = '../data/alpha_01.csv'


# specify two ranges to be compared (ranges in seconds)
# rng_in_sec = [[5, 10], [12, 16], [46, 51], [53, 58]]
rng_in_sec = [[5, 6], [12, 13], [46, 47], [53, 54]]

# list with info: how many seconds does the range include
sec_num = []
# calculate the number of seconds for each range
for bounds in rng_in_sec:
    sec_num.append(
        bounds[1] - bounds[0]
        )

# transform to sample number instead of second value
rng = []
for begin_end in rng_in_sec:
    rng.append([])
    for second in begin_end:
        rng[-1].append(second*int(fs))


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

# choose filtered data
flted = flted_1_50_pass

# get rid of the unfiltered begining of the data
flted = flted[2*fs:]


############################################
#                                          #
#      SPECIFY RANGES FOR COMPARISON       #
#                                          #
############################################

# list storing filtered data in ranges
flted_rng = []

# fill the data_rng list with values of the signal
for seconds in rng:
    flted_rng.append([])
    flted_rng[-1].append(flted[seconds[0]:seconds[1]])

############################################
#                                          #
#            FOURIER TRANSFORM             #
#                                          #
############################################

'''
Complete filtered dataset transformation
'''
# fourier transform for complete data
freq_all = abs(2 * np.fft.fft(flted))/len(flted)

# cut spectrum half
freq_all = freq_all[:len(freq_all)/2]

# create time frequency axis (for complete data)
x_freq_all = [i/float(5) for i in range(len(freq_all))]


'''
Dataset transformation in specified ranges
'''

# store data transformed to power spectrum
freq = []
# and x axis labels
x_freq = []

for bound_num in range(len(flted_rng)):

    freq_tmp = abs(
        2 * np.fft.fft(flted_rng[bound_num])
        )/sec_num[bound_num]*fs

    freq_tmp = freq_tmp[0]

    # cut spectrum half
    freq_tmp = freq_tmp[:len(freq_tmp)/2]
    print(freq_tmp)

    freq.append(freq_tmp)

    # create time frequency axis
    x_freq.append(
        [i/float(sec_num[bound_num]) for i in range(len(freq_tmp))]
        )


############################################
#                                          #
#             PLOTTING DATA                #
#                                          #
############################################

num_of_plots = len(rng_in_sec) + 3
colors = ['-b', '-r', '-g', '-k', '-y', '-m', '-c']

# required for plotting with an appropriate x axis (in seconds not samples)
x_time = [i/fs for i in range(len(flted))]
# filtered signal time domain plot
plt.subplot(num_of_plots, 1, 1)
plt.title('signal time domain')
plt.plot(x_time, flted)

# frequency domain of the signal (power spectrum) plot
plt.subplot(num_of_plots, 1, 2)
plt.title('signal power spectrum')
plt.plot(x_freq_all, freq_all)

for power_spec in range(len(freq)):
    # frequency domain of the signal (power spectrum) in range
    plt.subplot(num_of_plots, 1, power_spec + 3)
    plt.title(
        'signal power spectrum, seconds: ' +
        str(rng_in_sec[power_spec][0]) + ' to ' +
        str(rng_in_sec[power_spec][1]))
    plt.plot(x_freq[power_spec], freq[power_spec], colors[power_spec])
    plt.subplot(num_of_plots, 1, num_of_plots)
    plt.title('show power spectra of all ranges')
    plt.plot(x_freq[power_spec], freq[power_spec], colors[power_spec])

# plt.subplot(num_of_plots, 1, num_of_plots)
# plt.title('show power spectra of all ranges')
# plt.plot(x_freq[0], freq[0], '-r')

# tight layout was necesarry in my display to avoid overlapping
plt.tight_layout(h_pad=-1.2)
plt.show()

#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Filename: plot_frequency.py
File type: script

Plot frequency example
======================

Specify sampling rate and provide input filename, filters specification
as well as channels of interest list to plot the data in frequency domain.
Optonally, one may add time range (in seconds) to transform only part of the
signal.
"""

import matplotlib.pyplot as plt

from pyseeg.datasets import Dataset, fetch_ssvep


###############################################################################
# Set variables
# -------------
#
# Change the two variables (input_path and fs) to plot the data.
# Tip for OpenBCI: Cyton has sampling frequency of 250 and Ganglion: 200.

# Take the data from file. Get only one channel.
input_path = fetch_ssvep()

# Sampling frequency (how many samples are acquired per second).
fs = 250.0

# Select channels of interest (has to be list or tuple).
channels = [0, ]

# Specify n filters (two in this case).
filters = ({'type': 'bandstop', 'low': 49, 'high': 51},
           {'type': 'bandpass', 'low': 1, 'high': 50})

# If custom range is int, cut the leading k seconds of the signal. If custom
# range is list or tuple, take the range in seconds.
custom_range = [15, 25]


###############################################################################
# Read, filter and transform the data
# -----------------------------------
#

# Read the data as object.
ssvep = Dataset(input_path, fs, channels=channels, filters=filters,
                custom_range=custom_range)

# To filter and transform the data with fft (without plotting it) uncomment
# the line below. It is then available as ssvep.data and ssvep.transformed_data
# objects.
#
# ssvep.transform()

# To plot the data and show the plot.
ssvep.plot_transformed()
plt.show()

# Alternatively use an one-liner:
#
# ssvep.plot_transformed(show=True)

# If you want just plot the data (no need to inspect the data) use:
from pyseeg.datasets import plot_data
plot_data(input_path, fs, channels=channels, filters=filters,
          custom_range=custom_range,
          plot_dtype=['raw', 'filtered', 'transformed'], show=True)

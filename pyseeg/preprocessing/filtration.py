#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Filename: filtering.py
File type: module

Signal filtration utility
=========================

Filter your data freely.
"""

from scipy.signal import butter, lfilter


# Numerator (b) and denominator (a) polynomials of the IIR filter
def get_params(low, high, fs, btype, order=2):
    nyq = 0.5 * fs
    low = low / nyq
    high = high / nyq
    b, a = butter(order, [low, high], btype=btype)
    return b, a

############################################
# Butterworth bandstop filter
#
# Linear filter application
def butter_bandstop(data, lowstop, highstop, fs, order=2):
    b, a = get_params(lowstop, highstop, fs, order=order, btype='bandstop')
    y = lfilter(b, a, data)
    return y


# Linear filter application
def butter_bandpass(data, lowcut, highcut, fs, order=2):
    b, a = get_params(lowcut, highcut, fs, order=order, btype='pass')
    y = lfilter(b, a, data)
    return y
#
# End of Butterworth bandpass filter
############################################


############################################
# General filtering function
#
def lin_filter(data, fs, filter_info, order=2):
    low, high = filter_info['low'], filter_info['high']

    if filter_info['type'] == 'bandstop':
        data = butter_bandstop(data, low, high, fs, order)
    elif filter_info['type'] == 'bandpass':
        data = butter_bandpass(data, low, high, fs, order)

    return data
#
# End of General filtering function
############################################

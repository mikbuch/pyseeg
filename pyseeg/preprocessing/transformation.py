#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Filename: transformation.py
File type: module

Fourier transformation
======================

Transform to obtain frequency domain.
"""

import numpy as np
import scipy.signal as sig


############################################
# Fourier's transformation
#
def fft_transform(data, hamming=False):
    """Plot FFT-transformed data.

    Parameters
    ----------
    data : np.array or list
        (usually prefiltered) data

    """

    if hamming:
        frequency = 2 * abs(np.fft.fft(sig.hamming(len(data))*data, 256))/256.0

        # frequency = frequency[:len(frequency)/2]
    else:
        # Fourier transform.
        frequency = 2 * abs(np.fft.fft(data))/len(data)

        # Cut spectrum half.
        # frequency = frequency[:len(frequency)/2]

    return frequency
#
# End of Fourier's transformation
############################################

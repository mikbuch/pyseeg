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


############################################
# Fourier's transformation
#
def fft_transform(data):
    """Plot FFT-transformed data.

    Parameters
    ----------
    data : np.array or list
        (usually prefiltered) data

    """

    # Fourier transform.
    frequency = abs(2 * np.fft.fft(data))/len(data)

    # Cut spectrum half.
    frequency = frequency[:len(frequency)/2]

    return frequency
#
# End of Fourier's transformation
############################################

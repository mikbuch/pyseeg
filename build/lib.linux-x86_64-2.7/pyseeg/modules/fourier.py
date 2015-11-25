
'''
    Module for performing Fast Fourier Transform on the sample of data.

    Arguments:
        sample - list of data
        fs - sampling frequency - how many samples per second

    Returns:
        freq - data transformed to power spectrum
'''

import numpy as np


def transform(sample, fs):
    # perform fft
    freq = abs(2 * np.fft.fft(sample))/1*fs

    # cut spectrum half
    freq = freq[:len(freq)/2]

    freq = freq.tolist() 
    return freq

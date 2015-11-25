""" FFT and plot power spectrum
For quick getting data's power spectrum.
"""

import numpy as np
import matplotlib.pyplot as plt


def transform(data):
    '''
    data - usually prefiltered data
    '''

    # fourier transform
    frequency = abs(2 * np.fft.fft(data))/len(data)

    # cut spectrum half
    frequency = frequency[:len(frequency)/2]

    return frequency


def plot_frequency(frequency, fs):
    '''
    frequency - data fransformed with fft
    fs - sampling frequency
    '''

    # create time frequencyuency axis
    x_frequency = \
        [i/(len(frequency)/(float(fs)/2.)) for i in range(len(frequency))]

    plt.title('signal power spectrum')
    plt.plot(x_frequency, frequency)

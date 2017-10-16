""" FFT and plot power spectrum
For quick getting data's power spectrum.
"""

import numpy as np
import matplotlib.pyplot as plt


def _transform(data):
    """Plot FFT-transformed data.

    Parameters
    ----------
    data : np.array or list
        (usually prefiltered) data

    """

    # fourier transform
    frequency = abs(2 * np.fft.fft(data))/len(data)

    # cut spectrum half
    frequency = frequency[:len(frequency)/2]

    return frequency


def plot_frequency(data, fs, transform=True, custom_range=None,
                   color=None, show=True):
    """Plot FFT-transformed data.

    Parameters
    ----------
    data : np.array or list
        Waw data or already fransformed with fft.
    fs : int or float
        Sampling frequency.
    transform : bool
        Wheter to transform the data before plotting power spectrum or not.
    custom_range : int or list or tuple
        Crop the data (remove beginning or the end or both).
    color : str
        Color of the plotted function.
    show : bool
        Whether to show immediately after plotting or let the user decide
        when to plot.

    """

    if transform:
        data = _transform(data)

    if custom_range is not None:
        if isinstance(custom_range, int):
            data = data[custom_range:]
        else:
            data = data[custom_range[0]:custom_range[1]]

    # create time frequencyuency axis
    x_frequency = \
        [i/(len(data)/(float(fs)/2.)) for i in range(len(data))]

    plt.title('Signal power spectrum')

    if color is not None:
        plt.plot(x_frequency, data, color=color)
    else:
        plt.plot(x_frequency, data)

    if show:
        plt.show()

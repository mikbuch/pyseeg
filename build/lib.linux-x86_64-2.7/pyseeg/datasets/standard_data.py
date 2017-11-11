#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Filename: datsets.py
File type: module

Govern datasets
===============

With this file you can fetch datafiles adn create Datasets.
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pyseeg.preprocessing import lin_filter, fft_transform


"""
Define filters: bandpass and bandstop
-------------------------------------

This is required to generate filters parameters `on the run`.
"""


def fetch_ssvep(example_number=0):
    """Get the dataset.

    Parameters
    ----------
    channels : list (int)
    List of channes to be used. Default `None`. If `None` all channels
    will be used.

    Returns
    -------
    str
    Filepath of the dataset.
    """

    home_dir = os.environ['HOME']
    filepath = os.path.join(home_dir, 'eeg_data', 'OpenBCI',
                            'ssvep_example_%.2d.csv' % example_number)

    return filepath


class Dataset(object):

    def __init__(self, input_path, fs, channels=None, order=2,
                 filters=({'type': 'bandstop', 'low': 49., 'high': 51.},
                          {'type': 'bandpass', 'low': 5., 'high': 50.}),
                 custom_range=None):
        '''
        custom_range : int or list or tuple
            In seconds. Crop the data (remove beginning or the end or both).
        '''

        self.input_path = input_path
        self.channels = channels
        self.fs = float(fs)
        self.order = order
        self.filters = filters
        self.custom_range = custom_range

        # Before running either filtering or transformation both these
        # variables are of the type None.
        self.data = None
        self.filtered = None
        self.transformed = None

        # Read the data.
        self._get_data()

    def _get_data(self):
        self.data = pd.read_csv(self.input_path, header=None)
        if self.channels is not None:
            self.data = self.data[self.channels]
        self.x_time_axis = np.arange(len(self.data[0]))/self.fs

        print('Raw data: %s' % self.data.mean()[0])
        self.raw = self.data

    def filter(self):

        for flt in self.filters:
            # self.data = lin_filter(self.data, self.fs, flt, order=self.order)
            self.data = self.data.transform(lambda x: lin_filter(x, self.fs,
                                                        flt, order=self.order))

        if self.custom_range is not None:
            # When one value encountered, just remove the beginning, e.g.
            # to remove filter settling.
            if isinstance(self.custom_range, int):
                self.data = self.data[int(self.custom_range*self.fs):]
                self.raw = self.raw[int(self.custom_range*self.fs):]
                self.x_time_axis = self.x_time_axis[int(self.custom_range*
                                                        self.fs):]
            # Range in seconds.
            else:
                lo, hi = self.custom_range
                self.data = self.data[int(lo*self.fs): int(hi*self.fs)]
                self.raw = self.raw[int(lo*self.fs): int(hi*self.fs)]
                self.x_time_axis = self.x_time_axis[int(lo*self.fs):
                                                    int(hi*self.fs)]

        print('Filtered data: %s' % self.data.mean()[0])
        self.filtered = self.data

    def transform(self, filter_data=True):
        # Make sure that the signal is filtered. To transform unfiltered
        # data, pass filter_data as False.
        if filter_data and not isinstance(self.filtered, pd.DataFrame):
            self.filter()

        tmp = self.data.apply(lambda x: pd.Series(fft_transform(x)))
        del self.data
        self.data = tmp
        del tmp
        self.transformed = self.data
        print('Transformed data: %s' % self.data.mean()[0])

    def plot_transformed(self, color=None, show=True):
        """Plot FFT-transformed data.

        If the data were transformed before, just plot it. If no transformation
        took place, do it first.

        Parameters
        ----------
        self : np.array or list or panda's DataFrame
            Raw data or already fransformed with fft.
        fs : int or float
            Sampling frequency.
        color : str
            Color of the plotted function.
        show : bool
            Whether to show immediately after plotting or let the user decide
            when to plot.
        """

        # Data has to be filtered first.
        if self.filtered is None:
            self.filter()

        # Transform the data, if not already done.
        if self.transformed is None:
            self.transform()

        # Create X (frequency) axis.
        x_axis = [i/(len(self.data)/(float(self.fs)/2.))
                  for i in range(len(self.data))]

        plt.title('Signal power spectrum')

        if color is not None:
            plt.plot(x_axis, self.data, color=color)
        else:
            plt.plot(x_axis, self.data)

        if show:
            plt.show()


def plot_data(input_path, fs, channels, filters, custom_range,
              plot_dtype=['raw', 'filtered', 'transformed'], show=True):

    ds = Dataset(input_path, fs, channels=channels, filters=filters,
                 custom_range=custom_range)
    # Prepare the complete data regardless of the type to be plotted.
    ds.transform()
    for (i, pdt) in enumerate(plot_dtype):
        plt.subplot(len(plot_dtype), 1, i+1)
        if 'raw' in pdt:
            plt.plot(ds.x_time_axis, ds.raw[0])
        elif 'filtered' in pdt:
            plt.plot(ds.x_time_axis, ds.filtered[0])
        elif 'transformed' in pdt:
            # Create X (frequency) axis.
            x_axis = [i/(len(ds.data)/(float(ds.fs)/2.))
                      for i in range(len(ds.data))]
            plt.plot(x_axis, ds.data)
        plt.title(pdt)
        plt.tight_layout()
    if show:
        plt.show()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    name:
        filtration_specgram.py

'''

# remove two following lines if you are in the main folder of the repo
import sys
sys.path.append('..')

import numpy as np
import matplotlib.pyplot as plt
import argparse

from mpldatacursor import datacursor

from modules.read_csv import read
import modules.filterlib as flt
import modules.spectrogram as sg



from matplotlib import cbook

class DataCursor(object):
    """A simple data cursor widget that displays the x,y location of a
    matplotlib artist when it is selected."""
    def __init__(self, artists, tolerance=5, offsets=(-20, 20), 
                 template='x: %0.2f\ny: %0.2f', display_all=False):
        """Create the data cursor and connect it to the relevant figure.
        "artists" is the matplotlib artist or sequence of artists that will be 
            selected. 
        "tolerance" is the radius (in points) that the mouse click must be
            within to select the artist.
        "offsets" is a tuple of (x,y) offsets in points from the selected
            point to the displayed annotation box
        "template" is the format string to be used. Note: For compatibility
            with older versions of python, this uses the old-style (%) 
            formatting specification.
        "display_all" controls whether more than one annotation box will
            be shown if there are multiple axes.  Only one will be shown
            per-axis, regardless. 
        """
        self.template = template
        self.offsets = offsets
        self.display_all = display_all
        if not cbook.iterable(artists):
            artists = [artists]
        self.artists = artists
        self.axes = tuple(set(art.axes for art in self.artists))
        self.figures = tuple(set(ax.figure for ax in self.axes))

        self.annotations = {}
        for ax in self.axes:
            self.annotations[ax] = self.annotate(ax)

        for artist in self.artists:
            artist.set_picker(tolerance)
        for fig in self.figures:
            fig.canvas.mpl_connect('pick_event', self)

    def annotate(self, ax):
        """Draws and hides the annotation box for the given axis "ax"."""
        annotation = ax.annotate(self.template, xy=(0, 0), ha='right',
                xytext=self.offsets, textcoords='offset points', va='bottom',
                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.8),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
                )
        annotation.set_visible(False)
        return annotation

    def __call__(self, event):
        """Intended to be called through "mpl_connect"."""
        # Rather than trying to interpolate, just display the clicked coords
        # This will only be called if it's within "tolerance", anyway.
        x, y = event.mouseevent.xdata, event.mouseevent.ydata
        annotation = self.annotations[event.artist.axes]
        if x is not None:
            if not self.display_all:
                # Hide any other annotation boxes...
                for ann in self.annotations.values():
                    ann.set_visible(False)
            # Update the annotation in the current axis..
            annotation.xy = x, y
            annotation.set_text(self.template % (x, y))
            annotation.set_visible(True)
            event.canvas.draw()

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 22}

plt.rc('font', **font)

parser = argparse.ArgumentParser()
parser.add_argument("data_file")
args = parser.parse_args()


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
eeg_file = args.data_file

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

# required for futher plotting appropriate x axis (samples)
x_time = [i/fs for i in range(len(data))]

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

flted = flted_1_50_pass[350:16800]
ax1 = plt.subplot(2,1,1)
ax1.set_xlim([0, len(flted)])
a, = plt.plot(flted)
DataCursor([a,])
# plt.plot(flted)

############################################
#                                          #
#              SPECTROGRAM                 #
#                                          #
############################################
plt.subplot(2,1,2)
sg.spectrogram(flted, int(fs))

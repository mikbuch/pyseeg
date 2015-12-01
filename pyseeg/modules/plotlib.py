#!/usr/bin/env python

'''
    name:
        plottinglib.py

    description:
        Plotiing utility for pyseeg.
        Supports offline as well as real-time plotting.
'''

import time
from matplotlib import pyplot as plt

from pyseeg.modules.csvlib import read_csv
from pyseeg.modules.filterlib import filter_eeg


def plot_time(
        eeg_file, fs, channel,
        bandstop=(49, 51), bandpass=(1, 50), order=4,
        sec_remove=1, show=True
        ):

    data = read_csv(eeg_file, channel)

    # filter data using bandstop (first), and then bandpass filter
    filtered_data = filter_eeg(
        data, fs, bandstop=bandstop, bandpass=bandpass,
        order=order
        )

    filtered_data = filtered_data[fs*sec_remove:]

    plt.title('signal time domain after filtration')
    plt.plot(filtered_data)
    if show:
        plt.show()


def simulate_plot(data):
    """
    Display the simulation using matplotlib, using blit for speed
    Takes one argument:
        data_read - is the data read from file, the signal to be simulated
                    has to be 1D python list
    """
    data_read = list(data)

    # get figure and axis objects
    fig, ax = plt.subplots(1, 1)

    # x axis limit is set to the number of samples in simulated plot
    ax.set_xlim(0, len(data_read))
    ax.set_ylim(
        min(data_read) + 0.1*min(data_read),
        max(data_read) + 0.1*max(data_read)
        )
    ax.hold(True)

    data_plotted = []
    data_plotted.append(data_read.pop(0))

    plt.show(False)
    plt.draw()

    background = fig.canvas.copy_from_bbox(ax.bbox)

    signal = ax.plot(range(len(data_plotted)), data_plotted)[0]
    tic = time.time()

    for ii in xrange(len(data_read)):

        # update data
        data_plotted.append(data_read.pop(0))
        signal.set_data(range(len(data_plotted)), data_plotted)

        # restore background
        fig.canvas.restore_region(background)

        # redraw just the points
        ax.draw_artist(signal)

        # fill in the axes rectangle
        fig.canvas.blit(ax.bbox)

    plt.close(fig)
    print "average FPS: %.2f" % (len(data_plotted) / (time.time() - tic))


def simulate_optimal(data, samples_per_frame):

    data_read = list(data)
    samples_at_once = samples_per_frame

    # get figure and axis objects
    fig, ax = plt.subplots(1, 1)

    # x axis limit is set to the number of samples in simulated plot
    ax.set_xlim(0, len(data_read))
    ax.set_ylim(
        min(data_read) + 0.1*min(data_read),
        max(data_read) + 0.1*max(data_read)
        )
    ax.hold(True)

    data_plotted = []
    data_plotted.append(data_read.pop(0))

    plt.show(False)
    plt.draw()

    background = fig.canvas.copy_from_bbox(ax.bbox)

    signal = ax.plot(range(len(data_plotted)), data_plotted)[0]
    tic = time.time()

    for ii in xrange(len(data_read)):

        if ii % samples_at_once == 0:
            if len(data)-1-ii < samples_at_once:
                samples_at_once = len(data)-1-ii

            # update data
            for sample_stacked in range(samples_at_once):
                data_plotted.append(data_read.pop(0))
                signal.set_data(range(len(data_plotted)), data_plotted)

            # restore background
            fig.canvas.restore_region(background)

            # redraw just the points
            ax.draw_artist(signal)

            # fill in the axes rectangle
            fig.canvas.blit(ax.bbox)

            if samples_at_once < samples_per_frame:
                break

    plt.close(fig)
    print "average FPS: %.2f" % (len(data_plotted) / (time.time() - tic))


'''
    Online (real-time) plotter class.
    It is extended verions of the simulate_optimal() funciton.
    It handles real-time optimal (custom samples_per_frame) plotting.
    During creating the object that is an instance of this class:
        * you have to specify the number of samples_per_frame

   Example class object initialization:

        import modules.plotlib as pltmod

        prt = pltmod.OnlinePlot(samples_per_frame=2)
'''


class OnlinePlot(object):
    def __init__(self, samples_per_frame=1):
        self.samples_per_frame = samples_per_frame
        self.count_frames = 0
        self.fig, self.ax = plt.subplots(1, 1)

        # x axis limit is set to the 4 seconds of the OpenBCI signal
        self.ax.set_xlim(0, 250*5)
        self.ax.set_ylim(
            -250,
            250
            )
        self.ax.hold(True)

        self.data_plotted = [0]*5*250

        plt.show(False)
        plt.draw()

        self.background = self.fig.canvas.copy_from_bbox(self.ax.bbox)
        self.signal = self.ax.plot(
            range(len(self.data_plotted)),
            self.data_plotted)[0]
        self.tic = time.time()

    def frame_plot(self, sample):
        self.count_frames += 1

        # update data
        del(self.data_plotted[0])
        self.data_plotted.append(sample)

        if self.count_frames % self.samples_per_frame == 0:
            self.signal.set_data(
                range(len(self.data_plotted)), self.data_plotted
                )

            # restore background
            self.fig.canvas.restore_region(self.background)

            # redraw just the points
            self.ax.draw_artist(self.signal)

            # fill in the axes rectangle
            self.fig.canvas.blit(self.ax.bbox)

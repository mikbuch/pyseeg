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
from matplotlib import rc
import numpy as np

from pyseeg.modules.csvlib import read_csv
from pyseeg.modules.filterlib import filter_eeg


def plot_time(
        eeg_file, fs, channel,
        bandstop=(49, 51), bandpass=(1, 50), order=4,
        sec_remove=None, show=True, xticklabels='samples',
        title='Signal time domain after filtration',
        sec_range=None, ylim=None, threshold=None, linewidth=1.0
        ):
    '''
    This function has dual purpose: plotting eeg signal or visualising
    threshold detection line.

    sec_remove - remove first n seconde (e.g. for filter settling time)
    '''

    # in case someone passes float value (it has to be int for indexing)
    fs = int(fs)

    data = read_csv(eeg_file, channel=channel)

    if bandstop or bandpass:
        # filter data using bandstop (first), and then bandpass filter
        filtered_data = filter_eeg(
            data, fs, bandstop=bandstop, bandpass=bandpass,
            order=order
            )

        if sec_remove:
            filtered_data = filtered_data[int(fs*sec_remove):]
        elif sec_range:
            filtered_data = \
                filtered_data[int(fs*sec_range[0]):int(fs*sec_range[1])]

        data_plotted = filtered_data

    else:
        data_plotted = data

    if xticklabels == 'seconds':
        xlabel = 'Time [s]'
        if sec_range:
            x_axis = np.arange(
                0, len(data_plotted)/float(fs), 1/float(fs)
                ) + sec_range[0]
        else:
            x_axis = np.arange(0, len(data_plotted)/float(fs), 1/float(fs))
    else:
        xlabel = 'Sample number'
        x_axis = np.arange(0, len(data_plotted))

    fig, ax = plt.subplots()

    plt.plot(x_axis, data_plotted, linewidth=1.5, label='signal')


    ax.set_xlabel(xlabel, labelpad=15)
    ax.set_ylabel(r'microvolts [$\mu$V]', labelpad=20)


    if threshold:
        ax.text(
            x_axis[0]-0.12, 45, r'50',
            style='oblique', fontsize=30, color='red'
            )
        # draw threshold line
        plt.plot(
            (x_axis[0], x_axis[-1]),
            (threshold, threshold),
            'r-', linewidth=linewidth, label='threshold'
            )
        # change default title
        plt.title('Threshold Blink Detection', y=1.02)

    leg = plt.legend(bbox_to_anchor=(0.985, 0.14))
    llines = leg.get_lines()
    plt.setp(llines, linewidth=5)

    # set y axis boundries
    if ylim:
        plt.ylim(ylim)


    plt.rcParams.update({'font.size': 32})

    # show result
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
    print("average FPS: %.2f" % (len(data_plotted) / (time.time() - tic)))


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
    fig.canvas.draw()

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
    print("average FPS: %.2f" % (len(data_plotted) / (time.time() - tic)))


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

        # self.ax.draw(self.signal)

    def frame_plot(self, sample):
        self.count_frames += 1

        # update data
        del(self.data_plotted[0])
        self.data_plotted.append(sample)

        if self.count_frames % self.samples_per_frame == 0:
            self.signal.set_data(
                range(len(self.data_plotted)), self.data_plotted
                )

            # # restore background
            # self.fig.canvas.restore_region(self.background)

            # redraw just the points
            self.fig.canvas.draw()
            self.ax.draw_artist(self.signal)

            # fill in the axes rectangle
            self.fig.canvas.blit(self.ax.bbox)

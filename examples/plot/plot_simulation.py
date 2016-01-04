#!/usr/bin/env python

'''
    name:
        plot_simulation.py

    description:
        Simulate plotting data in real time.
        Uses already taken eeg data (stored in the file).
'''


from pyseeg.modules.csvlib import read_csv
import pyseeg.modules.plotlib as pltmod

############################################
#                                          #
#          GET DATA FROM FILE              #
#                                          #
############################################
'''
    If it were real-time the data would come directly from eeg.
    For the simulation purpose it has to be read from the file.
'''
# specify file with eeg data
eeg_file = '../example_data/blink_00.csv'

# get data form channel X
channel = 0

# read requested data form csv file
data = read_csv(eeg_file, channel)

'''
    simulate_plot()
        Plot one sample every frame

    simulate_optimal()
        Specify how many samples there are per one frame.
        Setting more samples per one frame increases FPS rate.
'''
if __name__ == '__main__':
    # pltmod.simulate_plot(data_read)
    pltmod.simulate_optimal(data, samples_per_frame=2)

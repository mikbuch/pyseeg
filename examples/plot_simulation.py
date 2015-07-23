#!/usr/bin/env python

'''
    name:
        plot_simulation.py

    description:
        Simulate plotting data in real time.
        Uses already taken eeg data (stored in the file).
'''

# remove two following lines if you are in the main folder of the repo
import sys
sys.path.append('..')

from modules.read_csv import read
import modules.plotlib as pltmod

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
eeg_file = '../data/flt_no_flt.txt'

# read the eeg file to the list
data_read = read(
    eeg_file, delimiter='\t', header=1, to_float=True, transpose=True
    )

data_read = data_read[1]

'''
    simulate_plot()
        Plot one sample every frame

    simulate_optimal()
        Specify how many samples there are per one frame.
        Setting more samples per one frame increases FPS rate.
'''
if __name__ == '__main__':
    # pltmod.simulate_plot(data_read)
    pltmod.simulate_optimal(data_read, 2)

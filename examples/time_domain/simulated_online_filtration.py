'''
    name:
        simulated_filter.py

    description:
        Simulate online filtering.
'''
import matplotlib.pyplot as plt

import pyseeg.modules.filterlib as flt
import pyseeg.modules.blink as blk

from pyseeg.modules.csvlib import read_csv

############################################
#                                          #
#         VARIABLES DECLATATION            #
#                                          #
############################################

# file with eeg data location
eeg_file = '../example_data/blink_00.csv'


############################################
#                                          #
#          GET DATA FROM FILE              #
#                                          #
############################################
'''
    If it were real-time the data would come directly from eeg.
    For the simulation purpose it has to be read from the file.
'''
# get data form channel X
channel = 0

# read requested data form csv file
data = read_csv(eeg_file, channel)


# TODO: delete it later
# ############################################
# #                                          #
# #               FILTERING                  #
# #                                          #
# ############################################
# # filter data using butt bandstop 49-51 Hz filter (50Hz)
# flted_50_stop = flt.butter_bandstop_filter(
    # data, lowstop, highstop, fs, order=2
    # )
# # filter prefiltered 50_stop data using 1-50 Hz bandpass filter
# flted_1_50_pass = flt.butter_bandpass_filter(
    # flted_50_stop, lowcut, highcut, fs, order=2
    # )


############################################
#                                          #
#   ONLINE FILTERING + BLINK DETECTION     #
#                                          #
############################################

frt = flt.FltRealTime()
brt = blk.BlinkRealTime()
signal_rt = []
for i in data:
    sample = frt.filterIIR(i,0)
    brt.blink_detect(sample, 50)
    signal_rt.append(sample)

plt.plot(data, '-g')
plt.plot(signal_rt, '-b')
plt.plot(brt.visual, '-r', linewidth=3.0)
plt.show()

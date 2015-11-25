'''
    name:
        simulated_filter.py

    description:
        Simulate online filtering.
'''

# remove two following lines if you are in the main folder of the repo
import sys
sys.path.append('..')

# import numpy as np
import matplotlib.pyplot as plt

from modules.read_csv import read
import modules.filterlib as flt
# import modules.spectrogram as sg
import modules.blink as blk

############################################
#                                          #
#         VARIABLES DECLATATION            #
#                                          #
############################################

# file with eeg data location
eeg_file = '../data/blink_00.csv'


############################################
#                                          #
#          GET DATA FROM FILE              #
#                                          #
############################################
'''
    If it were real-time the data would come directly from eeg.
    For the simulation purpose it has to be read from the file.
'''
# read the eeg file to the list
data = read(
    eeg_file, delimiter=',', header=1, to_float=True, transpose=True
    )

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

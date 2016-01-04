#!/usr/bin/env python

'''
    name:
        plot_online_simulation.py

    description:
        Offline simulator for preaquired data.
        It behaves almost like an online plotter with an EEG device running.
'''

import time

from pyseeg.modules.csvlib import read_csv
import pyseeg.modules.filterlib as flt
import pyseeg.modules.blink as blk
import pyseeg.modules.plotlib as pltmod


############################################
#                                          #
#  OPENBCI-LIKE CLASS FOR HANDLING SAMPLE  #
#                                          #
############################################
class OpenBCISample(object):
    '''
        Class for samples handling. Normally in openbci.py class.
        Here it is used to make code similar to those from openbci.
    '''
    def __init__(self, packet_id, channel_data, aux_data):
        self.id = packet_id
        self.channel_data = channel_data
        self.aux_data = aux_data


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

# read requested data
data = read_csv(eeg_file)


############################################
#                                          #
#       MAIN FUNCTION OF THE PROGRAM       #
#                                          #
############################################
# this function iterates x time in this simulator as well as in the openbci
def countBlinks(sample):

    # get sample form the first channel (index '0')
    smp = sample.channel_data[0]

    # filter fist sample (place in list with the index '0')
    smp_flted = frt.filterIIR(smp, 0)

    # detect all blinks (signal amplifications above 60uV)
    brt.blink_detect(smp_flted, 60)

    # report it the new blink is spotted
    if brt.new_blink:
        print(brt.blinks_num)

    # online plotting using matplotlib blit
    prt.frame_plot(smp_flted)


############################################
#                                          #
#      OBJECTS CREATION AND MAIN LOOP      #
#                                          #
############################################
if __name__ == '__main__':

    # filtering in real time object creation
    frt = flt.FltRealTime()

    # blink detection in real time object creation
    brt = blk.BlinkRealTime()

    # plotting in real time object creation
    prt = pltmod.OnlinePlot(samples_per_frame=2)

    # iterate trough EEG data samples read form the file
    for channel_sample in data:
        # create sample using openbci-like class
        sample = OpenBCISample(0, channel_sample, [0, 0, 0])
        # filtering the data sample, detecting all blinks and ploting it
        countBlinks(sample)

    # some benchmark utilities
    print(
        "number of frames: %.2f" % (prt.count_frames)
        )

    print(
        "time elapsed: %.2f sec" % (time.time() - prt.tic)
        )

    print(
        "average FPS: %.2f" % (prt.count_frames / (time.time() - prt.tic))
        )

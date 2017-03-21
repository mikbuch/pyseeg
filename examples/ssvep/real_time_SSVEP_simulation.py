#!/usr/bin/env python

'''
name: real_time_SSVEP_simulation.py
type: script
description:
    Offline simulator for preaquired data. It allows detecting SSVEPs in
    the signal provided by the simulator.
'''

import time

from pyseeg.modules.csvlib import read_csv
import pyseeg.modules.filterlib as flt
import pyseeg.modules.blink as blk
import pyseeg.modules.ssveplib as slt



###############################################################################
# OpenBCI-like class for handling sample

class OpenBCISample(object):
    '''
        Class for samples handling. Normally in openbci.py class.
        Here it is used to make code similar to those from openbci.
    '''
    def __init__(self, packet_id, channel_data, aux_data):
        self.id = packet_id
        self.channel_data = channel_data
        self.aux_data = aux_data


###############################################################################
# Get the data to be simulated from file
'''
    If it were real-time the data would come directly from eeg.
    For the simulation purpose it has to be read from the file.
'''
# Specify file with eeg data.
eeg_file = '../example_data/blink_00.csv'

# Read requested data.
data = read_csv(eeg_file)


###############################################################################
# Main function of the program       #

###############################################################################
# [Child process] Objects creation and main loop

# Define a function to run as the background process (foreground will be the
# graphical interface.
def func_ssvep_det(ssvep_state):
    def handle_sample(sample):

        # get data point (value) form the first channel (index '0')
        smp = sample.channel_data[channel]

        # filter fist sample (place in list with the index '0')
        smp_flted = frt.filterIIR(smp, 0)

        # detect ssvep state (which stimulus is the subject looking at)
        ssvep_state = srt.ssvep_detect(smp_flted)
        # srt.ssvep_detect(smp_flted, 95)

        # quit_program program, stop and disconnect board
        if quit_program.is_set():
            print('Disconnect signal sent...')
            board.disconnect()

        # It can even simulate saving
        with open(csv_filename, 'at') as f:
            save = csv.writer(f)
            save.writerow([smp, smp_flted, srt.ssvep_state])
            # save.writerow([sample.id] + sample.channel_data)

    if __name__ == '__main__':

        # filtering in real time object creation
        frt = flt.FltRealTime()

        # blink detection in real time object creation
        srt = slt.SSVEPRealTime(window_kind='nooverlap', window_len=1000)

        print('modules for OpenBCI real time set...')

        port = '/dev/ttyUSB0'
        baud = 115200
        board = bci.OpenBCIBoard(port=port, baud=baud)
        print('starting streaming...')
        board.start_streaming(plotData)
        board.disconnect()


# Multiprocessin events, values and queues
ssvep_state = mp.Value('i', 0)
connected = mp.Event()
quit_program = mp.Event()

# define process
proc_ssvep_det = mp.Process(name='proc_',
                            target=func_ssvep_det,
                            args=(ssvep_state,))

# start process
# proc_ssvep_det.start()
print('subprocess started')


###############################################################################
# [Paretn process] SSVEP GUI and stimuli section 

# Create a window.
# For configuring and debugging the code turn off full screen (set to False).
fullscr = False
win = visual.Window([1200,1000],
                    monitor="testMonitor",
                    units="deg",
                    fullscr=fullscr)
win.setMouseVisible(False)

# Sinusoidal control version.
freq_one = 0.5
freq_two = 1.5
# Colors of the rectangles.
color_one = 'red'
color_two = 'green'
# Positions of the rectanges.
pos_one = (-7, 0)
pos_two = (7, 0)


start = core.getTime()
cnt = 0
while cnt<600:
    second = core.getTime() - start

    sin_val_one = 0.5+0.5*np.sin(2 * np.pi * second * float(freq_one))
    sin_val_two = 0.5+0.5*np.sin(2 * np.pi * second * float(freq_two))
    
    rect_one = visual.Rect(win=win,
                           fillColor=color_one,
                           lineColor=color_one, 
                           size=20,
                           pos=pos_one,
                           opacity=sin_val_one)

    rect_two = visual.Rect(win=win,
                           fillColor=color_two,
                           lineColor=color_two, 
                           size=20,
                           pos=pos_two,
                           opacity=sin_val_two)

    rect_one.draw()
    rect_two.draw()
    win.flip()
    cnt += 1

win.close()
# Finish the child process as well.
quit_program.set()

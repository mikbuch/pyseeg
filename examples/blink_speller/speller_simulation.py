'''
name:
speller_simulation.py

type:
script

Simulates eeg/eog based speller. Here instead of blinks we have space bar
as trigger.
'''

import csv
import datetime
import time
from os.path import join

import multiprocessing as mp
from psychopy import visual, event, core

import pyseeg.modules.spellerlib as spell
# import pyseeg.modules.plotlib as pltmod


###############################################################################
#
#   VARIABLES, PATHS, CONFIGURATION
#
###############################################################################

# MAIN CHANNEL
channel = 0

subject_code = 'simulator_test'
# text_target = 'YELLOW_ZEBRA'
text_target = 'ORANGE_JUICE'

timecode = datetime.datetime.now().strftime("%Y%m%d%H%M")
log_filename = join(subject_code + '_' + timecode + '_output.csv')

############################################
#                                          #
#             SPELLER SECTION              #
#                                          #
############################################

quit_program = mp.Event()

# time elapsed until row/column switches
exposition_time = 0.5

# Color of the text to display (foreground) and the background.
fg_color='white'
bg_color='black'

# store typed text in string variable
text_typed = ''

# object generating table with the letters
generator = spell.TablesGenerator(pos=(500, 0), bg_color=bg_color, fg_color=fg_color)

# generate rows tables
rows = generator.rows_generate()
# generate cols tables
cols = generator.cols_generate()

# generate rows tables for PschoPy display
rows_stim = generator.rows_stim_generate()
# generate cols tables for PschoPy display
cols_stim = generator.cols_stim_generate()

# stim for typed text display
text_target_stim = visual.TextStim(
    generator.win_main, text='Text target:\n' + text_target,
    font='Monospace', pos=(0, 325), height=40, wrapWidth=600,
    color=fg_color
    )

# set time point before main loop of the program
time_begin = time.time()

# main loop. Only delete allows to escape it
# TODO: repair this. Typling delete doesn't break the loop
# TODO: latency time after previous decision
while not quit_program.is_set():
    # stim for typed text display
    text_typed_stim = visual.TextStim(
        generator.win_main, text='Text typed:\n' + text_typed,
        font='Monospace', pos=(0, -300), height=40, wrapWidth=600,
        color=fg_color
        )
    # get the time to furter reference as time of the last decision
    last_time = time.time()
    row = 0
    rows_stim[row].draw()
    text_typed_stim.draw()
    text_target_stim.draw()
    generator.win_main.flip()

    # get the time of the previous decision
    last_time = time.time()
    # blink presence flag
    blink_present = False
    # rows display loop. Awaits for the decision (typed space)
    while not blink_present and not quit_program.is_set():
        if 'delete' in event.getKeys() or text_typed == text_target:
            print('quitting')
            quit_program.set()
            generator.win_main.close()
            print('main window closed')
            break
        if time.time() - last_time > exposition_time:
            if row > 3:
                row = -1
            row += 1

            rows_stim[row].draw()
            text_typed_stim.draw()
            text_target_stim.draw()
            generator.win_main.flip()

            # get the time of the previous decision
            last_time = time.time()
        if 'space' in event.getKeys():
            blink_present = True

    if quit_program.is_set():
        break

    # clear the flag
    blink_present = False

    # get the time of the previous decision
    last_time = time.time()
    col = 0
    cols_stim[row][col].draw()
    text_typed_stim.draw()
    text_target_stim.draw()
    generator.win_main.flip()

    last_time = time.time()

    # rows display loop. Awaits for the decision (typed space)
    while not blink_present and not quit_program.is_set():
        if 'delete' in event.getKeys() or text_typed == text_target:
            print('quitting')
            quit_program.set()
            core.quit()
            generator.win_main.close()
            print('main window closed')
            break
        if time.time() - last_time > exposition_time:
            if col > 3:
                col = -1
            col += 1

            cols_stim[row][col].draw()
            text_typed_stim.draw()
            text_target_stim.draw()
            generator.win_main.flip()

            last_time = time.time()

        if 'space' in event.getKeys():
            blink_present = True

    # clear the flag
    blink_present = False

    # delete last char in the typed_text variable
    if row == 4 and col == 4:
        text_typed = text_typed[:-1]
        # console interface issue, feedback
        print('[backspace]')
        with open(log_filename, 'at') as f:
            save = csv.writer(f)
            save.writerow(['[backspace]'])

    # insert space to the typed_text variable
    elif row == 4 and col == 3:
        text_typed += '_'
        # console interface issue, feedback
        print('[space]')
        with open(log_filename, 'at') as f:
            save = csv.writer(f)
            save.writerow(['[space]'])

    # insert choosed letter to the typed_text variable
    else:
        text_typed += cols[row][col][row*2+1][col*4+2]
        # console interface issue, feedback
        print(cols[row][col][row*2+1][col*4+2])
        with open(log_filename, 'at') as f:
            save = csv.writer(f)
            save.writerow(cols[row][col][row*2+1][col*4+2])


import os

print "-- will kill"
pid = os.getpid()
print "-- pid:", pid
os.kill(pid, 1)
print "-- did kill"

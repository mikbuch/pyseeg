#!/usr/bin/env python2

'''
'''

# remove two following lines if you are in the main folder of the repo
import sys
sys.path.append('../..')

from psychopy import visual, event, core
import time

import modules.spellerlib as spell

# store typed text in string variable
text_typed = 'Typed text:\n'

# object generating table with the letters
generator = spell.TablesGenerator()

# generate rows tables
rows = generator.rows_generate()
# generate cols tables
cols = generator.cols_generate()

# generate rows tables for PschoPy display
rows_stim = generator.rows_stim_generate()
# generate cols tables for PschoPy display
cols_stim = generator.cols_stim_generate()

# main loop. Only delete allows to escape it
# TODO: repair this. Typling delete doesn't break the loop
# TODO: latency time after previous decision
while 'delete' not in event.getKeys():
    # stim for typed text display
    text_typed_stim = visual.TextStim(
        generator.win_main, text=text_typed,
        font='Monospace', pos=(0,-300), height='40', wrapWidth=600
        )
    # get the time to furter reference as time of the last decision
    last_time = time.time()
    row = 0
    rows_stim[row].draw()
    text_typed_stim.draw()
    generator.win_main.flip()

    # get the time of the previous decision
    last_time = time.time()
    # rows display loop. Awaits for the decision (typed space)
    # while 'space' not in event.getKeys():
    while len(event.getKeys())==0:

        if time.time() - last_time > 2:
            if row > 3:
                row = -1
            row += 1

            rows_stim[row].draw()
            text_typed_stim.draw()
            generator.win_main.flip()

            # get the time of the previous decision
            last_time = time.time()


    # get the time of the previous decision
    last_time = time.time()
    col = 0
    cols_stim[row][col].draw()
    text_typed_stim.draw()
    generator.win_main.flip()

    last_time = time.time()
    # rows display loop. Awaits for the decision (typed space)
    while 'space' not in event.getKeys():
        if time.time() - last_time > 2:
            if col > 3:
                col = -1
            col += 1

            cols_stim[row][col].draw()
            text_typed_stim.draw()
            generator.win_main.flip()

            last_time = time.time()

    # delete last char in the typed_text variable
    if row == 4 and col == 4:
        text_typed = text_typed[:-1]
        # console interface issue, feedback
        print('last char deleted')

    # insert space to the typed_text variable
    elif row == 4 and col == 3:
        text_typed += ' '
        # console interface issue, feedback
        print('[space]')

    # insert choosed letter to the typed_text variable
    else:
        text_typed += cols[row][col][row*2+1][col*4+2]
        # console interface issue, feedback
        print(cols[row][col][row*2+1][col*4+2])
        print(row)
        print(col)

# close the window after main loop ends
generator.win_main.close()

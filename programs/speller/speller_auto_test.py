#!/usr/bin/env python2

# TODO: create text field and insert there typed text

# remove two following lines if you are in the main folder of the repo
import sys
sys.path.append('..')

from psychopy import visual, event
import time

import modules.spellerlib as spell

text_typed = 'Typed text:\n'

generator = spell.TablesGenerator()

rows = generator.rows_generate()
cols = generator.cols_generate()

rows_stim = generator.rows_stim_generate()
cols_stim = generator.cols_stim_generate()

while 'delete' not in event.getKeys():
    text_typed_stim = visual.TextStim(
        generator.win_main, text=text_typed,
        font='Monospace', pos=(0,-300), height='40', wrapWidth=600
        )
    last_time = time.time()
    row = -1
    while 'space' not in event.getKeys():
        if time.time() - last_time > 2:
            if row > 3:
                row = -1
            row += 1

            rows_stim[row].draw()
            text_typed_stim.draw()
            generator.win_main.flip()

            last_time = time.time()

    last_time = time.time()
    col = -1
    while 'space' not in event.getKeys():
        if time.time() - last_time > 2:
            if col > 3:
                col = -1
            col += 1

            cols_stim[row][col].draw()
            text_typed_stim.draw()
            generator.win_main.flip()

            last_time = time.time()

    if row == 4 and col == 4:
        text_typed = text_typed[:-1]
        print('last char deleted')
    elif row == 4 and col == 3:
        text_typed += ' '
        print('[space]')
    else:
        text_typed += cols[row][col][row*2+1][col*4+2]
        print(cols[row][col][row*2+1][col*4+2])

generator.win_main.close()

import csv
import pyseeg.openbci.open_bci_v3 as bci
import datetime
import time

import multiprocessing as mp
from psychopy import visual, event, core

import pyseeg.modules.filterlib as flt
import pyseeg.modules.blink as blk
import pyseeg.modules.spellerlib as spell


output_dir = '../../../examples/example_data/'

# code the time to name file or variable
csv_filename = output_dir + \
    datetime.datetime.now().strftime("%Y%m%d%H%M") + \
    '.csv'


def func_blink_det(blink_det):
    def plotData(sample):

        # get sample form the first channel (index '0')
        smp = sample.channel_data[2]

        # filter fist sample (place in list with the index '0')
        smp_flted = frt.filterIIR(smp, 0)

        # detect all blinks (signal amplifications above 60uV)
        brt.blink_detect(smp_flted, 60)

        # report it the new blink is spotted
        if brt.new_blink:
            print(brt.blinks_num-1)
            if not brt.blinks_num == 1:
                blink_det.put(brt.blinks_num)
            else:
                connected.set()
                print('CONNECTED. Speller starts.')

        # # online plotting using matplotlib blit
        # prt.frame_plot(smp_flted)

        # quit_program program, stop and disconnect board
        if quit_program.is_set():
            print('Disconnect signal sent...')
            board.disconnect()

        with open(csv_filename, 'at') as f:
            save = csv.writer(f)
            save.writerow([smp, smp_flted, brt.blinks_num])
            # save.writerow([sample.id] + sample.channel_data)

    if __name__ == '__main__':

        # filtering in real time object creation
        frt = flt.FltRealTime()

        # blink detection in real time object creation
        brt = blk.BlinkRealTime()

        # plotting in real time object creation
        # prt = pltmod.OnlinePlot(samples_per_frame=2)

        port = '/dev/ttyUSB0'
        baud = 115200
        board = bci.OpenBCIBoard(port=port, baud=baud)
        print('starting streaming...')
        board.start_streaming(plotData)
        board.disconnect()


blink_det = mp.Queue()
connected = mp.Event()
quit_program = mp.Event()

proc_blink_det = mp.Process(
    name='proc_',
    target=func_blink_det,
    args=(blink_det,)
    )

print('subprocess started')
proc_blink_det.start()
# proc_blink_det.join())


############################################
#                                          #
#             SPELLER SECTION              #
#                                          #
############################################

# time elapsed until row/column switches
exposition_time = 0.5

# store typed text in string variable
text_typed = ''
goal = 'KILL'

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

# set time point before main loop of the program
time_begin = time.time()

# main loop. Only delete allows to escape it
# TODO: repair this. Typling delete doesn't break the loop
# TODO: latency time after previous decision
while not quit_program.is_set():
    print('main')
    # stim for typed text display
    text_typed_stim = visual.TextStim(
            generator.win_main, text='Text typed:\n' + text_typed,
        font='Monospace', pos=(0, -300), height='40', wrapWidth=600
        )
    # get the time to furter reference as time of the last decision
    last_time = time.time()
    row = 0
    rows_stim[row].draw()
    text_typed_stim.draw()
    generator.win_main.flip()

    # get the time of the previous decision
    last_time = time.time()
    # blink presence flag
    blink_present = False
    # rows display loop. Awaits for the decision (typed space)
    while not blink_present and not quit_program.is_set():
        if 'delete' in event.getKeys() or text_typed==goal:
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
            generator.win_main.flip()

            # get the time of the previous decision
            last_time = time.time()
        if not blink_det.empty():
            blink_present = True
            # to remove an object from the que
            blink_det.get()

    if quit_program.is_set():
        break

    # clear the flag
    blink_present = False

    # get the time of the previous decision
    last_time = time.time()
    col = 0
    cols_stim[row][col].draw()
    text_typed_stim.draw()
    generator.win_main.flip()

    last_time = time.time()

    # rows display loop. Awaits for the decision (typed space)
    while not blink_present and not quit_program.is_set():
        if 'delete' in event.getKeys() or text_typed==goal:
            print('quitting')
            quit_program.set()
            core.quit()
            generator.win_main.close()
            print('main window closed')
            break
        if time.time() - last_time >  exposition_time:
            if col > 3:
                col = -1
            col += 1

            cols_stim[row][col].draw()
            text_typed_stim.draw()
            generator.win_main.flip()

            last_time = time.time()
        if not blink_det.empty():
            blink_present = True
            # to remove an object from the que
            blink_det.get()

    # clear the flag
    blink_present = False

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

time_total = time.time() - time_begin
print('\n\n\nTotal time for this experiment: %f\n\n\n' % time_total)

print('main loop finished')

print('joining processes')
proc_blink_det.join()
print('processes joined successfully')


import os

print "-- will kill"
pid = os.getpid()
print "-- pid:", pid
os.kill(pid, 1)
print "-- did kill"

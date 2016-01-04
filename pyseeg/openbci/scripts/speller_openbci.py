import csv
import pyseeg.openbci.open_bci_v3 as bci
import datetime
import time

import multiprocessing as mp
from psychopy import visual, event, core

import pyseeg.modules.filterlib as flt
import pyseeg.modules.blink as blk
import pyseeg.modules.spellerlib as spell
# import pyseeg.modules.plotlib as pltmod


###############################################################################
#
#   VARIABLES, PATHS, CONFIGURATION
#
###############################################################################

# MAIN CHANNEL
channel = 0

output_dir = '../../../examples/example_data/'
log_dir = '../../../examples/logs/'

subject_code = 'MM'
# text_target = 'YELLOW_ZEBRA'
text_target = 'ORANGE_JUICE'

# code the time to name file or variable
csv_filename = \
    output_dir + \
    subject_code + '_' + \
    datetime.datetime.now().strftime("%Y%m%d%H%M") + \
    '.csv'

log_filename = \
    log_dir + \
    subject_code + '_' + \
    datetime.datetime.now().strftime("%Y%m%d%H%M") + \
    '.csv'




###############################################################################
#
#   OPENBCI DATA AQUIRING PROCESS (BACKGROUND PROCESS)
#
###############################################################################

def func_blink_det(blink_det, blinks_num):
    def plotData(sample):

        # get sample form the first channel (index '0')
        smp = sample.channel_data[channel]

        # filter fist sample (place in list with the index '0')
        smp_flted = frt.filterIIR(smp, 0)

        # detect all blinks (signal amplifications above 60uV)
        brt.blink_detect(smp_flted, 60)

        # report it the new blink is spotted
        if brt.new_blink:
            if brt.blinks_num == 1:
                # First detected blink is in fact artifact from filter
                # settling. Correct blink number by subtracting 1.
                # First "blink" successfully detected - device is connected.
                connected.set()
                print('CONNECTED. Speller starts detecting blinks.')
            else:
                blink_det.put(brt.blinks_num)
                blinks_num.value = brt.blinks_num
                print('BLINK!')

        # online plotting using matplotlib blit
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

        print('modules for OpenBCI real time set...')

        port = '/dev/ttyUSB0'
        baud = 115200
        board = bci.OpenBCIBoard(port=port, baud=baud)
        print('starting streaming...')
        board.start_streaming(plotData)
        board.disconnect()


blink_det = mp.Queue()
blinks_num = mp.Value('i', 0)
connected = mp.Event()
quit_program = mp.Event()

proc_blink_det = mp.Process(
    name='proc_',
    target=func_blink_det,
    args=(blink_det, blinks_num,)
    )

proc_blink_det.start()
print('subprocess started')
# proc_blink_det.join())


############################################
#                                          #
#             SPELLER SECTION              #
#                                          #
############################################


# wait for device to connect
print('Waiting for device to connect. Quit manually with delete key.')
while True:
    if 'delete' in event.getKeys():
        print('quitting')
        quit_program.set()
    elif connected.is_set():
        break


# time elapsed until row/column switches
exposition_time = 0.5

# store typed text in string variable
text_typed = ''

# object generating table with the letters
generator = spell.TablesGenerator(pos=(150, 150))

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
    font='Monospace', pos=(0, 325), height='40', wrapWidth=600
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
        font='Monospace', pos=(0, -300), height='40', wrapWidth=600
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

time_total = time.time() - time_begin
print('\n\n\nTotal time for this experiment: %f' % time_total)
print('Subject has blinked %d times\n\n\n' % (int(blinks_num.value) - 1))
with open(log_filename, 'at') as f:
    save = csv.writer(f)
    save.writerow([time_total, blinks_num.value - 1])
    print([time_total, blinks_num.value - 1])
print('main loop finished')

print('joining processes')
proc_blink_det.join()
time.sleep(2)
print('processes joined successfully')


import os

print "-- will kill"
pid = os.getpid()
print "-- pid:", pid
os.kill(pid, 1)
print "-- did kill"

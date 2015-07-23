import sys
sys.path.append('..')
sys.path.append('../..')

import csv
import datetime

import open_bci_v3 as bci
import modules.filterlib as flt
import modules.blink as blk

output_dir = '../../data/'

# code the time to name file or variable
csv_filename = output_dir + \
    datetime.datetime.now().strftime("%Y%m%d%H%M") + \
    '.csv'


def countBlinks(sample):

    smp = sample.channel_data[0]

    smp_flted = frt.filterIIR(smp, 0)
    brt.blink_detect(smp_flted, 60)

    print(brt.blinks_num)

    with open(csv_filename, 'at') as f:
        save = csv.writer(f)
        save.writerow(smp + [smp_flted, brt.visual[-1], brt.blinks_num])

if __name__ == '__main__':
    # filtering in real time object
    frt = flt.FltRealTime()
    # blink  detection in real time object
    brt = blk.BlinkRealTime()
    port = '/dev/ttyUSB0'
    baud = 115200
    board = bci.OpenBCIBoard(port=port)
    board.start_streaming(countBlinks)

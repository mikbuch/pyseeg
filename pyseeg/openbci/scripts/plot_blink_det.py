import sys
import csv
sys.path.append('..')
sys.path.append('../..')
import open_bci_v3 as bci
import datetime

import modules.filterlib as flt
import modules.blink as blk
import modules.plotlib as pltmod

output_dir = '../../../examples/example_data/'

# code the time to name file or variable
csv_filename = output_dir + \
    datetime.datetime.now().strftime("%Y%m%d%H%M") + \
    '.csv'


def plotData(sample):

    # get sample form the first channel (index '0')
    smp = sample.channel_data[0]

    # filter fist sample (place in list with the index '0')
    smp_flted = frt.filterIIR(smp, 0)

    # detect all blinks (signal amplifications above 60uV)
    brt.blink_detect(smp_flted, 60)

    # report it the new blink is spotted
    # if brt.new_blink:
        # print(brt.blinks_num)

    # online plotting using matplotlib blit
    prt.frame_plot(smp_flted)

    with open(csv_filename, 'at') as f:
        save = csv.writer(f)
        # save.writerow([smp, smp_flted, brt.blinks_num])
        save.writerow([sample.id] + sample.channel_data)


if __name__ == '__main__':

    # filtering in real time object creation
    frt = flt.FltRealTime()

    # blink detection in real time object creation
    brt = blk.BlinkRealTime()

    # plotting in real time object creation
    prt = pltmod.OnlinePlot(samples_per_frame=2)

    port = '/dev/ttyUSB0'
    baud = 115200
    board = bci.OpenBCIBoard(port=port)
    board.start_streaming(plotData)

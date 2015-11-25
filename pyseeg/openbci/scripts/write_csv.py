import pyseeg.openbci.open_bci_v3 as bci
import csv
import datetime

output_dir = '../../../examples/example_data/'

# code the time to name file or variable
csv_filename = output_dir + \
    datetime.datetime.now().strftime("%Y%m%d%H%M") + \
    '.csv'


def printData(sample):
    print "----------------"
#     print("%f" %(sample.id))
#     print sample.channel_data
    print sample.channel_data[0]
#     print sample.aux_data
    print "----------------"
    with open(csv_filename, 'at') as f:
        save = csv.writer(f)
        save.writerow(sample.channel_data)
        # save.writerow([sample.id] + sample.channel_data)

if __name__ == '__main__':
    port = '/dev/ttyUSB1'
    baud = 115200
    board = bci.OpenBCIBoard(port=port)
    board.start_streaming(printData)

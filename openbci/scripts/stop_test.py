import sys
sys.path.append('..')
import open_bci_v3 as bci
import multiprocessing as mp
import csv
import datetime
import time
import os

output_dir = '../../data/'

# code the time to name file or variable
csv_filename = output_dir + \
    datetime.datetime.now().strftime("%Y%m%d%H%M") + \
    '.csv'


def proc_print(e, pid):
    pid.put(os.getpid())
    def writeData(sample):
        with open(csv_filename, 'at') as f:
            save = csv.writer(f)
            save.writerow(sample.channel_data)
            # save.writerow([sample.id] + sample.channel_data)
        if stop_stream.is_set():
            board.disconnect()

        # print "----------------"
        # print("%f" %(sample.id))
        # print sample.channel_data[0]
        # print sample.aux_data
        # print "----------------"

    if __name__ == '__main__':
        port = '/dev/ttyUSB0'
        # baud = 115200
        board = bci.OpenBCIBoard(port=port)
        board.start_streaming(writeData)


# flag for stopping streaming
stop_stream = mp.Event()

pid = mp.Queue()

# child process to record eeg data
openbci_print = mp.Process(
    name='block',
    target=proc_print,
    args=(stop_stream, pid))

# start openbci writing
openbci_print.start()

time.sleep(10)
# press enter to finish program
raw_input("Press Enter to stop writing...")
stop_stream.set()
pid_child = pid.get()
print(pid_child)
os.kill(pid_child, 0)

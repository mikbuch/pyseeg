'''
name: csvlib.py
type: module

Read csv file to get data from all channels or just one specified.
'''

import csv


def read_csv(eeg_file, channel=None, delimiter=',', mode='r', quotechar='|'):
    data = []
    # read the eeg file to the list
    with open(eeg_file, mode=mode) as f:
        csvread = csv.reader(f, delimiter=delimiter, quotechar=quotechar)
        for sample in csvread:
            if channel is None:
                data.append([float(i) for i in sample])
            else:
                data.append(float(sample[channel]))
    return data

'''
'''

import csv


def read_csv(eeg_file, channel, delimiter=',', mode='rb', quotechar='|'):
    data = []
    # read the eeg file to the list
    with open(
            eeg_file, mode=mode, delimiter=delimiter, quotechar=quotechar
            ) as f:
        csvread = csv.reader(f)
        for sample in csvread:
            data.append(float(sample[channel]))

return data

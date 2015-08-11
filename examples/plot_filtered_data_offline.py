'''
    name:
        plot_filtered_data_offline.py
'''

import sys
sys.path.append('..')

import matplotlib.pyplot as plt

from modules.read_csv import read

# eeg_file = args.[0]
eeg_file = '../data/blink_00.csv'
# channel = args.[1] # default is 0
channel = 0
data = read(eeg_file)
# filter_data(data)
plt.plot(data[channel])
plt.show()

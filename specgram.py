#! /usr/bin/python

import sys
import collections
import json
import numpy as np
import matplotlib.pyplot as plt

config = {}
eegdata, channels = (collections.OrderedDict() for i in range(2))
for line in open(sys.argv[1]):
	f = line.rstrip().split(None, 3)
	if len(channels) == 0 and f[1] == '/muse/config':
		config = json.loads(f[3].strip("'"))
		for i, ch in enumerate(config['eeg_channel_layout'].split()):
			channels[ch] = i
	elif f[1] == '/muse/eeg':
		eegdata[f[0]] = [float(s) for s in f[3].split()]

sploc = { 'FP1':221, 'FP2':222, 'TP9':223, 'TP10':224 }
plt.figure(1)
for ch in channels.keys():
	plt.subplot(sploc[ch])
	plt.title(ch)
	chdata = np.array([eegdata[t][channels[ch]] for t in eegdata.keys()])
	plt.specgram(chdata - chdata.mean(),
				  NFFT=250, Fs=config['eeg_output_frequency_hz'])   
	plt.xlabel('Time (seconds)')
	plt.ylabel('Frequency (Hz)')
	plt.axis('tight')
	plt.ylim(0, 50)
plt.show()

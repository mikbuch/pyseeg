#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    name:
        eyes_closed.py
    # # #

    description:
        classify data as signal while eyes are closed or open

'''

# remove two following lines if you are in the main folder of the repo
import sys
sys.path.append('../..')

import matplotlib.pyplot as plt
import argparse
import numpy as np
from scipy import stats
import random

from modules.read_csv import read
import modules.filterlib as flt
import modules.spectrogram as sg
import modules.fourier as fourier


parser = argparse.ArgumentParser()
parser.add_argument("data_file")
args = parser.parse_args()

############################################
#                                          #
#           VARIABLES INIT                 #
#                                          #
############################################
# sampling frequency (how many samples per second)
fs = 250.0

# bandpass values
lowcut = 1.0
highcut = 50.0

# bandstop values
lowstop = 49.0
highstop = 51.0

# file with eeg data location
eeg_file = args.data_file


############################################
#                                          #
#          GET DATA FROM FILE              #
#                                          #
############################################
# read the eeg file to the list
data = read(
    eeg_file, delimiter=',', header=1, to_float=True, transpose=True
    )

# choose the channel (in this example its 1st channel - 0)
data = data[0]


############################################
#                                          #
#               FILTERING                  #
#                                          #
############################################
# filter data using butt bandstop 49-51 Hz filter (50Hz)
flted_50_stop = flt.butter_bandstop_filter(
    data, lowstop, highstop, fs, order=2
    )
# filter prefiltered 50_stop data using 1-50 Hz bandpass filter
flted_1_50_pass = flt.butter_bandpass_filter(
    flted_50_stop, lowcut, highcut, fs, order=2
    )

flted = flted_1_50_pass


############################################
#                                          #
#         GET TRAINING DATA SET            #
#                                          #
############################################

eyes_closed = []

alpha_ranges = [[11, 21], [30, 40], [52, 63]]

for sample in range(len(flted)):
    for rng in alpha_ranges:
        if sample >= rng[0]*fs and sample < rng[1]*fs:
            eyes_closed.append(flted[sample])


eyes_open = []

control_ranges = [[1, 10], [21, 29], [40, 51]]

for sample in range(len(flted)):
    for rng in control_ranges:
        if sample >= rng[0]*fs and sample < rng[1]*fs:
            eyes_open.append(flted[sample])


############################################
#                                          #
#              SPECTROGRAM                 #
#                                          #
############################################
# plt.subplot(2, 1, 1)
# plt.title('eyes_closed data spectrogram')
# sg.spectrogram(eyes_closed, int(fs), show_plot=False)
# plt.subplot(2, 1, 2)
# plt.title('eyes_open data spectrogram')
# sg.spectrogram(eyes_open, int(fs), show_plot=False)
# plt.show()


############################################
#                                          #
#     SPLIT DATA TO ONE SECOND PERIODS     #
#                                          #
############################################
'''
    Split complete data to one second periods.
    In this case every second consists of 250 samples.
    Take a second every half a second (to get more data for the network).
'''

alpha_data = []
for i in range(len(eyes_closed)):
    # if it is a new second or a new half part of the second
    if i % 125 == 0 and i < len(eyes_closed)-200:
        alpha_data.append(eyes_closed[i:i+250])

control_data = []
for i in range(len(eyes_open)):
    # if it is a new second or a new half part of the second
    if i % 125 == 0 and i < len(eyes_open)-200:
        control_data.append(eyes_open[i:i+250])

############################################
#                                          #
#             DEBUG SPLITTING              #
#                                          #
############################################
debug_alpha_even = []
debug_alpha_odd = []
for i in range(len(alpha_data)):
    if i % 2 == 0:
        debug_alpha_even += alpha_data[i]
    else:
        debug_alpha_odd += alpha_data[i]

debug_control_even = []
debug_control_odd = []
for i in range(len(control_data)):
    if i % 2 == 0:
        debug_control_even += control_data[i]
    else:
        debug_control_odd += control_data[i]

# plt.subplot(4, 1, 1)
# plt.title('eyes_closed odd spectrogram')
# sg.spectrogram(debug_alpha_odd, int(fs), show_plot=False)
# plt.subplot(4, 1, 2)
# plt.title('eyes_closed even spectrogram')
# sg.spectrogram(debug_alpha_even, int(fs), show_plot=False)
# plt.subplot(4, 1, 3)
# plt.title('eyes_open odd spectrogram')
# sg.spectrogram(debug_control_odd, int(fs), show_plot=False)
# plt.subplot(4, 1, 4)
# plt.title('eyes_open even spectrogram')
# sg.spectrogram(debug_control_even, int(fs), show_plot=False)
# plt.show()


############################################
#                                          #
# TRANSFORM ALL THE DATA SAMPLES USING FFT #
#                                          #
############################################

# contains X elements (depending on the number of samples).
alpha_freq = []

# transform all the data in the list using fft
# here by sample i mean a set of 250 'real' samples
for sample in alpha_data:
    # tmp = fourier.transform(sample, fs)
    # print(len(tmp))
    alpha_freq.append(fourier.transform(sample, fs))


# contains Y elements (depending on the number of samples).
control_freq = []

# transform all the data in the list using fft
# here by sample i mean a set of 250 'real' samples
for sample in control_data:
    control_freq.append(fourier.transform(sample, fs))


alpha_freq_trans = np.array(alpha_freq).T
control_freq_trans = np.array(control_freq).T
t_diff = []
for i in range(len(np.array(alpha_freq).T)):
    t_diff.append(
        stats.ttest_ind(alpha_freq_trans[i], control_freq_trans[i])
        )

t_scores = abs(np.array(t_diff).T[0])

# The most crucial thing: get the indexes of the highest values
ind = np.argsort(t_scores)

# Get 3 highest values (by index). The number 3 is arbitrary (heuristics)
val_high = 3
ind_high = ind[-3:]

#### MPL TESTING DELETE LATER ######
a_tmp = alpha_freq_trans[ind_high][:3]/1000
c_tmp = control_freq_trans[ind_high][:3]/1000
####################################

# Prepare the data for the network (for only 4 input nodes).
alpha_trn = alpha_freq_trans[ind_high]/1000
alpha_trn = alpha_trn.T.tolist()

for i in alpha_trn:
    i += [1.0, 0.0]


control_trn = control_freq_trans[ind_high]/1000
control_trn = control_trn.T.tolist()

for i in control_trn:
    i += [0.0, 1.0]


alpha_tst = []
for i in range(15):
    alpha_tst.append(alpha_trn.pop(random.randint(0, len(alpha_trn)-1)))

control_tst = []
for i in range(13):
    control_tst.append(control_trn.pop(random.randint(0, len(control_trn)-1)))

complete_trn = alpha_trn + control_trn
complete_tst = alpha_tst + control_tst

from pylab import figure, ioff, clf, contourf, ion, draw, show
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer

from pybrain.datasets import ClassificationDataSet, SequenceClassificationDataSet

trndata = ClassificationDataSet(val_high,2)
tstdata = ClassificationDataSet(val_high,2)

for i in complete_trn:
    # print(i[:val_high]),
    # print(i[-2:])
    trndata.addSample(i[:val_high], i[-2:])

for i in complete_tst:
    # print(i[:val_high]),
    # print(i[-2:])
    tstdata.addSample(i[:val_high], i[-2:])

# build a feed-forward network with 20 hidden units, plus
# a corresponding trainer
fnn = buildNetwork( trndata.indim, 10, trndata.outdim, outclass=SoftmaxLayer )
trainer = BackpropTrainer( fnn, dataset=trndata, momentum=0.1, verbose=True, weightdecay=0.01)

classtrn = np.array([[i] for i in np.array(complete_trn).T[3]])
classtst = np.array([[i] for i in np.array(complete_tst).T[3]])

# repeat 20 times
for i in range(20):
    # train the network for 1 epoch
    trainer.trainEpochs( 1 )

    # evaluate the result on the training and test data
    trnresult = percentError( trainer.testOnClassData(),
                              classtrn )
    tstresult = percentError( trainer.testOnClassData(
           dataset=tstdata ), classtst )

    # print the result
    print("epoch: %4d" % trainer.totalepochs, \
          "  train error: %5.2f%%" % trnresult, \
          "  test error: %5.2f%%" % tstresult)


from mpl_toolkits.mplot3d import Axes3D

def randrange(n, vmin, vmax):
    return (vmax-vmin)*np.random.rand(n) + vmin

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# n = 10
# for c, m, zl, zh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:

xs = a_tmp[0]
ys = a_tmp[1]
zs = a_tmp[2]
ax.scatter(xs, ys, zs, c='r', marker='o', s=100)

xs = c_tmp[0]
ys = c_tmp[1]
zs = c_tmp[2]
ax.scatter(xs, ys, zs, c='b', marker='^', s=100)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()

import neurolab as nl
input = np.array(complete_trn).T[:3].T
target = np.array(complete_trn).T[-2:].T
# target = np.array([[i[0]] for i in target.tolist()])


mn = input.min()
mx = input.max()
net = nl.net.newff([[mn, mx]]*len(input[0]), [12, 2])
err = net.train(input, target, show=1, epochs=1000)


tar = np.array([[i] for i in target.T[0]])
z = []
for i in complete_tst:
    i += net.sim([i[:3]]).tolist()[0]

classify = []
for i in complete_tst:
    classify.append(i[-4:])

tp = 0
for i in classify:
    if (i[0] == 1 and i[2] > i[3]) or (i[0] == 0 and i[2] < i[3]):
        tp +=1

print('\ntp: %d' % tp)
print('fp: %d' % (len(classify) - tp))
print('tp + fp: %d' % len(classify))
print('tp Rate: %f' % (tp / float(len(classify))))

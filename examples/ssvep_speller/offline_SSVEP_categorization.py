import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC

from pyseeg.modules.fft import transform

data_filepath = '../example_data/ssvep_02_4_stimuli.csv'
stimuli_filepath = '../example_data/ssvep_02_order.csv'

meta_data = np.loadtxt(data_filepath, delimiter=' ', comments='%')
stimuli_present = (meta_data.T[9]!=0.03)
stimuli_type = np.loadtxt(stimuli_filepath, delimiter=',')

fs = 250.

freqs = (10, 20, 30, 40) 
surround = 2

x_freq = np.array([i/(625./(float(fs)/2.)) for i in range(625)])

freq_idxs = []
for fq in freqs:
    fq_idx = np.argmin(np.abs(x_freq - fq))

    freq_idxs.append(range(fq_idx-1, fq_idx+2))


# plt.plot(stimuli_present)
# plt.ylim(-0.2, 1.2)
# plt.show()

stim_start = []
for i in range(1, len(stimuli_present)):
    if stimuli_present[i-1] == False and stimuli_present[i] == True:
        stim_start.append(i)

fs = 250.
n_types = np.unique(stimuli_type).shape[0]
n_stim = stimuli_type.shape[0]
stim_type_cnt = np.zeros(n_types).astype(int)

data_extracted = np.zeros((2, n_types, int(n_stim/n_types), int(fs*5)))

single_fft_shape = transform(np.random.rand(int(fs*5))).shape[0]
data_transformed = np.zeros(data_extracted.shape[:-1] + (single_fft_shape, ))

features = np.zeros((2, n_types, int(n_stim/n_types), n_types))


from pyseeg.modules.filterlib import filter_eeg
data = np.zeros((2, meta_data.shape[0]))

data[0] = filter_eeg(meta_data.T[1], fs, bandstop=(49, 51), bandpass=(1, 50))
data[1] = filter_eeg(meta_data.T[2], fs, bandstop=(49, 51), bandpass=(1, 50))

data[0] = meta_data.T[1]
data[1] = meta_data.T[2]


frequency_data = transform(data[1])

# plot data's power spectrum (transformed data)
from pyseeg.modules.fft import plot_frequency
plot_frequency(frequency_data, fs)
plt.show()



for (i, st) in enumerate(stimuli_type.astype(int)):

    st -= 1

    ind_b = stim_start[i]
    ind_e = stim_start[i]+1250

    # print('%s %s %s %s' % (st, ind_b, ind_e, stim_type_cnt))
    # print('%s %s %s %s %s' % (0, st, stim_type_cnt[st], ind_b, ind_e))

    ch1_raw = data[0][ind_b:ind_e]
    ch2_raw = data[1][ind_b:ind_e]

    data_extracted[0][st][stim_type_cnt[st]] = ch1_raw
    data_extracted[1][st][stim_type_cnt[st]] = ch2_raw

    ch1_trans = transform(ch1_raw)
    ch2_trans = transform(ch2_raw)

    data_transformed[0][st][stim_type_cnt[st]] = ch1_trans
    data_transformed[1][st][stim_type_cnt[st]] = ch2_trans

    for (j, fq) in enumerate(freq_idxs):

        features[0][st][stim_type_cnt[st]][j] = ch1_trans[fq].mean()
        features[1][st][stim_type_cnt[st]][j] = ch2_trans[fq].mean()


    stim_type_cnt[st] += 1



# Simplified test: one electrode, two conditions.
data_restricted = features[1, :2, :, :2].reshape(50, 2)
target = np.zeros(50)
target[:25] = np.ones(25)

X_train, X_test, y_train, y_test = train_test_split(data_restricted,
                                                    target)

cls = SVC()
cls.fit(X_train, y_train)
print(accuracy_score(y_test, cls.predict(X_test)))
print(y_test)

# plt.plot(x_freq, data_transformed[1, 0, :, :].mean(axis=0))
# plt.plot(x_freq, data_transformed[1, 1, :, :].mean(axis=0))
# plt.plot(x_freq, data_transformed[1, 2, :, :].mean(axis=0))
# plt.plot(x_freq, data_transformed[1, 3, :, :].mean(axis=0))
# plt.show()

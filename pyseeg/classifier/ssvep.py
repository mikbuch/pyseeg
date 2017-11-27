import numpy as np
from pyseeg.modules.fft import transform
from sklearn.cross_decomposition import CCA


class SSVEPRealTime(object):

    def __init__(self, fs, window_len, freqs, harmonics=0,
                 window_kind='nooverpal', cls_type='CCA'):
        '''
            fs (int or float) - sampling frequency
            window_len (int)  - length of a window (numer of samples to
                                analyze)
            freqs (int or floa) - requency ranges, the classifier has to know
                                  of which frequencies the choice has to be
                                  made
            window_kind (bool) - if two windows can contain the same samples
        '''

        self.fs = fs
        self.window_len = window_len
        self.window_kind = window_kind
        self.harmonics = harmonics
        self.cls_type = cls_type

        self.data = np.zeros(self.window_len)
        if 'CCA' in self.cls_type:
            # self.reference = (self.harmonics+1)*2
            self.reference = {}
            for freq in freqs:
                self.reference[str(int(freq))] = self._get_reference(freq)

        # For couning samples within window.
        self.cnt = 0

        self.freqs = freqs

        # We have to know which vector element to choose by frequency value,
        # not by the index of the vector.
        self.x_freq = np.array([i/(float(window_len)/(float(fs)/2.))
                                for i in range(window_len)])

        self.corrs = [0.0, 0.0]
        self.decision = 0
        # To mark the package at which classification occurs.
        self.win_end = False
        self.cca = CCA(n_components=1)

    def _get_reference(self, freq):

        ref = np.zeros((2*(self.harmonics+1), self.window_len))

        k = 0

        t = np.linspace(0, self.window_len/float(self.fs), self.window_len)

        for h in range(self.harmonics+1):
            k = h*2
            ref[k] = np.sin(freq*(h+1)*2*np.pi*t)
            ref[k+1] = np.cos(freq*(h+1)*2*np.pi*t)

        return ref.T

    def detect(self, smp):
        '''
            smp (float) - single, filtered sample
        '''

        self.data[self.cnt] = smp
        self.cnt += 1
        # To mark the package at which classification occurs.
        self.win_end = False

        if self.cnt == self.window_len:
            self.cnt = 0
            self.win_end = True

            if 'CCA' in self.cls_type:

                corrs = np.zeros(len(self.freqs))
                in_freq = np.zeros(2)

                for (i, freq) in enumerate(self.freqs):
                    for j in range(2):
                        self.data = self.data.reshape((self.window_len, 1))
                        self.cca.fit(self.data,
                                     self.reference[str(int(freq))].T[j])
                        U, V = self.cca.transform(self.data,
                                           self.reference[str(int(freq))].T[j])
                        corr = np.corrcoef(U.T, V)[0, 1]
                        in_freq[j] = abs(corr)
                    corrs[i] = in_freq[np.argmax(in_freq)]

                self.decision = np.argmax(corrs)
                self.corrs = corrs
                print('%s, corr: %.3f, %.3f' % (self.decision, corrs[0],
                                                corrs[1]))

            elif 'fft_ampl' in self.cls_type:

                data_fft = transform(self.data)

                # Mean frequency amplitude.
                mean_freqs = []

                for freq in self.freqs:
                    # Get the indices, values within +/-1 frequency value.
                    low_idx = np.argmin(np.abs(self.x_freq - freq)) - 1
                    hi_idx = np.argmin(np.abs(self.x_freq - freq)) + 1

                    mean_freqs.append(np.mean(data_fft[low_idx:hi_idx]))

                print(mean_freqs),
                self.decision = np.argmax(mean_freqs)
                print(self.decision)

        return self.win_end, self.decision

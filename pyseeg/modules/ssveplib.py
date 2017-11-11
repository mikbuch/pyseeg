import numpy as np
from pyseeg.modules.fft import _transform


class SSVEPRealTime(object):

    def __init__(self, fs, window_len, freqs, window_kind='nooverpal'):
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

        self.data = np.zeros(self.window_len)
        # For couning samples within window.
        self.cnt = 0

        self.freqs = freqs

        # We have to know which vector element to choose by frequency value,
        # not by the index of the vector.
        self.x_freq = np.array([i/(float(window_len)/(float(fs)/2.))
                                for i in range(window_len)])


        self.decision = 0

    def ssvep_detect(self, smp):
        '''
            smp (float) - single, filtered sample
        '''

        self.data[self.cnt] = smp
        self.cnt += 1

        if self.cnt == self.window_len:

            data_fft = _transform(self.data)

            # Mean frequency amplitude.
            mean_freqs = []

            for freq in self.freqs:
                # Get the indices, values within +/-1 frequency value.
                low_idx = np.argmin(np.abs(self.x_freq - freq)) - 1
                hi_idx = np.argmin(np.abs(self.x_freq - freq)) + 1

                mean_freqs.append(np.mean(data_fft[low_idx:hi_idx]))

            self.cnt = 0

            print(mean_freqs),
            self.decision = np.argmax(mean_freqs)
            print(self.decision)

        return self.decision

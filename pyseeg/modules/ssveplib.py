import numpy as np
from pyseeg.modules.fft import transform


class SSVEPRealTime(object):

    def __init__(self, fs, window_len, freq_ranges, window_kind='nooverpal'):
        
        self.fs = fs
        self.window_len = window_len
        self.window_kind = window_kind

        self.data = np.zeros(self.window_len)
        self.cnt = 0

        self.freq_ranges = freq_ranges

        self.x_freq = [i/window_len/(float(fs)/2.)) for i in range(window_len)]

        self.decision = 0
    

    def ssvep_detect(self, smp):

        self.data[self.cnt] = smp
        self.cnt += 1

        if self.cnt == self.window_len:

            data_fft = transform(self.data)

            mean_freqs = []

            freq_idxs = []
            for (low, hi) in freq_ranges:
                low_idx = np.argmin(np.abs(x_freq - low))
                hi_idx = np.argmin(np.abs(x_freq - hi))

                freq_idxs.append([low_idx, hi_idx])
            
            for idxs in freq_idxs:
                mean_freqs.append(data_ffs[idxs[0]:idxs[1]])
            
            self.cnt = 0

            self.decision = np.argmax(mean_freqs)

        return self.decision

    



    # def zzz(self):

        # print(self.data)


# srt = slt.SSVEPRealTime(window_kind='nooverlap', window_len=500, fs=250)
# srt.zzz()

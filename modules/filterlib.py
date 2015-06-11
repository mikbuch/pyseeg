from scipy.signal import butter, lfilter


# butterworth bandpass filter
def butter_bandpass(lowcut, highcut, fs, order=2):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=2):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


# butterworth bandstop filter
def butter_bandstop(lowstop, highstop, fs, order=2):
    nyq = 0.5 * fs
    low = lowstop / nyq
    high = highstop / nyq
    b, a = butter(order, [low, high], btype='bandstop')
    return b, a


def butter_bandstop_filter(data, lowstop, highstop, fs, order=2):
    b, a = butter_bandstop(lowstop, highstop, fs, order=order)
    y = lfilter(b, a, data)
    return y

import numpy as np


'''
    Detect blinks in the signal offline.

    Threshold approach: if any signal increase
    reaches the critical level - it is classified as blink.
    After classification as blink 0 must be crossed
    to classify next increase of the signal as blink.

    Parameters:
        * data - 1D list with the signal
        * thr - thresold above which the signal is considered blink

    Returns:
        * blink - 1D list with blinks visualised
        * blinks_num - number of blinks
'''


def blink_offline(data, thr, ommit=0):
    blink = np.zeros(len(data))
    blinks_num = 0
    zero_crossed = True
    prev_val = 0.0
    for i in range(len(data)):
        # ommiting first X samples. Suggested value is Fs.
        # Fist item has to be ommited anyway (data[i-i] comparison)
        if i > ommit:
            if data[i] > thr and prev_val <= thr \
                    and zero_crossed is True:
                blinks_num += 1
                if i < len(data)-2:
                    blink[i] = thr
                    blink[i+1] = -thr
                zero_crossed = False
            prev_val = data[i-1]
            if prev_val > 0.0 and data[i] <= 0.0:
                zero_crossed = True
    return blink, blinks_num


class BlinkRealTime(object):

    def __init__(self):
        self.blinks_num = 0
        self.new_blink = False
        self.zero_crossed = True
        self.prev_val = 0.0
        self.visual = np.array([])

    def blink_detect(self, value, thr):
        self.visual = np.append(self.visual, [0.0])

        # if there is no new blink detected then this is False
        self.new_blink = False

        if value > thr and self.prev_val <= thr \
                and self.zero_crossed is True:
            if (len(self.visual) > 2):
                # blink detected at this function call
                self.new_blink = True
                self.blinks_num += 1
                self.visual[-2] = thr
                self.visual[-1] = -thr
                self.zero_crossed = False

        if self.prev_val > 0.0 and value <= 0.0:
            self.zero_crossed = True

        self.prev_val = value

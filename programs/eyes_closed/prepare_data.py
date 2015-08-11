
# two following lanes are neccessery to import modules
import sys
sys.path.append('../..')

from modules.read_csv import read
import modules.filterlib as flt


class DataPreparation:
    def __init__(self, fs, data=None):
        self.data = data
        self.alpha_ranges = []
        self.control_ranges = []
        self.take_x_seconds = 1
        self.every_x_seconds = 0.5

    def getDataFromFile(self, input_file):
        # read the eeg file to the list
        data = read(
            input_file, delimiter=',', header=1,
            to_float=True, transpose=True
            )

        # choose the channel (in this example its 1st channel - 0)
        data = data[0]
        return data

    def filterData(
            self, data=None, bandstop=(49, 51), bandpass=(1, 50)
            ):
        if data is None:
            data = self.data
        filtered = flt.butter_bandstop_filter(
            data, bandstop[0], bandstop[1], self.fs, order=2
            )
        # filter prefiltered bandstop data using bandpass filter
        filtered = flt.butter_bandpass_filter(
            filtered, bandstop[0], bandstop[1], self.fs, order=2
            )

        return filtered

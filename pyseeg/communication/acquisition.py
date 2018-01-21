import csv
import datetime
import multiprocessing as mp
import pyseeg.openbci.open_bci_ganglion as bci
import os

import pyseeg.modules.filterlib as flt
import pyseeg.modules.ssveplib as svp


def record_data(stimuli, header=None, freqs=None, channel=0, output_path=None,
                port=None):

    # Define the process to run in background. It communicates with the parent
    # process via state and terminate variables.
    def mp_acquisition(state):
        print(' * acquisition * Feedback from within process.')
        print(' * acquisition * Current state: %s.' % state.value)
        print(' * acquisition * Acquisition will start soon.')

        # Callback function for OpenBCI class to handle samples.
        def handle_sample(sample):

            if freqs is not None:
                # Get data point (value) form the first channel (index '0').
                smp = sample.channel_data[channel]

                # Filter fist sample (place in list with the index '0').
                smp_flted = frt.filterIIR(smp, 0)

                # Detect ssvep state (stimulus is the subject looking at).
                ssvep_state = srt.ssvep_detect(smp_flted)

            # Let the inreface know that the data is streaming.
            if board.streaming:
                streaming.set()

            # Quit program, stop and disconnect board.
            if terminate.is_set():
                print(' * acquisition * Disconnect signal sent...')
                streaming.clear()
                board.disconnect()

            with open(output_path, 'at') as f:
                save = csv.writer(f)
                if freqs is not None:
                    save.writerow([sample.id, smp, smp_flted, ssvep_state])
                else:
                    save.writerow([sample.id] + sample.channel_data +
                                                                 [state.value])

        if freqs is not None:
            # Create an object for filtering in real-time.
            frt = flt.FltRealTime()

            # SSVEP detection in real-time.
            srt = svp.SSVEPRealTime(fs=250, window_len=250,
									freqs=freqs, window_kind='nooverlap')

        print(' * acquisition * Output file preparation...')
        if header is not None:
			with open(output_path, 'w') as f:
				save = csv.writer(f)
				save.writerow(header)

        print(' * acquisition * Modules for OpenBCI real time set...')

        board = bci.OpenBCIBoard(port=port)
        print(' * acquisition * Starting streaming...')
        board.start_streaming(handle_sample)
        board.disconnect()

    if output_path is None:
        # Define default timecode.
        home_dir = os.environ['HOME']
        time_code = datetime.datetime.today().strftime('%Y-%m-%d-%h-%s')
        output_path = os.path.join(home_dir, '%s.csv' % time_code)
    # Multiprocessing variables
    #
    # State tells which stimuli was active.
    state = mp.Value('i', 0)
    #
    # Flag to communicate the interface when to
    # to start stimuli display.
    streaming = mp.Event()
    #
    # The way to stop the data acquisition.
    terminate = mp.Event()

    # Define process.
    recorder = mp.Process(name='proc_acq', target=mp_acquisition,
                                                                 args=(state,))
    # Start process.
    recorder.start()
    print(' ! main ! Subprocess for recording started')


    ############################################
    # Stimuli reference
    #
    # State is shared between both objects.
    #
    stimuli.start_display(state, streaming, terminate)

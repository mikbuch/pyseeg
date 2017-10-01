import csv
import datetime
import multiprocessing as mp
import pyseeg.openbci.open_bci_ganglion as bci

def record_data(stimuli, output_path=None):

    # Define the process to run in background. It communicates with the parent
    # process via state and terminate variables.
    def mp_acquisition(state):
        print(' * acquisition * Feedback from within process.')
        print(' * acquisition * Current state: %s.' % state.value)
        print(' * acquisition * Acquisition will start soon.')

        # Callback function for OpenBCI class to handle samples.
        def handle_sample(sample):

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
                save.writerow([sample.id] + sample.channel_data +
                                                                 [state.value])

        print(' * acquisition * Modules for OpenBCI real time set...')

        board = bci.OpenBCIBoard()
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

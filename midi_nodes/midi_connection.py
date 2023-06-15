import threading

import os
import time
import ipdb

#os.environ["RTMIDI_API"] = "LINUX_ALSA"
import mido

class MIDIConnection:

    def __init__(self):
        self._listen_thread = None
        #FIXME
        self.note_on_data = {}
        self.note_aftertouch_data = {}
        pass

    def clearData(self):
        self.note_on_data = {}
        slef.note_aftertouch_data = {}

    def listen(self):
        if self._listen_thread:
            return
        # set device to listen on
        ipdb.set_trace()
        devices = mido.get_input_names()
        self._input_name = [name for name in devices if 'MPD' in name][0]
        print("MIDI INPUT:", self._input_name)
        # start thread
        self._listen_thread = threading.Thread(
                target=self._runListen)
        self._keep_running = True
        self._listen_thread.start()

    def stopListen(self):
        if self._listen_thread:
            self._keep_running = False
            self._listen_thread.join()
            self._listen_thread = None

    def _runListen(self):
        with mido.open_input(self._input_name) as midi_input:
            while self._keep_running:
                msg = midi_input.receive()
                if msg != None:
                    note = msg.note
                    if msg.type == 'note_on':
                        self._note_on_data[note] = msg.velocity
                    if msg.type == 'aftertouch':
                        self._note_aftertouch_data[note] = msg.value


midi_connection = MIDIConnection()

import threading

import os
import time

#os.environ["RTMIDI_API"] = "LINUX_ALSA"
import mido

class MIDIConnection:

    def __init__(self):
        self.encoding_mode = 'CHANNEL_AFTERTOUCH'
        self._listen_thread = None
        self._flag_get_teaching_pad = False
        self._teaching_pad = None
        # for CHANNEL_AFTERTOUCH
        self.id_to_value = {}


    def clearData(self):
        self.id_to_value = {}

    def listen(self):
        if self._listen_thread:
            return
        # set device to listen on
        devices = mido.get_input_names()
        print("DEVICES::::::", devices)
        self._input_name = [name for name in devices if 'MPD' in name][0]
        print("MIDI INPUT:", self._input_name)
        # start thread
        self._listen_thread = threading.Thread(
                target=self._runListen)
        self._keep_running = True
        self._listen_thread.start()

    def getTeachingPad(self):
        self._flag_get_teaching_pad = True
        while self._teaching_pad == None:
            time.sleep(0.1)
        teaching_pad = self._teaching_pad
        self._teaching_pad = None
        return teaching_pad

    def stopListen(self):
        if self._listen_thread:
            self._keep_running = False
            self._listen_thread.join()
            self._listen_thread = None

    def _runListen(self):
        with mido.open_input(self._input_name) as midi_input:
            while self._keep_running:
                msg = midi_input.receive()
                if msg:
                    cid = None
                    ctrl_type = ""
                    if msg.type == 'note_on':
                        ctrl_type = 'PAD'
                        if self.encoding_mode == 'CHANNEL_AFTERTOUCH':
                            cid = msg.channel
                        else:
                            cid = msg.note
                        self.id_to_value[cid] = msg.velocity
                    if msg.type == 'note_off':
                        ctrl_type = 'PAD'
                        if self.encoding_mode == 'CHANNEL_AFTERTOUCH':
                            cid = msg.channel
                        else:
                            cid = msg.note
                        self.id_to_value[cid] = msg.velocity
                    elif msg.type == 'aftertouch':
                        if self.encoding_mode == 'CHANNEL_AFTERTOUCH':
                            cid = msg.channel
                        self.id_to_value[cid] = msg.value
                    elif msg.type == 'control_change':
                        ctrl_type = 'CONTROL'
                        cid = msg.control + 100000
                        self.id_to_value[cid] = msg.value
                    # handle teaching mode
                    if self._flag_get_teaching_pad:
                        self._flag_get_teaching_pad = False
                        self._teaching_pad = (cid, ctrl_type)
                    print("PAD ID:", cid)


midi_connection = MIDIConnection()

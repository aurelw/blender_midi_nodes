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
        self.id_to_value_lock = threading.Lock()
        # misc config
        self._try_n_connects = 10


    def clearData(self):
        with self.id_to_value_lock:
            self.id_to_value = {}

    def listen(self):
        if self._listen_thread:
            return
        # set device to listen on
        is_connected = False
        for i in range(self._try_n_connects):
            try:
                devices = mido.get_input_names()
                self._input_name = [name for name in devices if 'MPD' in name][0]
                print("MIDI INPUT:", self._input_name)
            except:
                if i+1 < self._try_n_connects:
                    print("[ERROR] connecting.... retry...")
                    time.sleep(1)
                    continue
                else:
                    print("[ERROR] Cannot list MIDI devices.")
                    return
            break
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
                        with self.id_to_value_lock:
                            self.id_to_value[cid] = [msg.velocity]
                    if msg.type == 'note_off':
                        ctrl_type = 'PAD'
                        if self.encoding_mode == 'CHANNEL_AFTERTOUCH':
                            cid = msg.channel
                        else:
                            cid = msg.note
                        with self.id_to_value_lock:
                            # for a note off we should not overwrite the last
                            # value as it could be missed before processing the
                            # next frame.
                            if cid in self.id_to_value:
                                self.id_to_value[cid].append(msg.velocity)
                            else:
                                self.id_to_value[cid] = [msg.velocity]
                    elif msg.type == 'aftertouch':
                        if self.encoding_mode == 'CHANNEL_AFTERTOUCH':
                            cid = msg.channel
                        with self.id_to_value_lock:
                            self.id_to_value[cid] = [msg.value]
                    elif msg.type == 'control_change':
                        ctrl_type = 'CONTROL'
                        cid = msg.control + 100000
                        with self.id_to_value_lock:
                            self.id_to_value[cid] = [msg.value]
                    # handle teaching mode
                    if self._flag_get_teaching_pad:
                        self._flag_get_teaching_pad = False
                        self._teaching_pad = (cid, ctrl_type)
                    print("PAD ID:", cid)


midi_connection = MIDIConnection()

import threading
import queue

import os
import time

#os.environ["RTMIDI_API"] = "LINUX_ALSA"
import mido

class MIDIConnection:

    def __init__(self, device_id_str, encoding_mode='CHANNEL_AFTERTOUCH',
                 detect_mode='VALUE'):
        self._device_id_str = device_id_str
        #
        self.encoding_mode = encoding_mode
        self.detect_mode = detect_mode
        #
        self._listen_thread = None
        self._flag_get_teaching_pad = False
        self._teaching_pad = None
        self._midi_output = None
        # for detect_mode = VALUE
        self.id_to_value = {}
        self.id_to_value_lock = threading.Lock()
        # for detect_mode = NOTE_ON_EVT
        self.id_to_note_on_evt = {}
        self.id_to_note_on_evt_lock = threading.Lock()
        # misc config
        self._try_n_connects = 10
        # msg
        self._output_msg_queue = queue.Queue()

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
                self._input_name = [name for name in devices if self._device_id_str in name][0]
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

    def _handle_value_msg(self, msg):
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
        elif msg.type == 'note_off':
            ctrl_type = 'PAD'
            if self.encoding_mode == 'CHANNEL_AFTERTOUCH':
                cid = msg.channel
            else:
                cid = msg.note
            with self.id_to_value_lock:
                # for a note off we should not overwrite the last
                # value as it could be missed before processing the
                # next frame.
                #FIXME it it very unlikely that we get a note off
                # without having a note_on yet. so id_to_vlaue will
                # always have a cid value. maybe checking is 
                # unneccessary then.
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
        else:
            return
        # handle teaching mode
        if self._flag_get_teaching_pad:
            self._flag_get_teaching_pad = False
            self._teaching_pad = (cid, ctrl_type)
        print("PAD ID:", cid, " msg type:", msg.type)


    def _handle_note_on_evt_msg(self, msg):
        cid = None
        if msg.type == 'note_on':
            if self.encoding_mode == 'CHANNEL_AFTERTOUCH':
                cid = msg.channel
            else:
                cid = msg.note
            with self.id_to_note_on_evt_lock:
                if cid in self.id_to_note_on_evt:
                    self.id_to_note_on_evt[cid].append(True)
                else:
                    self.id_to_note_on_evt[cid] = [True]
                    # handle teaching mode
        else:
            return
        if self._flag_get_teaching_pad:
            self._flag_get_teaching_pad = False
            self._teaching_pad = (cid, 'PAD')
        print("PAD ID:", cid)


    def _runListen(self):
        with mido.open_input(self._input_name) as midi_input,\
             mido.open_output(self._input_name) as midi_output:
            self._midi_output = midi_output
            while self._keep_running:
                msg = midi_input.receive()
                if msg:
                    if self.detect_mode == 'VALUE':
                        self._handle_value_msg(msg)
                    elif self.detect_mode == 'NOTE_ON_EVT':
                        self._handle_note_on_evt_msg(msg)
                # handle output 
                if not self._output_msg_queue.empty():
                    out_msg = self._output_msg_queue.get()
                    midi_output.send(out_msg)


    def apc_set_status_pad(self, pad_id, is_active, color_value=38):
        m = mido.Message('note_on')
        if is_active:
            led_byte = '99'
        else:
            led_byte = '91'
        note_byte = hex(pad_id)[2:].rjust(2, '0')
        color_byte = hex(color_value)[2:].rjust(2, '0')
        hex_str = led_byte + ' ' + note_byte + ' ' + color_byte
        m = m.from_hex(hex_str)
        self._output_msg_queue.put(m)


    def flushOutputQueue(self):
        while not self._output_msg_queue.empty():
            out_msg = self._output_msg_queue.get()
            self._midi_output.send(out_msg)

        


midi_connection = MIDIConnection("MPD")
midi_apc = MIDIConnection("APC mini", encoding_mode='NOTE', detect_mode='NOTE_ON_EVT')
#midi_connection = MIDIConnection("S-1", encoding_mode='NOTE', detect_mode='VALUE')

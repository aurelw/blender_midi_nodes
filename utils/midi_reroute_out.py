#!/usr/bin/python3

import mido

transpose_v = 0
key_mapping = {37 : 50,
               39 : 57,
               38 : 62,
               40 : 34,
               48 : 70,
               49 : 79,
               44 : 50}




def main():
    mido.get_input_names()
    s1_name = [name for name in mido.get_input_names() if "S-1" in name][0]
    s1_out = mido.open_output(s1_name)
    mpd_in = mido.open_input('MPD218:MPD218 Port A 16:0')
    # prepare out  messages
    m_on = mido.Message('note_on')
    m_on.channel = 2
    m_off = mido.Message('note_off')
    m_off.channel = 2
    while True:
        msg_in = mpd_in.receive()
        print(msg_in)
        if msg_in.type in ['note_on', 'note_off']:
            note_in = msg_in.note
            if note_in in key_mapping:
                if msg_in.type == 'note_on':
                    msg_out = m_on
                else:
                    msg_out = m_off
                msg_out.note = key_mapping[note_in]
                msg_out.note += transpose_v
                msg_out.velocity = msg_in.velocity
                s1_out.send(msg_out)

if __name__ == "__main__":
    main()

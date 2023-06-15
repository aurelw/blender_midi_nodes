import bpy

import midi_connection

def updateAllNodes():
    con = midi_connection.midi_connection
    for node in bpy.node_groups[0].nodes:
        if 'midi_ctrld' in node:
            if node.type == 'VALUE':
                value = con.note_on_data[68]
                node.outputs['Value'].default_value = value

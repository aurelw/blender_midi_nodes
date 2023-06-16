import bpy

from bpy.types import Panel

class MIDINodePanel(Panel):

    bl_label = 'MIDI'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'MIDI'
    bl_idname = 'NODE_PT_midi'

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        scn = context.scene
        layout = self.layout
        row = layout.row()
        row.operator('node.midi_connect_to_device', text="Connect")
        row = layout.row()
        row.operator('node.midi_node_register_to_value_node', text="Activate Node")
        row.operator('node.midi_node_teach', text='Teach')


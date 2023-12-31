import bpy

from bpy.types import Panel

from . import midi_nodes

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
        # handle node
        node = midi_nodes.getActiveNode()
        if not node:
            return
        row = layout.row()
        row.operator('node.midi_node_register_to_value_node', text="Make MIDI Node")
        if 'midi_ctrld' in node and node['midi_ctrld']:
            row = layout.row()
            row.operator('node.midi_node_teach', text='Teach')
            row = layout.row()
            if node['midi_active']:
                row.operator('node.midi_node_deactivate', text='Deactivate')
            else:
                row.operator('node.midi_node_activate', text='Activate')
        ### node properties ###
        if 'midi_ctrld' in node and node['midi_ctrld']:
            if node.type == 'VALUE':
                # scaling
                box = layout.box()
                col = box.column()
                col.label(text="Scale Value")
                col.prop(node, '["midi_do_scale_value"]')
                col.prop(node, '["midi_scale_min"]')
                col.prop(node, '["midi_scale_max"]')
                # decay filter
                box = layout.box()
                col = box.column()
                col.label(text="Decay Filter")
                col.prop(node, '["midi_do_decay_filter"]')
                col.prop(node, '["midi_decay_hold_peak_frames"]')
                col.prop(node, '["midi_decay_rate"]')


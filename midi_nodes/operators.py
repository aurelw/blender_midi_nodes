import bpy
from bpy.types import Operator

from . import midi_connection
from . import midi_nodes

class MIDINodeRegisterToValueNode(Operator):
    """Registers midi trigger on currently selected value node"""
    bl_idname = "node.midi_node_register_to_value_node"
    bl_label = "Register MIDI Signal to Value Node"

    def execute(self, context):
        #FIXME select current node group
        active_node = midi_nodes.getActiveNode()
        active_node['midi_ctrld'] = True
        print("FNNNNNNNNNNNNNN")
        return {'FINISHED'}


class MIDINodeConnect(Operator):
    """Connect to MIDI Device"""
    bl_idname = "node.midi_connect_to_device"
    bl_label = "Connect MIDI"

    def execute(self, context):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!! execute onses")
        midi_connection.midi_connection.listen()
        return {'FINISHED'}


class MIDINodeTeachNode(Operator):
    """Teach the currently selected node with the next MIDI note or ctrl"""
    bl_idname = "node.midi_node_teach"
    bl_label = "Teach a Node with a Pad"

    color_active_input = (0.4, 0.1, 0.56)
    color_teaching = (0.8, 0.1, 0.15)

    def execute(self, context):
        active_node = midi_nodes.getActiveNode()
        if 'midi_ctrld' in active_node and active_node['midi_ctrld']:
            active_node.color = self.color_teaching
            teach = midi_connection.midi_connection.getTeachingPad()
            active_node['pad_id'] = teach[0]
            active_node['midi_ctrl_type'] = teach[1]
            # add color scheme
            active_node.use_custom_color = True
            active_node.color = self.color_active_input

        return {'FINISHED'}

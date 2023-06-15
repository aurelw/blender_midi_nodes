import bpy
from bpy.types import Operator

from . import midi_connection

class MIDINodeRegisterToValueNode(Operator):
    """Registers midi trigger on currently selected value node"""
    bl_idname = "node.midi_node_register_to_value_node"
    bl_label = "Register MIDI Signal to Value Node"

    def execute(self, context):
        #FIXME select current node group
        active_node = bpy.data.node_groups[0].nodes.active
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


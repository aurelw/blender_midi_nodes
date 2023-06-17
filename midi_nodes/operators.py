import bpy
from bpy.types import Operator

from . import midi_connection
from . import midi_nodes

class MIDINodeRegisterToValueNode(Operator):
    """Registers midi triggering on currently selected value node"""
    bl_idname = "node.midi_node_register_to_value_node"
    bl_label = "Register MIDI Signal to Value Node"

    def execute(self, context):
        #FIXME select current node group
        active_node = midi_nodes.getActiveNode()
        if active_node.type == 'VALUE':
            midi_nodes.initPropsOnNode(active_node)
            if active_node.label == '':
                active_node.label = "Value [MIDI]"
            else:
                active_node.label = active_node.label + " [MIDI]"
        return {'FINISHED'}


class MIDINodeActivateNode(Operator):
    """Activate the selected midi node"""
    bl_idname = "node.midi_node_activate"
    bl_label = "Activate MIDI Node"

    color_active_input = (0.4, 0.1, 0.56)
    color_active_noinput = (0.2, 0.05, 0.25)

    def execute(self, context):
        active_node = midi_nodes.getActiveNode()
        if 'midi_ctrld' in active_node and active_node['midi_ctrld']:
            active_node['midi_active'] = True
            if 'pad_id' in active_node and active_node['pad_id'] != '':
                active_node.color = self.color_active_input
            else:
                active_node.use_custom_color = True
                active_node.color = self.color_active_noinput
        return {'FINISHED'}


class MIDINodeDeactivateNode(Operator):
    """Deactivate the selected midi node"""
    bl_idname = "node.midi_node_deactivate"
    bl_label = "Deactivate MIDI Node"

    color_deactive = (0.54, 0.5, 0.4)

    def execute(self, context):
        active_node = midi_nodes.getActiveNode()
        if 'midi_ctrld' in active_node and active_node['midi_ctrld']:
            active_node['midi_active'] = False
            active_node.use_custom_color = True
            active_node.color = self.color_deactive
        return {'FINISHED'}


class MIDINodeConnect(Operator):
    """Connect to MIDI Device"""
    bl_idname = "node.midi_connect_to_device"
    bl_label = "Connect MIDI"

    def execute(self, context):
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
            # also active node right after teaching
            active_node['midi_active'] = True
            # add color scheme
            active_node.use_custom_color = True
            active_node.color = self.color_active_input
        return {'FINISHED'}


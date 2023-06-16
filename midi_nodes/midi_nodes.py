import bpy

from . import midi_connection

def getActiveNode():
    def getActiveNodeFromTree(tree):
        node = tree.nodes.active
        if node.type == 'GROUP':
            return getActiveNodeFromTree(node.node_tree)
        else:
            return node
    return getActiveNodeFromTree(bpy.data.node_groups[0])


def _updateNodeGroup(node_group):
    con = midi_connection.midi_connection
    for node in node_group.nodes:
        if node.type == 'GROUP':
            _updateNodeGroup(node.node_tree)
        elif 'midi_ctrld' in node and node['midi_ctrld']:
            if node.type == 'VALUE':
                if 'pad_id' in node:
                    pad_id = node['pad_id']
                    if pad_id in con.id_to_value:
                        value = con.id_to_value[pad_id]
                        node.outputs['Value'].default_value = value

def updateAllNodes():
    _updateNodeGroup(bpy.data.node_groups[0])

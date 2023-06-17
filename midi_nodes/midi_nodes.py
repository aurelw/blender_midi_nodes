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


def upgradePropsOnNode(node):
    if not 'midi_ctrld' in node or not node['midi_ctrld']:
        return
    if not 'midi_active' in node:
        node['midi_active'] = True
    if not 'midi_do_scale_value' in node:
        node['midi_do_scale_value'] = False
    if not 'midi_scale_min' in node:
        node['midi_scale_min'] = 0.0
    if not 'midi_scale_max' in node:
        node['midi_scale_max'] = 127.0

def initPropsOnNode(node):
    node['midi_ctrld'] = True
    upgradePropsOnNode(node)

def upgradePropsOnNodeGroup(node_group):
    for node in node_group.nodes:
        if node.type == 'GROUP':
            upgradePropsOnNodeGroup(node.node_tree)
        else:
            upgradePropsOnNode(node)


def applyNodeModifiersOnValue(node, value):
    m_value = value
    if node['midi_do_scale_value']:
        min_v = node['midi_scale_min']
        max_v = node['midi_scale_max']
        m_value = (m_value / 127.0) * (max_v - min_v) + min_v
        print("scale value from", value, "to", m_value)
    return m_value


def _updateNodeGroup(node_group):
    con = midi_connection.midi_connection
    for node in node_group.nodes:
        if node.type == 'GROUP':
            _updateNodeGroup(node.node_tree)
        elif 'midi_ctrld' in node and node['midi_ctrld'] and node['midi_active']:
            if node.type == 'VALUE':
                if 'pad_id' in node:
                    pad_id = node['pad_id']
                    if pad_id in con.id_to_value:
                        value = con.id_to_value[pad_id]
                        m_value = applyNodeModifiersOnValue(node, value)
                        node.outputs['Value'].default_value = m_value

def updateAllNodes():
    _updateNodeGroup(bpy.data.node_groups[0])

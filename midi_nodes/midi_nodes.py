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
    ## scaling
    if not 'midi_do_scale_value' in node:
        node['midi_do_scale_value'] = False
        node.id_properties_ensure()
        property_manager = node.id_properties_ui('midi_do_scale_value')
        property_manager.update(min=0, max=1)
    if not 'midi_scale_min' in node:
        node['midi_scale_min'] = 0.0
        node.id_properties_ensure()
        property_manager = node.id_properties_ui('midi_scale_min')
        property_manager.update(min=0)
    if not 'midi_scale_max' in node:
        node['midi_scale_max'] = 127.0
        node.id_properties_ensure()
        property_manager = node.id_properties_ui('midi_scale_max')
        property_manager.update(min=0)
    ## decay
    if not 'midi_do_decay_filter' in node:
        node['midi_do_decay_filter'] = False
        node.id_properties_ensure()
        property_manager = node.id_properties_ui('midi_do_decay_filter')
        property_manager.update(min=0, max=1)
    node['midi_decay_c_value'] = 0.0
    node['midi_decay_c_hold_peak_frames'] = 0
    if not 'midi_decay_hold_peak_frames' in node:
        node['midi_decay_hold_peak_frames'] = 3
        node.id_properties_ensure()
        property_manager = node.id_properties_ui('midi_decay_hold_peak_frames')
        property_manager.update(min=0, max=300)
    if not 'midi_decay_rate' in node:
        node['midi_decay_rate'] = 0.1
        node.id_properties_ensure()
        property_manager = node.id_properties_ui('midi_decay_rate')
        property_manager.update(min=0, max=1.0)

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
    # decay in the range [0.0,127.0] down
    # so start with raw value
    if node['midi_do_decay_filter']:
        # new peak
        if value > node['midi_decay_c_value']:
            print("new peak:", value)
            node['midi_decay_c_value'] = value
            node['midi_decay_c_hold_peak_frames'] = \
                    node['midi_decay_hold_peak_frames'] 
        else:
            # hold peak or decay down to target
            if node['midi_decay_c_hold_peak_frames'] > 0:
                node['midi_decay_c_hold_peak_frames'] -= 1
            else:
                next_c_value = node['midi_decay_c_value'] - \
                               (127 * node['midi_decay_rate'])
                if next_c_value < value:
                    node['midi_decay_c_value'] = value
                else:
                    node['midi_decay_c_value'] = next_c_value
        m_value = node['midi_decay_c_value']
    if node['midi_do_scale_value']:
        min_v = node['midi_scale_min']
        max_v = node['midi_scale_max']
        m_value = (m_value / 127.0) * (max_v - min_v) + min_v

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
                        with con.id_to_value_lock:
                            if len(con.id_to_value[pad_id]) == 2:
                                value = con.id_to_value[pad_id].pop(0)
                            else:
                                value = con.id_to_value[pad_id][0]
                        m_value = applyNodeModifiersOnValue(node, value)
                        node.outputs['Value'].default_value = m_value

def updateAllNodes():
    _updateNodeGroup(bpy.data.node_groups[0])

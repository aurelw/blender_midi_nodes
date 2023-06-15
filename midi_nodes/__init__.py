# Author: Aurel Wildfel lner

bl_info = {
    "name": "MIDI Nodes",
    "author": "Aurel Wildfellner",
    "blender": (3, 4, 0),
    "location": "Node > Toolbox",
    "description": "Drive geometry nodes with MIDI input",
    "warning": "",
    "wiki_url": "",
    "support": 'TESTING',
    "category": "Node"}


import bpy

from bpy.app.handlers import persistent

from . import ui
from . import operators
from . import midi_connection

classes = [
    ui.MIDINodePanel,
    operators.MIDINodeRegisterToValueNode,
    operators.MIDINodeConnect,
]


@persistent
def pre_frame_change_handler(scn):
    midi_nodes.updateAllNodes()

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


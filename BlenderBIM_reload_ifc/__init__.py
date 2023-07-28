bl_info = {
        "name": "IFC Development",
        "description": "Add-on meant for IFC Development.",
        "author": "Coen Claus",
        "version": (1, 0),
        "blender": (3, 5, 1),
        "support": "COMMUNITY",
        "category": "Import-Export",
        "location": "IFC Development"
        }

import bpy

#
# Add additional functions here
#

def register():
    from . import properties
    from . import operator
    from . import ui
    properties.register()
    operator.register()
    ui.register()
   

def unregister():
    from . import properties
    from . import operator
    from . import ui
    properties.unregister()
    operator.unregister()
    ui.unregister()

if __name__ == '__main__':
    register()
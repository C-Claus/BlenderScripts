
bl_info = {
        "name": "Add Reference Image",
        "description": "Just an add-on",
        "author": "Coen Claus",
        "version": (1, 0),
        "blender": (3, 5, 0),
        "location": "IFC Reference Image",
        "warning": "", # used for warning icon and text in add-ons panel
        #"wiki_url": "http://my.wiki.url",
        #"tracker_url": "http://my.bugtracker.url",
        "support": "COMMUNITY",
        "category": "Import-Export"
        }

import bpy

#
# Add additional functions here
#
from . import  properties, ui, operator

def register():
    from . import properties
    from . import ui
    from . import operator
  
    properties.register()
    ui.register()
    operator.register()

def unregister():
    from . import properties
    from . import ui
    from . import operator

    properties.unregister()
    ui.unregister()
    operator.unregister()


if __name__ == '__main__':
    register()
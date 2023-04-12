import bpy
from bpy.types import Panel
#from . import  prop, operator

#
# Add additional functions here
#
print ("hallo")

class PANEL_PT_demo(Panel):
    bl_label = 'Panel demo'
    bl_space_type = 'PROPERTIES'
    bl_region_type= 'WINDOW'
    bl_context = 'render'

    def draw(self, context):
        row = self.layout.row()
        row.prop(context.scene, 'my_property')

def register():
    bpy.utils.register_class(PANEL_PT_demo)

def unregister():
    bpy.utils.unregister_class(PANEL_PT_demo)
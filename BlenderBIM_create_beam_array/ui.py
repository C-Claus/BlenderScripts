import bpy
from bpy.types import Panel
#from . import  prop, operator

#
# Add additional functions here
#
print ("hallo ui ui")

#bl_label = "BlenderBIM Spreadsheet"
#    bl_space_type = "VIEW_3D"
#    bl_region_type = "UI"
#    bl_category = "BlenderBIM | Spreadsheet"
#    bl_options = {"DEFAULT_CLOSED"}

class PANEL_PT_demo(Panel):
    bl_label = 'Panel demo'
    bl_space_type = 'VIEW_3D'
    bl_region_type = "UI"
    bl_category = "Bim"
    #bl_region_type= 'WINDOW'
    #bl_context = 'render'

    def draw(self, context):
        row = self.layout.row()
        #row.prop(context.scene, 'my_property')
    
        # bpy.ops.mesh.primitive_cube_add()
        row.operator("create.array")

def register():
    bpy.utils.register_class(PANEL_PT_demo)
   

def unregister():
    bpy.utils.unregister_class(PANEL_PT_demo)
import bpy
from bpy.types import Panel
from . import  properties, operator



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

        dimension_properties = context.scene.dimension_properties

        layout = self.layout

        box = layout.box()
        row = box.row()
        row.prop(dimension_properties, 'my_height')
        
        box = layout.box()
        row = box.row()
        row.operator("create.array")
     

def register():
    bpy.utils.register_class(PANEL_PT_demo)
   

def unregister():
    bpy.utils.unregister_class(PANEL_PT_demo)
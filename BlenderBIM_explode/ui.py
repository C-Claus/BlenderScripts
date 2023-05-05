import bpy
from bpy.types import Panel
from . import  properties, operator
from blenderbim.bim.ifc import IfcStore




class PANEL_PT_explode(Panel):
    bl_label = 'IFC Explode'
    bl_space_type = 'VIEW_3D'
    bl_region_type = "UI"
    bl_category = "IFC Explode"

    def draw(self, context):


        layout = self.layout
        box = layout.box()
        box.operator("explode.ifc", text="Fuck it")

        return {'FINISHED'}

def register():
    bpy.utils.register_class(PANEL_PT_explode)

   

def unregister():
    bpy.utils.unregister_class(PANEL_PT_explode)
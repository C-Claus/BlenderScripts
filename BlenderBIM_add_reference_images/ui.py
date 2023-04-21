import bpy
from bpy.types import Panel
from . import  properties, operator
from blenderbim.bim.ifc import IfcStore

class PANEL_PT_demo(Panel):
    bl_label = 'IFC Reference Images'
    bl_space_type = 'VIEW_3D'
    bl_region_type = "UI"
    bl_category = "IFC Reference Images"

    def draw(self, context):

        image_properties = context.scene.image_properties

def register():
    bpy.utils.register_class(PANEL_PT_demo)
   

def unregister():
    bpy.utils.unregister_class(PANEL_PT_demo)
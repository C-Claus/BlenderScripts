import bpy
from bpy.types import Panel
from . import  properties, operator
from blenderbim.bim.ifc import IfcStore

class PANEL_PT_demo(Panel):
    bl_label = 'Panel demo'
    bl_space_type = 'VIEW_3D'
    bl_region_type = "UI"
    bl_category = "Bim"

    def draw(self, context):

        dimension_properties = context.scene.dimension_properties
import bpy
from bpy.types import Panel
from . import properties, operator 
from blenderbim.bim.ifc import IfcStore

#
# Add additional functions here
#

class PANEL_PT_MyPanel(Panel):
    bl_label = 'IFC Development'
    bl_space_type = 'VIEW_3D'
    bl_region_type= 'UI'

    bl_category = "IFC Development"

    def draw(self, context):
        row = self.layout.row()
        row.prop(context.scene, 'my_properties')

def register():
    bpy.utils.register_class(PANEL_PT_MyPanel)

def unregister():
    bpy.utils.unregister_class(PANEL_PT_MyPanel)
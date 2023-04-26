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

        layout = self.layout

        #box = layout.box()
        #row = box.row()
        #row.prop(image_properties, 'my_reference_image')

        box = layout.box()
        row = box.row()
        #box.operator("add.referenceimage")
        #box.operator("store.referenceimage")
        box.operator("load.referenceimage")




        layout = self.layout
        box = layout.box()
        box.operator("image.collection_actions", text="Add", icon="ADD").action = "add"

        image_collection = context.scene.image_collection
        row = layout.row(align=True)

        #if len(custom_collection.items) > 0:
        #    row.operator("clear.clear_properties", text="Clear Properties")
       
        for i, item in enumerate(image_collection.items):
          
            row = box.row(align=True)
            row.prop(item, "image")
            row.operator("add.referenceimage", text="", icon="RIGHTARROW")
            row.operator("store.referenceimage", text="", icon="PLUS")
            op = row.operator("image.collection_actions", text="", icon="REMOVE")
            op.action = "remove"
            op.index = i  


            #row = box.row(align=True)
            
            #op = row.operator("image.collection_actions", text="", icon="REMOVE")
            #op.action = "remove"
            #op.index = i
           
     

def register():
    bpy.utils.register_class(PANEL_PT_demo)

   

def unregister():
    bpy.utils.unregister_class(PANEL_PT_demo)

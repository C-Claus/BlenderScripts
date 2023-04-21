import os
import bpy
import numpy as np
import ifcopenshell.api
from ifcopenshell.api import run
from . import operator
import math
from blenderbim.bim.ifc import IfcStore


class AddReferenceImage(bpy.types.Operator):
    """Add Reference Image"""
    bl_idname = "add.referenceimage"
    bl_label = "Add Reference Image"

    def execute(self, context):

        #store image file path in custom property
        #read custom property
        #save image settings
        image_properties = context.scene.image_properties
        print (image_properties.my_reference_image_A)

        print ('excecute')

        #dimension_properties = context.scene.dimension_properties

        return {'FINISHED'}

    def add_image_path_to_ifcproperty(self,context, image_path):

        ifc = ifcopenshell.open(IfcStore.path)
        element = ifc.by_type("IfcBuilding") # Just as an example, you will need to select the elements you want to add properties to yourself.
        pset = run("pset.add_pset", ifc, product=element, name="Reference Image")
        run("pset.edit_pset", ifc, pset=pset, properties={"image A": str(image_path), "foo2": "foobaz"})

def register():
    bpy.utils.register_class(AddReferenceImage)



def unregister():
    bpy.utils.unregister_class(AddReferenceImage)
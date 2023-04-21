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

        print ('excecute')

        #dimension_properties = context.scene.dimension_properties

def register():
    bpy.utils.register_class(AddReferenceImage)



def unregister():
    bpy.utils.unregister_class(AddReferenceImage)
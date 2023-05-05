
import os
from os.path import isabs
import bpy
import uuid
#import numpy as np
import ifcopenshell.api
from ifcopenshell.api import run
from . import operator
#import math
from blenderbim.bim.ifc import IfcStore

import bpy
import random

import mathutils
from mathutils import Euler


class ExplodeIFC(bpy.types.Operator):
    """Explode IFC"""
    bl_idname = "explode.ifc"
    bl_label = "Explode IFC"

    index: bpy.props.IntProperty(default=-1)

    def execute(self, context):

        for obj in bpy.context.view_layer.objects:
            obj.rotation_euler.rotate(Euler((random.randint(1,30), random.randint(1,30), random.randint(1,30))))

        return {'FINISHED'}

def register():
    bpy.utils.register_class(ExplodeIFC)


def unregister():
    bpy.utils.unregister_class(ExplodeIFC)




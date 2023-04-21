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

        #when first add images
        image_properties = context.scene.image_properties

        self.add_image_path_to_ifcproperty(context, image_path=image_properties.my_reference_image_A)


        #when image paths are stored as a property in IFC

        #psets = ifcopenshell.util.element.get_psets(element)
        #ifcopenshell.api.run("pset.edit_pset", ifc, pset=ifc.by_id(psets["Pset_Name"]["id"]), properties={"foo": "changed"})
        #print(ifcopenshell.util.element.get_psets(element))

        return {'FINISHED'}

    def add_image_path_to_ifcproperty(self,context, image_path):

        ifc     =   ifcopenshell.open(IfcStore.path)
        element =   ifc.by_type("IfcBuilding")[0]
        pset    =   run("pset.add_pset", ifc, product=element, name="Reference Images")

        run("pset.edit_pset", ifc, pset=pset, properties={"image A": str(image_path), "image B": "image B file path"})

        ifc.write(IfcStore.path)

        print (image_path + ' has been added to the properties of IfcBuilding')

        #ifc_file = ifcopenshell.open(IfcStore.path)
        #ifc_element = ifc_file.by_type("IfcBuildingStorey")[0]
        #image = ifcopenshell.util.element.get_pset(element, "My Images","StringProperty")
        #bpy.context.area.type = 'VIEW_3D'
        #bpy.ops.view3d.view_axis(type='TOP')

        #bpy.ops.object.empty_add(type='IMAGE',
        #                        radius=1,
        #                        align='VIEW',
        #                        location=(0, 0, 0),
        #                        rotation=(0, -0, 0),
        #                        scale=(1, 1, 1))

        #bpy.ops.object.load_reference_image(filepath=image_path)


class LoadReferenceImage(bpy.types.Operator):
    """Add Reference Image"""
    bl_idname = "load.referenceimage"
    bl_label = "Load Reference Image"

    def execute(self, context):

        #when first add images
        image_properties = context.scene.image_properties

        self.load_reference_images(context, property=None)

        return {'FINISHED'}

    def load_reference_images(self, context, property):

        ifc         =   ifcopenshell.open(IfcStore.path)
        element     =   ifc.by_type("IfcBuilding")[0]
        image_path  =   ifcopenshell.util.element.get_pset(element, "Reference Images","image A")

        bpy.context.area.type = 'VIEW_3D'
        bpy.ops.view3d.view_axis(type='TOP')

        bpy.ops.object.empty_add(type='IMAGE',
                                radius=1,
                                align='VIEW',
                                location=(0, 0, 0),
                                rotation=(0, -0, 0),
                                scale=(1, 1, 1))

        bpy.ops.object.load_reference_image(filepath=image_path)

        print ('load reference images')



def register():
    bpy.utils.register_class(AddReferenceImage)
    bpy.utils.register_class(LoadReferenceImage)



def unregister():
    bpy.utils.unregister_class(AddReferenceImage)
    bpy.utils.unregister_class(LoadReferenceImage)
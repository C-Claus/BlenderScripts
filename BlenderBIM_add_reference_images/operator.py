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

        image_properties = context.scene.image_properties

        self.add_image_path_to_ifcproperty(context, image_path=image_properties.my_reference_image_A)

        return {'FINISHED'}

    def add_image_path_to_ifcproperty(self,context, image_path):

        ifc                 =   ifcopenshell.open(IfcStore.path)
        element             =   ifc.by_type("IfcBuilding")[0]
        propertyset_name    =   'Reference Image'
        image_properties    =   context.scene.image_properties


        pset    =   run("pset.add_pset", ifc, product=element, name=propertyset_name)

        run("pset.edit_pset", ifc, pset=pset, properties={  "image A": str(image_path),
                                                            "image B": "image B file path"})

        ifc.write(IfcStore.path)
        #add image
        #make transformations
        #store image path and transformations

        print (image_path + ' has been added to the properties of IfcBuilding')
        self.load_ifc(ifc_file=ifc, file_path=IfcStore.path)

    def load_ifc(self, ifc_file, file_path):

        if (bool(ifc_file)) == True:
            project = ifc_file.by_type('IfcProject')
            
            if project is not None:
                for i in project:
                    collection_name = 'IfcProject/' + i.Name
                    
                collection = bpy.data.collections.get(str(collection_name))
                
                if collection is not None:
                    for obj in collection.objects:
                        bpy.data.objects.remove(obj, do_unlink=True)
                        
                    bpy.data.collections.remove(collection)
                    
            bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)         
            bpy.ops.bim.load_project(filepath=file_path)


class LoadReferenceImage(bpy.types.Operator):
    """Add Reference Image"""
    bl_idname = "load.referenceimage"
    bl_label = "Load Reference Image"

    def execute(self, context):

        ifc                 =   ifcopenshell.open(IfcStore.path)
        element             =   ifc.by_type("IfcBuilding")[0]
        propertyset_name    =   'Reference Image'

        property_value = ifcopenshell.util.element.get_pset(element, propertyset_name, "image A")

       
        self.load_reference_images(context, property=property_value)

        return {'FINISHED'}

    def load_reference_images(self, context, property):

        """tutorials\

        image_obj = bpy.context.active_object

        # Get the current position, rotation, and scale of the image
        position = image_obj.location
        rotation = image_obj.rotation_euler
        scale = image_obj.scale

        # Print the transformation values to the console
        print("Position:", position)
        print("Rotation:", rotation)
        print("Scale:", scale)
        """


        bpy.context.area.type = 'VIEW_3D'
        bpy.ops.view3d.view_axis(type='TOP')

        bpy.ops.object.empty_add(type='IMAGE',
                                radius=1,
                                align='VIEW',
                                location=(0, 0, 0),
                                rotation=(0, -0, 0),
                                scale=(1, 1, 1))

        bpy.ops.object.load_reference_image(filepath=property)

      


def register():
    bpy.utils.register_class(AddReferenceImage)
    bpy.utils.register_class(LoadReferenceImage)



def unregister():
    bpy.utils.unregister_class(AddReferenceImage)
    bpy.utils.unregister_class(LoadReferenceImage)
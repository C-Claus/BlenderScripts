import os
import bpy
import numpy as np
import ifcopenshell.api
from ifcopenshell.api import run
from . import operator
import math
from blenderbim.bim.ifc import IfcStore

#program flow
#1. load image in planar Z
#2. make transformations to that image
#3. store the image and its tranformations in IFC
#4. upon loading the new ifc image with transformations should appear

image_list = []

class AddReferenceImage(bpy.types.Operator):
    """Import Reference Image"""
    bl_idname = "add.referenceimage"
    bl_label = "Add Image"

    index: bpy.props.IntProperty(default=-1)

    def execute(self, context):

        image_collection    =   context.scene.image_collection
        image_item          =   image_collection.items[self.index]

        print (self.index)
        print (image_item.image)

        if image_item.image:

            bpy.context.area.type = 'VIEW_3D'
            bpy.ops.view3d.view_axis(type='TOP')

            bpy.ops.object.load_reference_image(filepath=image_item.image)
            obj = bpy.context.active_object
            obj.name = os.path.basename(image_item.image)


        return {'FINISHED'}



class StoreReferenceImage(bpy.types.Operator):
    """Store Reference Image"""
    bl_idname = "store.referenceimage"
    bl_label = "Store image path and transformation in IFC"

    index: bpy.props.IntProperty(default=-1)

    def execute(self, context):

        image_collection    =   context.scene.image_collection
        image_item          =   image_collection.items[self.index]
     
        ifc                 =   ifcopenshell.open(IfcStore.path)
        element             =   ifc.by_type("IfcBuilding")[0]
        propertyset_name    =   str(os.path.basename(image_item.image))
        image_properties    =   context.scene.image_properties
        #image_path          =   image_properties.my_reference_image

        #get transformations
        image_obj = bpy.context.active_object

        position = image_obj.location
        rotation = image_obj.rotation_euler
        scale    = image_obj.scale

        pset    =   run("pset.add_pset", ifc, product=element, name=propertyset_name)
        run("pset.edit_pset", ifc, pset=pset, properties={  "image": str(image_item.image),
                                                            "Position X": str(position.x),
                                                            "Position Y": str(position.y),
                                                            "Position Z": str(position.z),
                                                            "Rotation X": str(rotation.x),
                                                            "Rotation Y": str(rotation.y),
                                                            "Rotation Z": str(rotation.z),
                                                            "Scale X": str(scale.x),
                                                            "Scale Y": str(scale.y),
                                                            "Scale Z": str(scale.z)})
        ifc.write(IfcStore.path)
        print (image_item.image + ' has been added to the properties of IfcBuilding')
        self.load_ifc(ifc_file=ifc, file_path=IfcStore.path)
        print ('IFC has been reloaded into BlenderBIM')

      

        return {'FINISHED'}

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
    bl_label = "Load image(s) from IFC"

    index: bpy.props.IntProperty(default=-1)

    def execute(self, context):

        

        image_collection    =   context.scene.image_collection
        image_item          =   image_collection.items[self.index]

  

        ifc                 =   ifcopenshell.open(IfcStore.path)
        element             =   ifc.by_type("IfcBuilding")[0]
        propertyset_name    =   str(os.path.basename(image_item.image))

        property_value =    ifcopenshell.util.element.get_pset(element, propertyset_name, "image")
        location_x     =    ifcopenshell.util.element.get_pset(element, propertyset_name, "Position X")
        location_y     =    ifcopenshell.util.element.get_pset(element, propertyset_name, "Position Y")
        location_z     =    ifcopenshell.util.element.get_pset(element, propertyset_name, "Position Z")
        rotation_x     =    ifcopenshell.util.element.get_pset(element, propertyset_name, "Rotation X")
        rotation_y     =    ifcopenshell.util.element.get_pset(element, propertyset_name, "Rotation Y")
        rotation_z     =    ifcopenshell.util.element.get_pset(element, propertyset_name, "Rotation Z")
        scale_x        =    ifcopenshell.util.element.get_pset(element, propertyset_name, "Scale X")
        scale_y        =    ifcopenshell.util.element.get_pset(element, propertyset_name, "Scale Y")
        scale_z        =    ifcopenshell.util.element.get_pset(element, propertyset_name, "Scale Z")

        image       =   bpy.ops.object.load_reference_image(filepath=property_value)
        obj         =   bpy.context.active_object
        obj.name    =   os.path.basename(property_value)

        # Set the location, rotation, and scale of the object
        obj.location        =   (float(location_x), float(location_y), float(location_z))
        obj.rotation_euler  =   (float(rotation_x), float(rotation_y), float(rotation_z))
        obj.scale           =   (float(scale_x), float(scale_x), float(scale_x))


        return {'FINISHED'}

class ImageCollectionActions(bpy.types.Operator):
    bl_idname = "image.collection_actions"
    bl_label = "Execute"
    action: bpy.props.EnumProperty(items=(("add",) * 3,("remove",) * 3,),)
 
    index: bpy.props.IntProperty(default=-1)

    def execute(self, context):

        image_collection = context.scene.image_collection

        if self.action == "add":        
            image_item =  image_collection.items.add()  
         

         
 
        if self.action == "remove":
            image_collection.items.remove(self.index)

        #for item in image_collection.items:
        #    print (dir(item))
        #    print (item.image, item.name)

        return {"FINISHED"}  

        




def register():
    bpy.utils.register_class(ImageCollectionActions)
    bpy.utils.register_class(AddReferenceImage)
    bpy.utils.register_class(StoreReferenceImage)
    bpy.utils.register_class(LoadReferenceImage)



def unregister():
    bpy.utils.unregister_class(ImageCollectionActions)
    bpy.utils.unregister_class(AddReferenceImage)
    bpy.utils.unregister_class(StoreReferenceImage)
    bpy.utils.unregister_class(LoadReferenceImage)
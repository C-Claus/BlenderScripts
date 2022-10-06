
import bpy
import ifcopenshell
import ifcopenshell.util.element as Element
import ifcopenshell.api.drawing.assign_product as Assign

import blenderbim.bim.import_ifc
from blenderbim.bim.ifc import IfcStore
import blenderbim.tool as tool

import math
from mathutils import Vector

ifc_file = ifcopenshell.open(IfcStore.path)    
walls = ifc_file.by_type('IfcWall')
annotations = ifc_file.by_type('IfcAnnotation')

for obj in bpy.context.view_layer.objects:
    if obj.name.startswith('IfcWall/'):
        
        x = obj.location.x
        y = obj.location.y
        z = obj.location.z
        
        for wall in walls:
            print (wall.Name)
            
            font_curve = bpy.data.curves.new(type="FONT", name="Font Curve")
            font_curve.body = wall.Name
            font_obj = bpy.data.objects.new(name=wall.Name, object_data=font_curve)
            bpy.context.scene.collection.objects.link(font_obj)
            

            bpy.data.objects[font_obj.name].location = Vector((x,y,z))
               

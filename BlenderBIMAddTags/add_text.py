
import bpy
import ifcopenshell
import ifcopenshell.util.element as Element
import ifcopenshell.api.drawing.assign_product as Assign

import blenderbim.bim.import_ifc
from blenderbim.bim.ifc import IfcStore
import blenderbim.tool as tool

import math
import mathutils
from mathutils import Vector

#data_font = bpy.data.fonts.load('C:\\Windows\\Fonts\\Arial.tff')

ifc_file = ifcopenshell.open(IfcStore.path)    
walls = ifc_file.by_type('IfcWall')
annotations = ifc_file.by_type('IfcAnnotation')


#https://blender.stackexchange.com/questions/62040/get-center-of-geometry-of-an-object
#https://blender.stackexchange.com/questions/129473/typeerror-element-wise-multiplication-not-supported-between-matrix-and-vect


#get centre coordines of mesh through bounding box
obj = bpy.context.object
local_bbox_center = 0.125 * sum((Vector(b) for b in obj.bound_box), Vector())
global_bbox_center = obj.matrix_world @ local_bbox_center

#get normals
p = obj.data.polygons[0]
#p.select #Indicates if the face is selected
print ('normal X', p.normal.x)
print ('normal Y', p.normal.y) #The face normal
print ('normal Z', p.normal.z)
#p.vertices #The vertices indexes

#add the text
font_curve = bpy.data.curves.new(type="FONT", name="Font Curve")
font_curve.body = "wall.Name"
font_obj = bpy.data.objects.new(name="wall.Name", object_data=font_curve)
font_obj.data.size = 0.5

bpy.context.scene.collection.objects.link(font_obj)

#set text object
bpy.data.objects[font_obj.name].location = Vector((global_bbox_center.x,global_bbox_center.y,global_bbox_center.z))

#rotate text object throuh normal
#https://blender.stackexchange.com/questions/19533/align-object-to-vector-using-python
DirectionVector = mathutils.Vector(p.normal) 
bpy.data.objects[font_obj.name].rotation_mode = 'QUATERNION'
bpy.data.objects[font_obj.name].rotation_quaternion = DirectionVector.to_track_quat('X','Y')



print (bpy.data.objects[font_obj.name])
print (global_bbox_center.x, global_bbox_center.y, global_bbox_center.z)




"""
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

"""

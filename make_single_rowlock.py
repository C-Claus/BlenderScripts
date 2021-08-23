
import bpy
from mathutils import Vector

collection_name = bpy.data.collections.new("RowLockCollection")

def add_curve():
    
    bpy.context.scene.collection.children.link(collection_name)
    #xyz
    coords_list = [[0,0,0], [10,3,0], [20,3,0],[30,0,0]]

    #coords_list = [[0,0,0], [0,0,0], [0,0,0], [0,0,0]]

    # make a new curve
    crv = bpy.data.curves.new('crv', 'CURVE')
    crv.dimensions = '3D'

    # make a new spline in that curve
    spline = crv.splines.new(type='NURBS')

    # a spline point for each point
    spline.points.add(len(coords_list)-1) # theres already one point by default


    # assign the point coordinates to the spline points
    for p, new_co in zip(spline.points, coords_list):
        print (p, new_co)
        p.co = (new_co + [1.0]) # (add nurbs weight)

    # make a new object with the curve
    obj = bpy.data.objects.new('curve_for_rowlock', crv)
    #bpy.context.scene.collection.objects.link(obj)

    collection_name.objects.link(obj) 
 
def add_brick():
    
   #bpy.context.scene.collection.children.link(collection_name)
    
   obj = bpy.ops.mesh.primitive_cube_add(location=(0.0, 0.0, 0.0)) 

   bpy.context.object.name = "brick"
   
   #bpy.context.object.scale = (0.21, 0.1, 0.5)
   
   bpy.context.object.scale = (0.21, 0.5, 0.1)
   
   #collection_name.objects.link(obj) 
   

def add_array():
    bpy.ops.object.modifier_add(type="ARRAY")
    

    bpy.data.objects[0].modifiers["Array"].count = 24
    
    #xyz = [0][1][2]
    bpy.data.objects[0].modifiers["Array"].relative_offset_displace[0] = 1.0
    
    bpy.context.object.modifiers["Array"].use_constant_offset = True
    
    bpy.data.objects[0].modifiers["Array"].constant_offset_displace[0] = 0.1
    
    
    
    bpy.ops.object.modifier_add(type="CURVE")
    
   
    bpy.context.object.modifiers["Curve"].object = bpy.data.objects["curve_for_rowlock"]
    
    #apply modifiers
    bpy.ops.object.modifier_apply(modifier="Array")
    bpy.ops.object.modifier_apply(modifier="Curve")
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)




    
   
   
      
add_curve()
add_brick()
add_array()



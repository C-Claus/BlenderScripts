import csv
import bpy
import mathutils
from mathutils import Vector


collection_name = bpy.data.collections.new("BeamCollection")

def create_profile(profile_name, profile_height, profile_width):
    
    context = bpy.context
    scene = context.scene
    
    for c in scene.collection.children:
        scene.collection.children.unlink(c)
    
    #collection_name = bpy.data.collections.new("BeamCollection")
    bpy.context.scene.collection.children.link(collection_name)

    w = 1     
    
    
    cList = [   Vector((0,0,0)),
                Vector((0,profile_width,0)),
                Vector((0,profile_width,profile_height)), 
                Vector((0,0,profile_height)), 
                Vector((0,0,0)), 
            ]                      

    curvedata = bpy.data.curves.new(name='Curve', type='CURVE')
    curvedata.dimensions = '3D'

    objectdata = bpy.data.objects.new(profile_name, curvedata)
    objectdata.location = (0,0,0) 

    
    collection_name.objects.link(objectdata) 
   

    polyline = curvedata.splines.new('POLY')
    polyline.points.add(len(cList)-1)
    
    
    for num in range(len(cList)):
        x, y, z = cList[num]
        polyline.points[num].co = (x, y, z, w)
        
    

    
    return bpy.data.objects[objectdata.name]
        

def create_path(path_length):
    
    context = bpy.context
    scene = context.scene
    
    for c in scene.collection.children:
        scene.collection.children.unlink(c)
    
    path_name = "Path"

    bpy.context.scene.collection.children.link(collection_name)
    
    w = 1     
    
    
    cList = [   Vector((0,0,0)),
                Vector((path_length,0,0)),   
                #Vector((0,0,0)),
            ]   
            
    curvedata = bpy.data.curves.new(name='Curve', type='CURVE')
    curvedata.dimensions = '3D'

    objectdata = bpy.data.objects.new(path_name, curvedata)
    objectdata.location = (0,0,0)
    
    collection_name.objects.link(objectdata) 
   


    polyline = curvedata.splines.new('POLY')
    polyline.points.add(len(cList)-1)
    
    
    for num in range(len(cList)):
        x, y, z = cList[num]
        polyline.points[num].co = (x, y, z, w)
        
        
    return bpy.data.objects[objectdata.name]


def extrude_profile_along_path(profile, path):
    
    print (profile.name)
    
    context = bpy.context
    scene = context.scene
    
    #sets active objects
    bpy.context.view_layer.objects.active = profile
     
    #selects active object
    #profile.select_set(True)
    
    bpy.context.object.data.bevel_mode = 'OBJECT'
    
    bpy.context.object.data.bevel_object = bpy.data.objects[path.name]
    bpy.context.object.data.use_fill_caps = True
    
    
    x = 0.0
    y = 0.0
    z = 0.0
    
    for i in range(0, 10):
        y += 4
        make_array(object=profile, x=x, y=y, z=z)


def make_array(object, x, y, z):      
 
    
    C = bpy.context
    
    new_object = object            
    new_obj = new_object.copy()
    new_obj.animation_data_clear()
    collection_name.objects.link(new_obj)  
    
 
    # one blender unit in x-direction
    vec = mathutils.Vector((x, y, z))
    inv = new_obj.matrix_world.copy()
    inv.invert()
    
    # vector aligned to local axis in Blender 2.8+
    vec_rot = vec @ inv
    new_obj.location = new_obj.location + vec_rot   
    
         
    
extrude_profile_along_path(profile=create_profile(profile_name="Beam",profile_height=2, profile_width=1),
                           path=create_path(path_length=5))
    



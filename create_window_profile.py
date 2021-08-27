import bpy
from mathutils import Vector

geometry_name = 'geometry' 
path_name = 'path' 
profile_name = 'profile' 

def create_bezier_curve():
    coords_list = [[0,-2,0], [0,0,0], [0,2,0], [0,4,0]]

    # make a new curve
    crv = bpy.data.curves.new('crv', 'CURVE')
    crv.dimensions = '3D'

    # make a new spline in that curve
    spline = crv.splines.new(type='NURBS')

    # a spline point for each point
    spline.points.add(len(coords_list)-1) # theres already one point by default

    # assign the point coordinates to the spline points
    for p, new_co in zip(spline.points, coords_list):
        p.co = (new_co + [1.0]) # (add nurbs weight)

    # make a new object with the curve
    obj = bpy.data.objects.new(path_name, crv)
    bpy.context.scene.collection.objects.link(obj)





def create_polyline():
    w = 1 # weight
    #cList = [Vector((0,0,0)),Vector((1,0,0)),Vector((2,0,0)),Vector((2,3,0)),
    #        Vector((0,2,0)),Vector((0,0,0))]
            
            
    cList = [      Vector((0,0,0)),
                   Vector((0.03,0,0)),
                   Vector((0.03,-0.009,0)),
                   Vector((0.071999,-0.009,0)),
                   Vector((0.071999,0,0)),
                   Vector((0.081999 ,0,0)),
                   Vector((0.081999 ,-0.009,0)),
                   Vector((0.101999 ,-0.009,0)),
                   Vector((0.101999 ,-0.064999,0)),
                   Vector((0.099999 ,-0.066999,0)),
                   Vector((0.067999 ,-0.066999,0)),
                   Vector((0.067999 ,-0.066999,0)),
                   Vector((0.066999 ,-0.065999,0)),
                   Vector((0.066999 ,-0.049999,0)),
                   Vector((0.002  ,-0.049999,0)),
                   Vector((0  ,-0.047999 ,0)),
                   Vector((0,0,0))
        
                  ]          

    curvedata = bpy.data.curves.new(name='Curve', type='CURVE')
    curvedata.dimensions = '3D'

    objectdata = bpy.data.objects.new(profile_name, curvedata)
    objectdata.location = (0,0,0) 
   
    bpy.context.scene.collection.objects.link(objectdata)


    polyline = curvedata.splines.new('POLY')
    polyline.points.add(len(cList)-1)
    for num in range(len(cList)):
        x, y, z = cList[num]
        polyline.points[num].co = (x, y, z, w)
        
        
def create_mesh():
    
   
    bpy.context.view_layer.objects.active = bpy.data.objects[path_name]
    

    bpy.context.object.data.bevel_mode = 'OBJECT'
    
    
    
    bpy.context.object.data.bevel_object = bpy.data.objects[profile_name]
    
    
    bpy.data.objects[path_name].select_set(True)
    
    bpy.ops.object.convert(target='MESH')

    #bpy.context.view_layer.objects.active.convert(target='MESH')




            
        
create_polyline()
create_bezier_curve()
create_mesh()
import csv
import bpy
import mathutils
from mathutils import Vector


collection_name = bpy.data.collections.new("BeamCollection")

def create_beam(profile_name, profile_height, profile_width, beam_length, direction):
    
    context = bpy.context
    scene = context.scene
    
    for c in scene.collection.children:
        
        if c.name[0:(len(c.name)-4)] in collection_name.name:
            scene.collection.children.unlink(c)
    

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
        
    context.view_layer.objects.active = objectdata
    
    
    
    
    objectdata.select_set(True)
    bpy.ops.object.convert(target='MESH')
    
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')

    
    bpy.ops.mesh.edge_face_add()
    
    bpy.ops.mesh.extrude_context_move(MESH_OT_extrude_context={"use_normal_flip":False, 
                                        "use_dissolve_ortho_edges":False, "mirror":False}, 
                                        TRANSFORM_OT_translate={"value":(0, 0, beam_length), 
                                        "orient_type":'NORMAL',
                                        "orient_matrix":((0, -1, 0), (0, 0, -1), (1, 0, 0)),
                                        "orient_matrix_type":'NORMAL', 
                                        "constraint_axis":(False, False, True), 
                                        "mirror":False,
                                        "use_proportional_edit":False,
                                        "proportional_edit_falloff":'SMOOTH',
                                        "proportional_size":1,
                                        "use_proportional_connected":False, 
                                        "use_proportional_projected":False,
                                        "snap":False, "snap_target":'CLOSEST',
                                        "snap_point":(0, 0, 0),
                                        "snap_align":False, 
                                        "snap_normal":(0, 0, 0),
                                        "gpencil_strokes":False,
                                        "cursor_transform":False,
                                        "texture_space":False, 
                                        "remove_on_cancel":False, 
                                        "release_confirm":True,
                                        "use_accurate":False, 
                                        "use_automerge_and_split":False})
                                        
                                        
 
    
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
    
    
    if direction == "y":
        bpy.ops.transform.rotate(value=1.5708, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)



    return bpy.data.objects[objectdata.name]
        


def create_beam_system(count, center_to_center_distance, beam):

    
    context = bpy.context
    scene = context.scene
    
    
    #sets active objects
    bpy.context.view_layer.objects.active = beam
    
    
    x = 0.0
    y = 0.0
    z = 0.0
    
    for i in range(0, count-1):
        y += center_to_center_distance
        make_array(object=beam, x=x, y=y, z=z)



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
   
                    
    
create_beam_system( count=9, 
                    center_to_center_distance=0.6,
                    beam = create_beam(profile_name="Beam",
                    profile_height=0.05, 
                    profile_width=0.025,
                    beam_length=7,
                    direction="x" ))
    




import bpy
import mathutils
from itertools import repeat
import bmesh
#hoe update je een mesh?

def add_single_tread(tread_width, tread_length, tread_height):
    
    
    mesh_name = "tread" 
    collection_name = bpy.data.collections.new("stair_collection")
    bpy.context.scene.collection.children.link(collection_name)
    
    vertices_tread = [  (0,0,0),
                        (0,tread_width,0),
                        (tread_length,tread_width,0),
                        (tread_length,0,0),
                        
                        (0,0,tread_height),
                        (0,tread_width,tread_height),
                        (tread_length,tread_width,tread_height),
                        (tread_length,0,tread_height)
                        ]

    edges = []

    faces = [(0,1,2,3),
             (4,5,6,7),
             (0,4,5,1), 
             (1,5,6,2),
             (2,6,7,3),
             (3,7,4,0)
             ]


    new_mesh = bpy.data.meshes.new('tread_mesh')
    new_mesh.from_pydata(vertices_tread, edges, faces)
    new_mesh.update()
    
    
    # make object from mesh
    new_object = bpy.data.objects.new(mesh_name, new_mesh)
    collection_name.objects.link(new_object) 
    
    


tread_length = 0.21
tread_width = 0.1
tread_height = 0.05    
    
add_single_tread(tread_width=tread_width, tread_length=tread_length, tread_height=tread_height)
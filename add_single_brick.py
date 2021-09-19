
import bpy
import mathutils
from itertools import repeat



mesh_name = "brick" 
collection_name = bpy.data.collections.new("BrickCollection")
bpy.context.scene.collection.children.link(collection_name)


def add_single_brick(brick_width, brick_length, brick_height):
    print ("add single brick")
    
    vertices_brick = [  (0,0,0),
                        (0,brick_width,0),
                        (brick_length,brick_width,0),
                        (brick_length,0,0),
                        
                        (0,0,brick_height),
                        (0,brick_width,brick_height),
                        (brick_length,brick_width,brick_height),
                        (brick_length,0,brick_height)
                        ]

    edges = []
    

    faces = [(0,1,2,3),
             (4,5,6,7),
             (0,4,5,1), 
             (1,5,6,2),
             (2,6,7,3),
             (3,7,4,0)
             ]


    new_mesh = bpy.data.meshes.new('brick_mesh')
    new_mesh.from_pydata(vertices_brick, edges, faces)
    new_mesh.update()
    
    
    # make object from mesh
    new_object = bpy.data.objects.new(mesh_name, new_mesh)
    
    collection_name.objects.link(new_object) 
    
    


brick_length = 0.21
brick_width = 0.1
brick_height = 0.05    
    
add_single_brick(brick_width=brick_width, brick_length=brick_length, brick_height=brick_height)
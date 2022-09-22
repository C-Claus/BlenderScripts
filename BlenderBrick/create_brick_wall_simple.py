
import bpy
import mathutils
from itertools import repeat


mesh_name = "brick" 
collection_name = "Collection" 

head_joint = 0
#bed_joint = 0



def make_brick_wall(bricks_y_direction, bricks_z_direction, bed_joint, horizontal_joint):
    
    #hardcode coordinates of vertices of brick
    vertices_brick = [  (0,0,0),
                        (0,1,0),
                        (2.1,1,0),
                        (2.1,0,0),
                        
                        (0,0,0.5),
                        (0,1,0.5),
                        (2.1,1,0.5),
                        (2.1,0,0.5)
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

    # make collection
    new_collection = bpy.data.collections.new(collection_name)


    # add object to scene collection
    new_collection.objects.link(new_object)

    
    x = 0.0
    y = 0.0
    z = 0.0 
    
    
    
    x_vector = (vertices_brick[2][0])/2 #=1.1
    z_vector =  (vertices_brick[4][2])+bed_joint#=0.6
    x_move_list=[]
    xyz_list = []
    
    print (z_vector)
    
    x_move_list.extend(repeat(x_vector,bricks_z_direction))
 
    for b in range (0,len(x_move_list)):
        x_move_list.insert(b*2,0)
    
    z_list = [x * z_vector for x in range(0, len(x_move_list))]
  
    #amount of brick in x-direction
    for i in range(0,bricks_y_direction):
        x += (vertices_brick[2][0]) + horizontal_joint
        
        for x_move, z in zip(x_move_list, z_list):
    
            xyz_list.append([x+x_move, 0.0, z])
            add_row(object=new_object, x=x+x_move, y=y, z=z)

           

             
def add_row(object, x, y, z):      
 
    
    C = bpy.context
    
    new_object = object
            
    new_obj = new_object.copy()
    new_obj.animation_data_clear()
    C.collection.objects.link(new_obj)  
    
 
    # one blender unit in x-direction
    vec = mathutils.Vector((x, y, z))
    inv = new_obj.matrix_world.copy()
    inv.invert()
    
    # vector aligned to local axis in Blender 2.8+
    vec_rot = vec @ inv
    new_obj.location = new_obj.location + vec_rot
  
    



           
make_brick_wall(bricks_y_direction=15, 
                bricks_z_direction=15,
                bed_joint=0.1,
                horizontal_joint=0.1)   


#bricks = [obj for obj in bpy.data.objects if obj.name.startswith(mesh_name)] 


        

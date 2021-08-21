
import bpy
import mathutils
from itertools import repeat


mesh_name = "brick" 
collection_name = bpy.data.collections.new("BrickCollection")
bpy.context.scene.collection.children.link(collection_name)


def make_brick_wall(brick_height, brick_length, brick_width,bricks_x_direction, bricks_z_direction, bed_joint, horizontal_joint):
    
   
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
  
    x = 0.0
    y = 0.0
    #z = 0.0 
    
    x_vector = (vertices_brick[2][0])/2
    z_vector =  (vertices_brick[4][2])+bed_joint
    x_move_list=[]
    xyz_list = []
    
 
    
    x_move_list.extend(repeat(x_vector,bricks_z_direction))
 
    for b in range (0,len(x_move_list)):
        x_move_list.insert(b*2,0)
    
    z_list = [x * z_vector for x in range(0, len(x_move_list))]
  
    #amount of brick in x-direction
    for i in range(0,bricks_x_direction):
        x += (vertices_brick[2][0]) + horizontal_joint
        
        for x_move, z in zip(x_move_list, z_list):
    
            #xyz_list.append([x+x_move, 0.0, z])
            add_row(object=new_object, x=x+x_move, y=y, z=z)

           
             
def add_row(object, x, y, z):      
 
    
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
  
    


brick_length = 0.21
brick_width = 0.1
brick_height = 0.05

bed_joint = 0.01
horizontal_joint = 0.01

wall_length = 1
wall_height = 1


amount_bricks_z = (wall_height/(brick_height+bed_joint))/2
amount_bricks_x = (wall_length)/(brick_length+horizontal_joint)
actual_wall_height = (amount_bricks_z)*(brick_height+bed_joint)*2-(2*brick_height+bed_joint)
actual_wall_length = (amount_bricks_x)

print ("lagenmaat:" , actual_wall_height)

           
make_brick_wall(brick_height=brick_height, 
                brick_length=brick_length, 
                brick_width=brick_width, 
                bricks_x_direction=int(amount_bricks_x), 
                bricks_z_direction=int(amount_bricks_z),
                bed_joint=bed_joint,
                horizontal_joint=horizontal_joint)   

#bricks = [obj for obj in bpy.data.objects if obj.name.startswith(mesh_name)] 



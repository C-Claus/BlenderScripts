
import bpy
import mathutils
from itertools import repeat



mesh_name = "brick" 
collection_name = bpy.data.collections.new("RowLockCollection")
bpy.context.scene.collection.children.link(collection_name)


def add_single_brick(brick_width, brick_length, brick_height, horizontal_joint, amount_of_bricks):
 

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
    
    
    x = 0.0
    y = 0.0
    #z = 0.0 
    
  
    for y_move in range(0, amount_of_bricks-1):
       
        y  += (brick_width+horizontal_joint)
    
        add_row(object=new_object, x=0, y=y, z=0)
    
    
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
    
    
    

def join_all_bricks():              
    scene = bpy.context.scene

    bricks_list = []
    for brick in scene.objects:
        if brick.type == 'MESH':
            bricks_list.append(brick)


    context = bpy.context.copy()
    context['active_object'] = bricks_list[0]
    context['selected_editable_objects'] = bricks_list
    
    bpy.ops.object.join(context)
    

    obj = bpy.context.window.scene.objects[0]
    bpy.context.view_layer.objects.active = obj  
    obj.select_set(True)  # 'obj' is the active object now
    
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN') 
    
    add_simple_deform_modifier(rowlock_object=obj)
    

  
    
def add_simple_deform_modifier(rowlock_object):
    
    context = bpy.context
    scene = context.scene
    

 
    context.view_layer.objects.active = rowlock_object
    rowlock_object.select_set(True)
    
          
    bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')
    bpy.context.object.modifiers["SimpleDeform"].deform_method = 'TAPER'
    bpy.context.object.modifiers["SimpleDeform"].deform_axis = 'Z'
    bpy.context.object.modifiers["SimpleDeform"].factor = 0.15  
    
    bpy.ops.object.modifier_apply(modifier="SimpleDeform")

    
    
    #mesh = bpy.data.meshes[str(mesh_name)]
    
    #if rowlock_object.select_get():
    #    rowlock_object.data = mesh
    
    
    

def create_rowlock():    
    context = bpy.context
    scene = context.scene

 
    brick_length = 0.21
    brick_width = 0.1
    brick_height = 0.05    
    horizontal_joint = 0.01    
    amount_of_bricks = 10

     
    add_single_brick(brick_width=brick_height, 
                    brick_length=brick_width, 
                    brick_height=brick_length,
                    horizontal_joint=horizontal_joint,
                    amount_of_bricks=amount_of_bricks)
                    
    join_all_bricks() 
    
    
    
    
    
def delete_collection():
    
    context = bpy.context
    scene = context.scene
     
    for c in scene.collection.children:
        if c.name[0:(len(c.name)-4)] in collection_name.name:
            scene.collection.children.unlink(c) 




create_rowlock()






    



import bpy
import mathutils
from itertools import repeat

name_collection = "brick_collection"
name_object = "brick"
name_mesh = "brick" 


def add_single_brick(amount_of_bricks, horizontal_joint, brick_width, brick_length, brick_height):
    
    mesh_name = name_mesh 
    collection_name = bpy.data.collections.new(name_collection)
    bpy.context.scene.collection.children.link(collection_name)
    
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

    new_mesh = bpy.data.meshes.new(name_mesh)
    new_mesh.from_pydata(vertices_brick, edges, faces)
    new_mesh.update()
    
    
    # make object from mesh
    new_object = bpy.data.objects.new(mesh_name, new_mesh)
    collection_name.objects.link(new_object) 
    
    x=0
    y=0
    z=0
    
 
    y_move_list =[]
    
    for y_move in range(0, amount_of_bricks-1):
       
        y += (brick_width+horizontal_joint)
       
        #add_row(object=new_object, x=0, y=y, z=0.0)
        
        y_move_list.append(y)
        
        
       
    z_repeat_list = [0,brick_height/2+horizontal_joint] * amount_of_bricks
    
    #print (z_repeat_list)
    
    for y, z in zip(y_move_list, z_repeat_list):
        print (y,z)
        
        add_row(object=new_object, x=0, y=y, z=z)
        
        
        

    
def add_row(object, x, y, z):      
 
    C = bpy.context
    
    new_object = object            
    new_obj = new_object.copy()
    new_obj.animation_data_clear()
    
    if (bool(bpy.data.collections.get(name_collection))) == True:
       
        collection = bpy.data.collections.get(name_collection)
        collection.objects.link(new_obj)  
    
 
        # one blender unit in x-direction
        vec = mathutils.Vector((x, y, z))
        inv = new_obj.matrix_world.copy()
        inv.invert()
        
        # vector aligned to local axis in Blender 2.8+
        vec_rot = vec @ inv
        new_obj.location = new_obj.location + vec_rot  
        
        
        
def join_all(deform_factor):
    
    bricks_list = []
    
    for obj in bpy.data.collections[name_collection].all_objects:
        bricks_list.append(bpy.data.objects[obj.name])
        
    context = bpy.context.copy()
    context['active_object'] = bricks_list[0]
    context['selected_editable_objects'] = bricks_list
    
    bpy.ops.object.join(context)
    bpy.ops.object.select_all(action='SELECT')
    
    if (bool(bpy.data.collections.get(name_collection))) == True:
      
        collection = bpy.data.collections.get(name_collection)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        
        for obj in bpy.data.collections[name_collection].all_objects:
            add_simple_deform_modifier(rowlock_object=obj, deform_factor=deform_factor)
        
    else:
        print ("no collection found")
      

def remove_brick_collection():
    
    bpy.ops.object.select_all(action='DESELECT')
    
    if (bool(bpy.data.collections.get(name_collection))) == True:
      
        collection = bpy.data.collections.get(name_collection)
        bpy.data.collections.remove(collection)
        
    else:
        print ("no collection found")
        
        
        
def add_simple_deform_modifier(rowlock_object, deform_factor):
    
    context = bpy.context
    scene = context.scene
    

    context.view_layer.objects.active = rowlock_object
    rowlock_object.select_set(True)
    
          
    bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')
    bpy.context.object.modifiers["SimpleDeform"].deform_method = 'TAPER'
    bpy.context.object.modifiers["SimpleDeform"].deform_axis = 'Z'
    bpy.context.object.modifiers["SimpleDeform"].factor = deform_factor
    
    bpy.ops.object.modifier_apply(modifier="SimpleDeform")
    
        

        
def add_rowlock():   
    
 
 
    #brick_length = 0.21
    #brick_width = 0.10
    #brick_height = 0.05 
    
    brick_length = 0.10
    brick_width = 0.05
    brick_height = 0.21   
       
    brick_amount = 18
    horizontal_joint = 0.01
    
    taper_factor = 0.15
         
      
    remove_brick_collection()   
        
    add_single_brick(amount_of_bricks=brick_amount,
                     horizontal_joint=horizontal_joint,
                     brick_width=brick_width, 
                     brick_length=brick_length, 
                     brick_height=brick_height) 
                      
    join_all(deform_factor=taper_factor)   

add_rowlock()
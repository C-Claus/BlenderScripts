
import bpy
import mathutils
from itertools import repeat

import lxml
import xlsxwriter


name_collection = "brick_collection"
name_object = "brick_wall"
name_mesh = "brick_whole" 
name_mesh_half = "brick_half"
name_mesh_two_third = "brick_two_third"


def add_single_brick(wall_length, head_joint, bed_joint, brick_length, brick_width, brick_thickness, bond):
    
    scale_factor = 1000
    
    amount_of_bricks = int((wall_length/brick_width+head_joint))
    amount_of_half_bricks = int((wall_length/(brick_width/2)+head_joint))
    

    
    mesh_name = name_mesh + "_" + bond + "_"  + str(int(brick_width*scale_factor)) + "x" + str(int(brick_length*scale_factor)) + "x" + str(int(brick_thickness*scale_factor))
    collection_name = bpy.data.collections.new(name_collection)
    bpy.context.scene.collection.children.link(collection_name)
    
    #######################################################
    ##################### single brickk ###################
    #######################################################
    vertices_whole_brick = [  (0,0,0),
                        (0,brick_width,0),
                        (brick_length,brick_width,0),
                        (brick_length,0,0),
                        
                        (0,0,brick_thickness),
                        (0,brick_width,brick_thickness),
                        (brick_length,brick_width,brick_thickness),
                        (brick_length,0,brick_thickness)
                        ]

    edges_whole_brick = []

    faces_whole_brick = [(0,1,2,3),
             (4,5,6,7),
             (0,4,5,1), 
             (1,5,6,2),
             (2,6,7,3),
             (3,7,4,0)
             ]

    new_mesh = bpy.data.meshes.new(name_mesh)
    new_mesh.from_pydata(vertices_whole_brick, edges_whole_brick, faces_whole_brick)
    new_mesh.update()
    
    # make object from mesh
    new_object = bpy.data.objects.new(mesh_name, new_mesh)
    collection_name.objects.link(new_object) 
    
    
    #######################################################
    ##################### half brick ######################
    #######################################################
    vertices_half_brick = [  (0,0,0),
                            (0,brick_width/2,0),
                            (brick_length,brick_width/2,0),
                            (brick_length,0,0),
                            
                            (0,0,brick_thickness),
                            (0,brick_width/2,brick_thickness),
                            (brick_length,brick_width/2,brick_thickness),
                            (brick_length,0,brick_thickness)
                        ]

    edges_half_brick = []

    faces_half_brick = [(0,1,2,3),
             (4,5,6,7),
             (0,4,5,1), 
             (1,5,6,2),
             (2,6,7,3),
             (3,7,4,0)
             ]
             
    new_mesh_half = bpy.data.meshes.new(name_mesh_half)
    new_mesh_half.from_pydata(vertices_half_brick, edges_half_brick, faces_half_brick)
    new_mesh_half.update()
    
    new_half_object = bpy.data.objects.new(name_mesh_half, new_mesh_half)
    collection_name.objects.link(new_half_object) 
             
             
             
    #######################################################
    ###############  2/3 brick quoin ######################
    #######################################################
    vertices_two_third_brick = [  (0,0,0),
                            (0,brick_width*(3/4),0),
                            (brick_length,brick_width*(3/4),0),
                            (brick_length,0,0),
                            
                            (0,0,brick_thickness),
                            (0,brick_width*(3/4),brick_thickness),
                            (brick_length,brick_width*(3/4),brick_thickness),
                            (brick_length,0,brick_thickness)
                        ]

    edges_two_third_brick = []

    faces_two_third_brick = [(0,1,2,3),
             (4,5,6,7),
             (0,4,5,1), 
             (1,5,6,2),
             (2,6,7,3),
             (3,7,4,0)
             ]
             
    new_mesh_two_third = bpy.data.meshes.new(name_mesh_two_third)
    new_mesh_two_third.from_pydata(vertices_two_third_brick, edges_two_third_brick, faces_two_third_brick)
    new_mesh_two_third.update()
    
    new_two_third_object = bpy.data.objects.new(name_mesh_two_third, new_mesh_two_third)
    collection_name.objects.link(new_two_third_object) 
             

    x=0
    y=0
    y2=(2/3)*brick_width + head_joint
    y3=(2/3)*brick_width + head_joint 
    z=0
    
    
    if bond == 'stretcher':   
        for bricks in range(0, amount_of_bricks):
            y += (brick_width+head_joint)
            
            #adds whole brickl
            add_row(object=new_object, x=0, y=y, z=0.0)
            add_row(object=new_object, x=0, y=y+brick_width/2+head_joint, z=brick_thickness+bed_joint)
            
            #adds half bricks at the end
            add_row(object=new_half_object, x=0, y=brick_width+head_joint, z=brick_thickness+bed_joint)
            add_row(object=new_half_object, x=0, y=brick_width+head_joint+amount_of_bricks*(brick_width+head_joint), z=0.0)
            
            
    if bond == 'flemish':
         for bricks in range(0, amount_of_bricks):
            y += (brick_width+(head_joint)) + (brick_width/2) + (head_joint)
        
            #add bottom row
            add_row(object=new_object, x=0, y=y, z=0.0)
            add_row(object=new_half_object, x=0, y=y+brick_width+head_joint, z=0.0)
             

            #add top row
            add_row(object=new_object, x=0, y=y-y2-head_joint-head_joint, z=brick_thickness+bed_joint)
            add_row(object=new_half_object, x=0, y=y-y2+(brick_width)-head_joint, z=brick_thickness+bed_joint)
            
            
            y_end = (brick_width*(3/4) + (brick_width/2) - head_joint + head_joint/2)
            
            #add bricks at ends 
            add_row(object=new_two_third_object, x=0, y=(brick_width)*(2/3) + (head_joint*2)+head_joint/2,z=0)
            move_brick_y =  (amount_of_bricks)*brick_width + (amount_of_bricks)*brick_width/2 + (amount_of_bricks)*head_joint 
            add_row(object=new_two_third_object,
                    x=0, 
                     y=move_brick_y+y_end,#0.2575,
                     z=brick_thickness+bed_joint)
       
 
    #remove initial brick and half brick
    objs = bpy.data.objects
    objs.remove(objs[new_object.name], do_unlink=True)
    objs.remove(objs[new_half_object.name], do_unlink=True)
    objs.remove(objs[new_two_third_object.name], do_unlink=True)
      
    
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
              
        
def join_all_and_create_array(wall_height, bed_joint):
    
    bricks_list = []
    
    for obj in bpy.data.collections[name_collection].all_objects:
        bricks_list.append(bpy.data.objects[obj.name])
        
    context = bpy.context.copy()
    context['active_object'] = bricks_list[0]
    context['selected_editable_objects'] = bricks_list
    
    
    ################################################
    ############# join all objects #################
    ################################################
    bpy.ops.object.join(context)
    #bpy.ops.object.select_all(action='SELECT')
    
    
    if (bool(bpy.data.collections.get(name_collection))) == True:
      
        collection = bpy.data.collections.get(name_collection)
        #bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        
        for joined_object in bpy.data.collections[name_collection].all_objects:
         
            
            bpy.ops.object.select_all(action='DESELECT')
            object_selected = bpy.data.objects[joined_object.name]
            object_selected.select_set(True)    
            bpy.context.view_layer.objects.active = object_selected
            
            ################################################
            ### start of array modifier for Z-direction ####
            ################################################
           
            bpy.ops.object.modifier_add(type='ARRAY')
            
            #relative offset
            bpy.context.object.modifiers["Array"].relative_offset_displace[0] = 0
            bpy.context.object.modifiers["Array"].relative_offset_displace[2] = 1
            
            #constant offset
            bpy.context.object.modifiers["Array"].use_constant_offset = True
            bpy.context.object.modifiers["Array"].constant_offset_displace[0] = 0
            bpy.context.object.modifiers["Array"].constant_offset_displace[2] = bed_joint
            
            bpy.context.object.modifiers["Array"].fit_type = 'FIT_LENGTH'
            bpy.context.object.modifiers["Array"].fit_length = wall_height
            
            bpy.ops.object.modifier_apply(modifier="Array")
            
            #bpy.ops.object.join(context)
            
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
            
            
        bpy.ops.object.select_all(action='DESELECT')
       
    else:
        print ("no collection found")
      

def remove_brick_collection():
    
    bpy.ops.object.select_all(action='DESELECT')
    
    if (bool(bpy.data.collections.get(name_collection))) == True:
      
        collection = bpy.data.collections.get(name_collection)
        bpy.data.collections.remove(collection)
        
    else:
        print ("no collection found")
        
  
def add_wall():  
    
    
    
    wall_length = 2
    wall_height = 1
    
    brick_length = 0.11
    brick_width = 0.21
    brick_thickness = 0.05
    
    
    head_joint = 0.01
    bed_joint = 0.01
       
    
    #stretcher
    #english
    #flemish
    #monk
    #dutch
    #brazillian
    
    bond_type = 'stretcher'
           
    remove_brick_collection()   
        
    add_single_brick(wall_length=wall_length,
    
                     
                     head_joint=head_joint,
                     bed_joint=bed_joint,
                     
                        
                     brick_length=brick_length,
                     brick_width=brick_width,
                     brick_thickness=brick_thickness,
                 
                     
                  
                     bond=bond_type) 
             
    join_all_and_create_array(wall_height=wall_height,bed_joint=bed_joint)   
    

def export_to_ifc():
    
    bpy.ops.bim.create_project()
    
    #bpy.ops.bim.create_project()
    
    if (bool(bpy.data.collections.get(name_collection))) == True:
      
        collection = bpy.data.collections.get(name_collection)
        #bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        
        for joined_object in bpy.data.collections[name_collection].all_objects:
            print (joined_object)
            
            bpy.ops.object.select_all(action='DESELECT')
            object_selected = bpy.data.objects[joined_object.name]
            object_selected.select_set(True)    
            bpy.context.view_layer.objects.active = object_selected
    
            bpy.context.scene.BIMRootProperties.ifc_class = 'IfcWall'
            
            #bpy.ops.bim.edit_object_placement(obj="IfcWall/brick_wall_stretcher_110x210x50.008")
            #bpy.ops.bim.add_representation(obj="IfcWall/brick_wall_stretcher_110x210x50.008", context_id=0, ifc_representation_class="")
            bpy.ops.bim.assign_class(ifc_class="IfcWall", 
                                     predefined_type="ELEMENTEDWALL",
                                     )





    
    

add_wall()
#export_to_ifc()



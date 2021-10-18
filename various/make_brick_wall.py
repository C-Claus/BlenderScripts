
import bpy
import mathutils

mesh_name = "brick" 
collection_name = "Collection" 


def make_brick_wall():
    
    ########################
    ### Initialize brick ###
    ########################
    
    #hardcode coordinates of vertices of brick
    vertices_waalformaat = [(0,0,0),
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
    new_mesh.from_pydata(vertices_waalformaat, edges, faces)
    new_mesh.update()

    # make object from mesh
    new_object = bpy.data.objects.new(mesh_name, new_mesh)

    # make collection
    new_collection = bpy.data.collections.new(collection_name)


    # add object to scene collection
    new_collection.objects.link(new_object)
    
    bpy.data.collections[collection_name].objects.link(new_object)
    
    
 
    
    C = bpy.context
    
    x = 0
    y = 0
    z = 0 
    

 

    for i in range (0,5):
        
        
        
        
        
        ########################
        ###### copy brick ######
        ########################
        new_obj = new_object.copy()
        new_obj.animation_data_clear()
        C.collection.objects.link(new_obj)  
        
        
        ########################
        ###### move brick ######
        ########################
        x += 2.2   
        # one blender unit in x-direction
        vec = mathutils.Vector((x, 0.0, 0.0))
        inv = new_obj.matrix_world.copy()
        inv.invert()
        
        # vec aligned to local axis in Blender 2.8+
        # in previous versions: vec_rot = vec * inv
        vec_rot = vec @ inv
        new_obj.location = new_obj.location + vec_rot
        
      
      
    
        
        #add second row
            
        new_obj = new_object.copy()
        new_obj.animation_data_clear()
        C.collection.objects.link(new_obj)  
        
     
        # one blender unit in x-direction
        vec = mathutils.Vector((x+1.1, 0.0, 0.6))
        inv = new_obj.matrix_world.copy()
        inv.invert()
        
        # vec aligned to local axis in Blender 2.8+
        # in previous versions: vec_rot = vec * inv
        vec_rot = vec @ inv
        new_obj.location = new_obj.location + vec_rot
        
        
        
        
        
        #add third row
            
        new_obj = new_object.copy()
        new_obj.animation_data_clear()
        C.collection.objects.link(new_obj)  
        
     
        # one blender unit in x-direction
        vec = mathutils.Vector((x, 0.0, 1.2))
        inv = new_obj.matrix_world.copy()
        inv.invert()
        
        # vec aligned to local axis in Blender 2.8+
        # in previous versions: vec_rot = vec * inv
        vec_rot = vec @ inv
        new_obj.location = new_obj.location + vec_rot
        
        
        
        
        #add fourth row
        
        new_obj = new_object.copy()
        new_obj.animation_data_clear()
        C.collection.objects.link(new_obj)  
        
     
        # one blender unit in x-direction
        vec = mathutils.Vector((x+1.1, 0.0, 1.8))
        inv = new_obj.matrix_world.copy()
        inv.invert()
        
        # vec aligned to local axis in Blender 2.8+
        # in previous versions: vec_rot = vec * inv
        vec_rot = vec @ inv
        new_obj.location = new_obj.location + vec_rot
        
        
        
        
        
        
        
        
        #z += 0.6
        
        #add_row(x=0.0, y=0.0, z=z)





       
             
def add_row(x, y, z):      
    #add third row
            
    new_obj = new_object.copy()
    new_obj.animation_data_clear()
    C.collection.objects.link(new_obj)  
    
 
    # one blender unit in x-direction
    vec = mathutils.Vector((x, y, z))
    inv = new_obj.matrix_world.copy()
    inv.invert()
    
    # vec aligned to local axis in Blender 2.8+
    # in previous versions: vec_rot = vec * inv
    vec_rot = vec @ inv
    new_obj.location = new_obj.location + vec_rot
  
    


def copy_z():
    C = bpy.context
    bricks = [obj for obj in bpy.data.objects if obj.name.startswith(mesh_name)]
    
    
    z = 0

    for i in bricks:


        ########################
        ###### copy brick ######
        ########################
        new_obj = i.copy()
        new_obj.animation_data_clear()
        C.collection.objects.link(i)  


        ########################
        ###### move brick ######
        ########################
          

        z += 0.6

        # one blender unit in x-direction
        vec = mathutils.Vector((0.0, 0.0, z))
        inv = i.matrix_world.copy()
        inv.invert()

        # vec aligned to local axis in Blender 2.8+
        # in previous versions: vec_rot = vec * inv
        vec_rot = vec @ inv
        i.location = i.location + vec_rot


        
make_brick_wall()    

        

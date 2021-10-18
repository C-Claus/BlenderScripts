
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


    new_mesh = bpy.data.meshes.new('new_mesh')
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
      
        
        x += 2.3
    
        # one blender unit in x-direction
        vec = mathutils.Vector((x, 0.0, 0.0))
        inv = new_obj.matrix_world.copy()
        inv.invert()
        
        # vec aligned to local axis in Blender 2.8+
        # in previous versions: vec_rot = vec * inv
        vec_rot = vec @ inv
        new_obj.location = new_obj.location + vec_rot
        
    
    
    
make_brick_wall()    


def add_brick():
    
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


    new_mesh = bpy.data.meshes.new('new_mesh')
    new_mesh.from_pydata(vertices_waalformaat, edges, faces)
    new_mesh.update()

    # make object from mesh
    new_object = bpy.data.objects.new(mesh_name, new_mesh)

    # make collection
    new_collection = bpy.data.collections.new('Collection')
    #bpy.context.scene.collection.children.link(new_collection)

    # add object to scene collection
    new_collection.objects.link(new_object)


    return bpy.data.collections['Collection'].objects.link(new_object)
    
  

def array(self, obj):
    mod = bpy.data.objects[obj.name].modifiers.new(name='array', type='ARRAY')
    mod.count = 10
    mod.relative_offset_displace[0] = 2.5
    

def move_brick():
    cube = bpy.data.objects[mesh_name]
    
    # one blender unit in x-direction
    vec = mathutils.Vector((2.2, 0.0, 0.0))
    inv = cube.matrix_world.copy()
    inv.invert()
    
    # vec aligned to local axis in Blender 2.8+
    # in previous versions: vec_rot = vec * inv
    vec_rot = vec @ inv
    cube.location = cube.location + vec_rot
    
    
def copy_brick(amount):
    C = bpy.context
    src_obj = bpy.context.active_object

    for i in range (0,amount):
        new_obj = src_obj.copy()
        new_obj.data = src_obj.data.copy()
        new_obj.animation_data_clear()
        C.collection.objects.link(new_obj)  
        
        
"""       
def copy_brick_array():
    
    brick_list = [obj for obj in bpy.data.objects if obj.name.startswith("IfcWallStandardCase")]
    
    z=0
    
    C = bpy.context
    for bricks in brick_list:
        
        new_obj = bricks.copy()
        new_obj.data = bricks.data.copy()
        new_obj.animation_data_clear()
        C.collection.objects.link(new_obj) 
        
        
        
        z += 0.6
        
        vec = mathutils.Vector((0.0, 0.0, z))
        inv = i.matrix_world.copy()
        inv.invert()
        
        # vec aligned to local axis in Blender 2.8+
        # in previous versions: vec_rot = vec * inv
        vec_rot = vec @ inv
        i.location = i.location + vec_rot
        
    
    print (z)

""" 


def make_brick_array():
    foo_objs = [obj for obj in bpy.data.objects if obj.name.startswith(mesh_name)]

    x = 0
    y = 0
    z = 0
    
    for i in foo_objs[1:-1]:
        print (i)
        
        x += 2.3
        #y += 
        #z += 0.6
        
        vec = mathutils.Vector((x, 0.0, 0.0))
        inv = i.matrix_world.copy()
        inv.invert()
        
        # vec aligned to local axis in Blender 2.8+
        # in previous versions: vec_rot = vec * inv
        vec_rot = vec @ inv
        i.location = i.location + vec_rot
        
    print (x)
    
    
  
#add brick mesh  
#add_brick()

#select object and copy mesh
#copy_brick(amount=5)

#move the copied meshes within an array
#make_brick_array()

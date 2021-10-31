import bpy
import mathutils

bl_info = {
    "name": "BlenderBrick",
    "blender": (2, 80, 0),
    "category": "Object",
}


def update_cube_dimensions(self, context):
    if context.scene.cube is None:
        return
    
    #name_collection="blender_brick"
    #collection_name = bpy.data.collections.new(name_collection)
    #bpy.context.scene.collection.children.link(collection_name)
    
    
    context.scene.cube.dimensions = context.scene.cube_dimensions
    
    x,y,z = context.scene.cube.dimensions
  
    
    
  
   
 
    obj = context.scene.cube        
    new_obj = obj.copy()
    new_obj.animation_data_clear()
    
    # one blender unit in x-direction
    vec = mathutils.Vector((x, y, z))
    inv = new_obj.matrix_world.copy()
    inv.invert()
    
    # vector aligned to local axis in Blender 2.8+
    vec_rot = vec @ inv
    new_obj.location = new_obj.location + vec_rot 
    
    #obj.users_collection[0].link(new_obj)
    
    bpy.context.collection[0].objects.link(obj)

    

class BlenderBrickPanel(bpy.types.Panel):
    """Creates a Panel in the 3D Viewport N Panel"""
    bl_label = "Hello World Panel"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "BlenderBrick"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(context.scene, "cube_dimensions")
        row = layout.row()
        row.prop(context.scene, "cube")


def register():
    bpy.types.Scene.cube_dimensions = bpy.props.FloatVectorProperty(name="Brick Dimensions", min=0.01, default=(2, 2, 2), update=update_cube_dimensions)
    bpy.types.Scene.cube = bpy.props.PointerProperty(type=bpy.types.Object)

    bpy.utils.register_class(BlenderBrickPanel)


def unregister():
    del bpy.types.Scene.cube
    del bpy.types.Scene.cube_dimensions
    bpy.utils.unregister_class(BlenderBrickPanel)


if __name__ == "__main__":
    register()
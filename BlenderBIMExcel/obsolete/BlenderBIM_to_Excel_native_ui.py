import bpy


bl_info = {
    "name": "BlenderBIM Excel",
    "blender": (2, 80, 0),
    "category": "Object",
}


def update_cube_dimensions(self, context):
    if context.scene.cube is None:
        return
    context.scene.cube.dimensions = context.scene.cube_dimensions


class BlenderBIMExcelPanel(bpy.types.Panel):
    """Creates a Panel in the 3D Viewport N Panel"""
    bl_label = "Blender BIM Excel"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "BlenderBIM Excel"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(context.scene, "cube_dimensions")
        row = layout.row()
        row.prop(context.scene, "cube")


def register():
    #bpy.types.Scene.cube_dimensions = bpy.props.FloatVectorProperty(name="Cube Dimensions", min=0.01, default=(2, 2, 2), update=update_cube_dimensions)
    bpy.types.Scene.cube = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.utils.register_class(BlenderBIMExcelPanel)


def unregister():
    del bpy.types.Scene.cube
    del bpy.types.Scene.cube_dimensions
    bpy.utils.unregister_class(BlenderBIMExcel)


if __name__ == "__main__":
    register()
import bpy



class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"


    def execute(self, context):
        print("Hello World !")
        return {'FINISHED'}


class HelloWorldPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Hello World Panel"
    bl_idname = "OBJECT_PT_hello"  # this is not strictly necessary
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tools"

    def draw(self, context):
        # Here we create the button and link it to the operator class' bl_idname unique identifier :
        self.layout.operator("object.simple_operator")
        # You can also use :
        self.layout.operator(SimpleOperator.bl_idname)
        # You can use a custom text :
        self.layout.operator(SimpleOperator.bl_idname, text="My custom button text !")
        # You can use a custom icon :
        self.layout.operator(SimpleOperator.bl_idname, text="My custom button text !", icon="WORLD")
        # Tip : enable Icon Viewer addon to have a list of available icons
        # https://docs.blender.org/manual/en/latest/addons/development/icon_viewer.html

        # You can use just an icon :
        self.layout.operator(SimpleOperator.bl_idname, text="", icon="WORLD")


def register():
    bpy.utils.register_class(SimpleOperator)
    bpy.utils.register_class(HelloWorldPanel)


def unregister():
    bpy.utils.unregister_class(HelloWorldPanel)
    bpy.utils.unregister_class(SimpleOperator)


if __name__ == "__main__":
    register()
import bpy
from bpy.types import Scene
from bpy.props import BoolProperty
from bpy.props import FloatProperty
from bpy.props import IntProperty


class ExplodeProperties(bpy.types.PropertyGroup):

    my_reference_image:           bpy.props.StringProperty(           name="Image",
                                                                        description="path to your reference image",
                                                                        default="",
                                                                        maxlen=1024,
                                                                        subtype="FILE_PATH"
                                                                        )

def register():
   
    bpy.utils.register_class(ExplodeProperties)
    bpy.types.Scene.explode_properties = bpy.props.PointerProperty(type=ExplodeProperties)
  

def unregister():
   
    bpy.utils.unregister_class(ExplodeProperties)
    del bpy.types.Scene.explode_properties

                                                                      
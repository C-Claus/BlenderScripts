
import bpy
from bpy.types import Scene
from bpy.props import BoolProperty
from bpy.props import FloatProperty
from bpy.props import IntProperty


class ImageProperties(bpy.types.PropertyGroup):

    my_reference_image_A:           bpy.props.StringProperty(           name="Reference Image A",
                                                                        description="path to your reference image",
                                                                        default="",
                                                                        maxlen=1024,
                                                                        subtype="FILE_PATH")

def register():
    bpy.utils.register_class(ImageProperties)
    bpy.types.Scene.image_properties = bpy.props.PointerProperty(type=ImageProperties)

def unregister():
 
    bpy.utils.unregister_class(ImageProperties)
    del bpy.types.Scene.image_properties
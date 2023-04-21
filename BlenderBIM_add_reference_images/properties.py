
import bpy
from bpy.types import Scene
from bpy.props import BoolProperty
from bpy.props import FloatProperty
from bpy.props import IntProperty


class ImageProperties(bpy.types.PropertyGroup):

    my_reference_image_A:           bpy.props.StringProperty(         name="Reference Image A",
                                                                        description="path to your reference image",
                                                                        default="",
                                                                        maxlen=1024,
                                                                        subtype="FILE_PATH")
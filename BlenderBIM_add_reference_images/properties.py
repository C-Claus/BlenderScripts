
import bpy
from bpy.types import Scene
from bpy.props import BoolProperty
from bpy.props import FloatProperty
from bpy.props import IntProperty


class ImageProperties(bpy.types.PropertyGroup):

    my_reference_image:           bpy.props.StringProperty(           name="Image",
                                                                        description="path to your reference image",
                                                                        default="",
                                                                        maxlen=1024,
                                                                        subtype="FILE_PATH"
                                                                        )

class ImageItem(bpy.types.PropertyGroup):
    #name: bpy.props.StringProperty(name         ="Property",
    #                               description  ="Use the PropertySet name and Property name divided by a .",
    #                               default      ="PropertySet.Property"
    #                               )

    image:           bpy.props.StringProperty(              name="Image",
                                                            description="path to your reference image",
                                                            default="",
                                                            subtype="FILE_PATH")                               
    
class ImageCollection(bpy.types.PropertyGroup):
    items: bpy.props.CollectionProperty(type=ImageItem)


def register():
    bpy.utils.register_class(ImageItem)
    bpy.utils.register_class(ImageCollection)
    bpy.utils.register_class(ImageProperties)
    bpy.types.Scene.image_properties = bpy.props.PointerProperty(type=ImageProperties)
    bpy.types.Scene.image_collection = bpy.props.PointerProperty(type=ImageCollection)

def unregister():
    bpy.utils.unregister_class(ImageItem)
    bpy.utils.unregister_class(ImageCollection)
    bpy.utils.unregister_class(ImageProperties)
    del bpy.types.Scene.image_properties
    del bpy.types.Scene.image_collection
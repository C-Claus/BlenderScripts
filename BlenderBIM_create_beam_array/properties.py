
import bpy
from bpy.types import Scene

# For more information about Blender Properties, visit:
# <https://blender.org/api/blender_python_api_2_78a_release/bpy.types.Property.html>
from bpy.props import BoolProperty
# from bpy.props import CollectionProperty
# from bpy.props import EnumProperty
from bpy.props import FloatProperty
from bpy.props import IntProperty
# from bpy.props import PointerProperty
# from bpy.props import StringProperty
# from bpy.props import PropertyGroup

#
# Add additional functions or classes here
#
def update_length(self, context):
    self.my_length = (self.my_n * round(self.my_center_to_center_distance,2)) #- round(self.my_center_to_center_distance,2)
class DimensionProperties(bpy.types.PropertyGroup):

    my_height: bpy.props.FloatProperty(default=3.0, min=1, max=100, name="Height")
    my_n: bpy.props.IntProperty(default=10,name="N", step=1, min=2, max=100, update=update_length)
    my_center_to_center_distance: bpy.props.FloatProperty(default=1, min=0.1, max=100, name="Center to Center", update=update_length)
    my_length: bpy.props.FloatProperty(default=10,name="Length")

    #my_n: bpy.props.IntProperty(default=1,name="N", step=1, min=2, max=100)
    #my_height: bpy.props.FloatProperty(default=0.1, min=1, max=100, name="Height")
    #my_center_to_center_distance: bpy.props.FloatProperty(default=0.01, min=0.01, max=100, name="Center to Center")

   

    my_profile_x: bpy.props.FloatProperty(default=0.1, min=1, max=100)
    my_profile_y: bpy.props.FloatProperty(default=0.1, min=0.1, max=100)



    my_covering_exterior: bpy.props.BoolProperty(default=True)
    my_covering_interior: bpy.props.BoolProperty(default=True)
    my_insulation: bpy.props.BoolProperty(default=True)


# This is where you assign any variables you need in your script. Note that they
# won't always be assigned to the Scene object but it's a good place to start.
def register():
    bpy.utils.register_class(DimensionProperties)
    Scene.my_beam_foundation = BoolProperty(default=True)

    bpy.types.Scene.dimension_properties = bpy.props.PointerProperty(type=DimensionProperties)

def unregister():
    del Scene.my_beam_foundation
    bpy.utils.unregister_class(DimensionProperties)
    #bpy.utils.unregister_class(DimensionProperties)
    del bpy.types.Scene.dimension_properties



import bpy
from bpy.types import Scene
from bpy.props import BoolProperty
from bpy.props import FloatProperty
from bpy.props import IntProperty

def update_length(self, context):
    self.my_length = (self.my_n * round(self.my_center_to_center_distance,2)) #- round(self.my_center_to_center_distance,2)
class DimensionProperties(bpy.types.PropertyGroup):

    my_ifcfile:           bpy.props.StringProperty(         name="IFC",
                                                            description="path to your IFC",
                                                            default="",
                                                            maxlen=1024,
                                                            subtype="FILE_PATH")

    my_height: bpy.props.FloatProperty(default=3.0, min=1, max=100, name="Height")
    my_n: bpy.props.IntProperty(default=10,name="N", step=1, min=2, max=100, update=update_length)
    my_center_to_center_distance: bpy.props.FloatProperty(default=1, min=0.1, max=100, name="Center to Center", update=update_length)
    my_length: bpy.props.FloatProperty(default=10,name="Length")

    my_profile_x: bpy.props.IntProperty(default=50, step=1, min=10, max=10000, name='Profile X')
    my_profile_y: bpy.props.IntProperty(default=200,step=1, min=10, max=10000, name='Profile Y')

    my_covering_exterior_thickness: bpy.props.FloatProperty(default=0.02, min=0.01, max=100, name="Covering Exterior thickness")
    my_covering_interior_thickness: bpy.props.FloatProperty(default=0.02, min=0.01, max=100, name="Covering Interior thickness")

    my_covering_exterior: bpy.props.BoolProperty(default=True, name='Include Exterior Covering')
    my_covering_interior: bpy.props.BoolProperty(default=True, name='Include Interior Covering')
    my_insulation: bpy.props.BoolProperty(default=True, name='Include Insulation')

    

    


def register():
    bpy.utils.register_class(DimensionProperties)
    Scene.my_beam_foundation = BoolProperty(default=True)
    bpy.types.Scene.dimension_properties = bpy.props.PointerProperty(type=DimensionProperties)

def unregister():
    del Scene.my_beam_foundation
    bpy.utils.unregister_class(DimensionProperties)
    del bpy.types.Scene.dimension_properties


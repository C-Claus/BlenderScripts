import os
import bpy

from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper 
from bpy.types import Operator



class SimpleOperator(bpy.types.Operator, ImportHelper):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Open Excel"
    
    filter_glob: StringProperty(
    default='*.xlsx;*',
    options={'HIDDEN'}
    )
    
    some_boolean: BoolProperty(
        name="open Excel file",
        description='open the excel file',
        default=True,
    )


    def execute(self, context):
        
        print("Hello World !")
        
        filename, extension = os.path.splitext(self.filepath)
        
        print ('selected file', self.filepath)
        print ('selected name', filename)
        
        #global excel_file
        #excel_file = self.filepath
        os.startfile(self.filepath)
        
        return {'FINISHED'}
    
class FilterIFCElements(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.filter_ifc_elements"
    bl_label = "Simple Object Operator"


    def execute(self, context):
        print("filter IFC elements")
        
        #print (excel_file)
        return {'FINISHED'}
    


class BlenderBIMExcelPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "BlenderBIM Excel"
    bl_idname = "OBJECT_PT_hello"  # this is not strictly necessary
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tools"

    def draw(self, context):
        
        

        self.layout.operator(SimpleOperator.bl_idname, text="Open Excel File", icon="FILE_FOLDER")
        
        self.layout.operator(FilterIFCElements.bl_idname, text="Filter IFC elements", icon="FILTER")
        # Tip : enable Icon Viewer addon to have a list of available icons
        # https://docs.blender.org/manual/en/latest/addons/development/icon_viewer.html



def register():
    bpy.utils.register_class(SimpleOperator)
    bpy.utils.register_class(FilterIFCElements)
    bpy.utils.register_class(BlenderBIMExcelPanel)


def unregister():
    bpy.utils.unregister_class(BlenderBIMExcelPanel)
    bpy.utils.unregister_class(SimpleOperator)
    bpy.utils.register_class(FilterIFCElements)


if __name__ == "__main__":
    register()
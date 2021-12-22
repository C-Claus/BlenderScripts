import os
import bpy
from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper 
from bpy.types import Operator

import openpyxl
from openpyxl import load_workbook

import blenderbim.bim.import_ifc
from blenderbim.bim.ifc import IfcStore
import blenderbim.tool as tool

class WriteToExcel(bpy.types.Operator):
    """Write IFC data to Excel"""
    bl_idname = "object.write_to_excel"
    bl_label = "Simple Object Operator"


    def execute(self, context):
        print("Write to Excel")
        
    
        return {'FINISHED'}



class OpenExcelFile(bpy.types.Operator, ImportHelper):
    """Open an existing Excel file"""
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
        
        global excel_file
        excel_file = self.filepath
        os.startfile(self.filepath)
        
        return {'FINISHED'}
    
class FilterIFCElements(bpy.types.Operator):
    """Show the IFC elements you filtered in Excel"""
    bl_idname = "object.filter_ifc_elements"
    bl_label = "select the IFC elements"


    def execute(self, context):
        print("filter IFC elements")
        
        print (excel_file)
        
        workbook_openpyxl = load_workbook(excel_file)
        worksheet_openpyxl = workbook_openpyxl['IfcProduct'] 
        
        global_id_filtered_list = []

        for row in worksheet_openpyxl:     
            if worksheet_openpyxl.row_dimensions[row[0].row].hidden == False:
                for cell in row:  
                    if cell in worksheet_openpyxl['A']:  
                        global_id_filtered_list.append(cell.value)
                        
         
        
        outliner = next(a for a in bpy.context.screen.areas if a.type == "OUTLINER") 
        outliner.spaces[0].show_restrict_column_viewport = not outliner.spaces[0].show_restrict_column_viewport
        
        bpy.ops.object.select_all(action='DESELECT')
      
        for obj in bpy.context.view_layer.objects:
            element = tool.Ifc.get_entity(obj)
            if element is None:        
                obj.hide_viewport = True
                continue
            data = element.get_info()
          
            obj.hide_viewport = data.get("GlobalId", False) not in global_id_filtered_list[1:]

        bpy.ops.object.select_all(action='SELECT') 
        
        return {'FINISHED'}
    
 
class UnhideIFCElements(bpy.types.Operator):
    """Unhide all IFC elements"""
    bl_idname = "object.unhide_all"
    bl_label = "Unhide All"


    def execute(self, context):
        print("Unhide all")
        
        for obj in bpy.data.objects:
            obj.hide_viewport = False 
        
    
        return {'FINISHED'}      
               
     
    


class BlenderBIMExcelPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "BlenderBIM Excel"
    bl_idname = "OBJECT_PT_hello"  # this is not strictly necessary
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tools"

    def draw(self, context):
        
        
        self.layout.operator(WriteToExcel.bl_idname, text="Write to Excel", icon="FILE")
        self.layout.operator(OpenExcelFile.bl_idname, text="Open Excel File", icon="FILE_FOLDER")
        
        self.layout.operator(FilterIFCElements.bl_idname, text="Filter IFC elements", icon="FILTER")
        #self.layout.operator(UnhideIFCElements.bl_idname, text="Unhide IFC elements", icon="LAMP")
        
        
        # Tip : enable Icon Viewer addon to have a list of available icons
        # https://docs.blender.org/manual/en/latest/addons/development/icon_viewer.html



def register():
    bpy.utils.register_class(WriteToExcel)
    bpy.utils.register_class(OpenExcelFile)
    bpy.utils.register_class(FilterIFCElements)
    bpy.utils.register_class(UnhideIFCElements)
    bpy.utils.register_class(BlenderBIMExcelPanel)


def unregister(): 
    bpy.utils.unregister_class(WriteToExcel)
    bpy.utils.unregister_class(OpenExcelFile)
    bpy.utils.unregister_class(FilterIFCElements)
    bpy.utils.unregister_class(UnhideIFCElements)
    bpy.utils.unregister_class(BlenderBIMExcelPanel)


if __name__ == "__main__":
    register()
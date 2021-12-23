import os
import bpy
from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper 
from bpy.types import Operator

import openpyxl
from openpyxl import load_workbook
import pandas as pd
import xlsxwriter

import blenderbim.bim.import_ifc
from blenderbim.bim.ifc import IfcStore
import blenderbim.tool as tool

import ifcopenshell

class WriteToExcel(bpy.types.Operator):
    """Write IFC data to Excel"""
    bl_idname = "object.write_to_excel"
    bl_label = "Simple Object Operator"


    def execute(self, context):
        print("Write to Excel")
        
        header_index = 2
        ifc_dictionary = {}
        sheet_name_custom = 'IfcProduct'
        
        global_id_list = []
        ifc_product_type_list = []
        ifc_product_name_list = []
        ifc_building_storey_list = []
        ifc_classification_list = []
        ifc_materials_list = []
        ifc_isexternal_list = []
        ifc_loadbearing_list = []
        ifc_firerating_list = []
        
        
        excel_file = IfcStore.path.replace('.ifc','_blenderbim.xlsx')   
        ifc_file = ifcopenshell.open(IfcStore.path)
        products = ifc_file.by_type('IfcProduct')
        
        
        for product in products:
            global_id_list.append(product.GlobalId)
            ifc_product_type_list.append(str(product.is_a()))
            ifc_product_name_list.append(str(product.Name))
            ifc_building_storey_list.append(self.get_ifcbuildingstorey(context, ifcproduct=product)[0])
            ifc_classification_list.append(self.get_classification_code(context, ifcproduct=product)[0])
            ifc_materials_list.append(self.get_materials(context, ifcproduct=product)[0])
            
        ifc_dictionary['GlobalId'] = global_id_list
        ifc_dictionary['IfcProduct'] = ifc_product_type_list
        ifc_dictionary['Name'] = ifc_product_name_list
        ifc_dictionary['IfcBuildingStorey'] = ifc_building_storey_list
        ifc_dictionary['Classification'] = ifc_classification_list
        ifc_dictionary['Materials'] = ifc_materials_list
            
         
        df = pd.DataFrame(ifc_dictionary)
        writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    
        df.to_excel(writer, sheet_name=sheet_name_custom, startrow=1, header=False, index=False)
        
        workbook  = writer.book
        worksheet = writer.sheets[sheet_name_custom]
        
        
        (max_row, max_col) = df.shape
         
        # Create a list of column headers, to use in add_table().
        column_settings = []
        for header in df.columns:
            column_settings.append({'header': header})

        # Add the table.
        worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})

        # Make the columns wider for clarity.
        worksheet.set_column(0, max_col - 1, 30)

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()
        os.startfile(excel_file)
        
    
        return {'FINISHED'}
    
    def get_ifcbuildingstorey(self, context, ifcproduct):
        building_storey_list = []
         
        try:
            if ifcproduct:
                if ifcproduct.ContainedInStructure:            
                    if ifcproduct.ContainedInStructure[0].RelatingStructure.is_a() == 'IfcBuildingStorey':
                        building_storey_list.append(ifcproduct.ContainedInStructure[0].RelatingStructure.Name)
        except:
            pass
        else:
            pass

        #IfcOpeningElement should not be linked directly to the spatial structure of the project,
        #i.e. the inverse relationship ContainedInStructure shall be NIL.
        #It is assigned to the spatial structure through the elements it penetrates.
        if len(building_storey_list) == 0:
            building_storey_list.append('N/A')
             
        return building_storey_list 
    
    def get_classification_code(self, context, ifcproduct):
    
        #Classifications of an object may be referenced from an external source rather than being
        #contained within the IFC model. This is done through the IfcClassificationReference class.
        
        assembly_code_list = []

        if ifcproduct.HasAssociations:
            if ifcproduct.HasAssociations[0].is_a() == 'IfcRelAssociatesClassification':
                assembly_code_list.append(ifcproduct.HasAssociations[0].RelatingClassification.ItemReference)
                
            if ifcproduct.HasAssociations[0].is_a() == 'IfcRelAssociatesMaterial':
                for i in ifcproduct.HasAssociations:
                    if i.is_a() == 'IfcRelAssociatesClassification' :
                        assembly_code_list.append(i.RelatingClassification.ItemReference)
                
                                               
        if len(assembly_code_list) == 0:
            assembly_code_list.append('N/A')
            
        if assembly_code_list[0] == None:
            assembly_code_list.append('N/A')
            
        return assembly_code_list
    
    def get_materials(self, context, ifcproduct):
        
        material_list = []
        
        if ifcproduct.HasAssociations:
            for i in ifcproduct.HasAssociations:
                if i.is_a('IfcRelAssociatesMaterial'):
                    
                    if i.RelatingMaterial.is_a('IfcMaterial'):
                        material_list.append(i.RelatingMaterial.Name)
                       
                    if i.RelatingMaterial.is_a('IfcMaterialList'):
                        for materials in i.RelatingMaterial.Materials:
                            material_list.append(materials.Name)
                             
                    if i.RelatingMaterial.is_a('IfcMaterialLayerSetUsage'):
                        for materials in i.RelatingMaterial.ForLayerSet.MaterialLayers:
                            material_list.append(materials.Material.Name)
                            
                    else:
                        pass
                          
        if len(material_list) == 0:
            material_list.append('N/A')
           
        joined_material_list = ' | '.join(material_list)
                             
        return [joined_material_list] 
        
    



class OpenExcelFile(bpy.types.Operator, ImportHelper):
    """Open an existing Excel file"""
    bl_idname = "object.open_excel"
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
    
    filepath:bpy.props.StringProperty(subtype="FILE_PATH")


    def execute(self, context):
        
        print("Open Excel")
        
        filename, extension = os.path.splitext(self.filepath)
        
        print ('selected file', self.filepath)
        print ('selected name', filename)
        
        global excel_file
        excel_file = self.filepath
        os.startfile(self.filepath)
        
        return {'FINISHED'}
    
class ShowExcelFile(bpy.types.Operator):
    """Show Excel file"""
    bl_idname = "object.show_excel"
    bl_label = "Show Path to Excel file"
    
    filepath:bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        print("Show Excel")
        
        return {'FINISHED'}
    
    
class FilterIFCElements(bpy.types.Operator):
    """Show the IFC elements you filtered in Excel"""
    bl_idname = "object.filter_ifc_elements"
    bl_label = "select the IFC elements"
    

    def execute(self, context):
        print("filter IFC elements")
        
 
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
    bl_idname = "OBJECT_PT_blenderbimpanel"  # this is not strictly necessary
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tools"

    def draw(self, context):
        
        self.layout.operator(WriteToExcel.bl_idname, text="Write to Excel", icon="FILE")
        self.layout.operator(OpenExcelFile.bl_idname, text="Open Excel File", icon="FILE_FOLDER")
        
        #self.layout.label(text="File location: {}")
        #self.layout.operator(OpenExcelFile.bl_idname, text="Open Excel folder location", icon="FILE_FOLDER")
        
        self.layout.operator(FilterIFCElements.bl_idname, text="Filter IFC elements", icon="FILTER")
        self.layout.operator(UnhideIFCElements.bl_idname, text="Unhide IFC elements", icon="LIGHT")
        
        # Tip : enable Icon Viewer addon to have a list of available icons
        # https://docs.blender.org/manual/en/latest/addons/development/icon_viewer.html



def register():
    bpy.utils.register_class(WriteToExcel)
    bpy.utils.register_class(OpenExcelFile)
    bpy.utils.register_class(ShowExcelFile)
    bpy.utils.register_class(FilterIFCElements)
    bpy.utils.register_class(UnhideIFCElements)
    bpy.utils.register_class(BlenderBIMExcelPanel)


def unregister(): 
    bpy.utils.unregister_class(WriteToExcel)
    bpy.utils.unregister_class(OpenExcelFile)
    bpy.utils.unregister_class(ShowExcelFile)
    bpy.utils.unregister_class(FilterIFCElements)
    bpy.utils.unregister_class(UnhideIFCElements)
    bpy.utils.unregister_class(BlenderBIMExcelPanel)


if __name__ == "__main__":
    register()
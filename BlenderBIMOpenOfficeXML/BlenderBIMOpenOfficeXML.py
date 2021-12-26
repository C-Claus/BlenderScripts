bl_info = {
    "name": "BlenderBIM Office Open XML",
    "author": "C. Claus",
    "version": (1, 0, 0),
    "blender": (2, 93, 6),
    "location": "Tools",
    "description": "BlenderBIM xlsx",
    "warning": "Requires installation of dependencies pandas, xlsxwriter and openpyxl",
    "support": "COMMUNITY",
    }
    

import os
import sys

import subprocess
import bpy
from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper 
from bpy.types import (Operator, PropertyGroup)

import blenderbim.bim.import_ifc
from blenderbim.bim.ifc import IfcStore
import blenderbim.tool as tool

import ifcopenshell

py_exec = str(sys.executable)
# ensure pip is installed
subprocess.call([py_exec, "-m", "ensurepip", "--user" ])
# update pip (not mandatory but highly recommended)
#subprocess.call([py_exec, "-m", "pip", "install", "--upgrade", "pip" ])
# install packages
subprocess.call([py_exec,"-m", "pip", "install", f"--target={py_exec[:-14]}" + "lib", "openpyxl"])

subprocess.call([py_exec,"-m", "pip", "install", f"--target={py_exec[:-14]}" + "lib", "pandas"])

subprocess.call([py_exec,"-m", "pip", "install", f"--target={py_exec[:-14]}" + "lib", "xlsxwriter"])

import openpyxl
from openpyxl import load_workbook
import pandas as pd
import xlsxwriter

class WriteToXLSX(bpy.types.Operator):
    """Write IFC data to .xlsx"""
    bl_idname = "object.write_to_xlsx"
    bl_label = "Simple Object Operator"


    def execute(self, context):
        print("Write to .xlsx")
   
        ifc_dictionary = {}
        
        global sheet_name_custom
        sheet_name_custom = 'Overview'
        
        global_id_list = []
        ifc_product_type_list = []
        ifc_product_name_list = []
        ifc_product_type_name_list = []
        ifc_building_storey_list = []
        ifc_classification_list = []
        ifc_materials_list = []
        ifc_isexternal_list = []
        ifc_loadbearing_list = []
        ifc_firerating_list = []
        
        ifc_quantities_length_list = []
        ifc_quantities_width_list = []
        ifc_quantities_height_list = []
        ifc_quantities_area_list = []
        ifc_quantities_volume_list = []
        ifc_quantities_perimeter_list = []
        
        global excel_file
        
        excel_file = IfcStore.path.replace('.ifc','_blenderbim.xlsx')   
        ifc_file = ifcopenshell.open(IfcStore.path)
        products = ifc_file.by_type('IfcProduct')
        
        
        for product in products:
            global_id_list.append(product.GlobalId)
            ifc_product_type_list.append(str(product.is_a()))
            
         
            ifc_product_name_list.append(str(product.Name))
            ifc_product_type_name_list.append(self.get_ifcproducttype_name(context, ifcproduct=product)[0])
            ifc_building_storey_list.append(self.get_ifcbuildingstorey(context, ifcproduct=product)[0])
            ifc_classification_list.append(self.get_classification_code(context, ifcproduct=product)[0])
            ifc_materials_list.append(self.get_materials(context, ifcproduct=product)[0])
            ifc_isexternal_list.append(self.get_isexternal(context, ifcproduct=product)[0])
            ifc_loadbearing_list.append(self.get_loadbearing(context, ifcproduct=product)[0])
            ifc_firerating_list.append(self.get_firerating(context, ifcproduct=product)[0])
            
            ifc_quantities_length_list.append(self.get_quantities_length(context, ifcproduct=product)[0])
            ifc_quantities_width_list.append(self.get_quantities_width(context, ifcproduct=product)[0])
            ifc_quantities_height_list.append(self.get_quantities_height(context, ifcproduct=product)[0])
            ifc_quantities_area_list.append(self.get_quantities_area(context, ifcproduct=product)[0])
            ifc_quantities_volume_list.append(self.get_quantities_volume(context, ifcproduct=product)[0])
            ifc_quantities_perimeter_list.append(self.get_quantities_perimeter(context, ifcproduct=product)[0])
            
        ifc_dictionary['GlobalId'] = global_id_list
        
        ##################################################################
        ########################### General #############################
        ##################################################################
        if context.scene.my_ifcproduct == True:
            ifc_dictionary['IfcProduct'] = ifc_product_type_list
            
        if context.scene.my_ifcbuildingstorey == True:  
            ifc_dictionary['IfcBuildingStorey'] = ifc_building_storey_list
            
        if context.scene.my_ifcproduct_name == True:  
            ifc_dictionary['Name'] = ifc_product_name_list
          
        if context.scene.my_type == True:    
            ifc_dictionary['Type'] = ifc_product_type_name_list
            
        if context.scene.my_ifcclassification == True:     
            ifc_dictionary['Classification'] = ifc_classification_list
              
        if context.scene.my_ifcmaterial == True:   
            ifc_dictionary['Materials'] = ifc_materials_list
            
        ##################################################################
        ######################## Pset_*Common ############################
        ##################################################################    
        if context.scene.my_isexternal == True:   
            ifc_dictionary['IsExternal'] = ifc_isexternal_list
            
        if context.scene.my_loadbearing == True:  
            ifc_dictionary['LoadBearing'] = ifc_loadbearing_list
            
        if context.scene.my_firerating == True:   
            ifc_dictionary['FireRating'] = ifc_firerating_list
            
            
        ##################################################################
        ##################### Base Quantities ############################
        ##################################################################
        if context.scene.my_length == True:  
            ifc_dictionary['Length'] = ifc_quantities_length_list
        
        if context.scene.my_width == True:  
            ifc_dictionary['Width'] = ifc_quantities_width_list
            
        if context.scene.my_height == True:
            ifc_dictionary['Height'] = ifc_quantities_height_list
           
        if context.scene.my_area == True: 
            ifc_dictionary['Area'] = ifc_quantities_area_list
            #ifc_dictionary["Area" & '=SUBTOTAL(109,N3:N' + str(len(products)) + ')'] = ifc_quantities_area_list  
            
        if context.scene.my_volume == True: 
            ifc_dictionary['Volume'] = ifc_quantities_volume_list
            
        if context.scene.my_perimeter == True: 
            ifc_dictionary['Perimeter'] = ifc_quantities_perimeter_list
            
         
        df = pd.DataFrame(ifc_dictionary)
        writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    
        df.to_excel(writer, sheet_name=sheet_name_custom, startrow=1, header=False, index=False)
        
        workbook  = writer.book
  
        cell_format = workbook.add_format({'bold': True,'border': 1,'bg_color': '#4F81BD','font_color': 'white','font_size':14})
        
        
        worksheet = writer.sheets[sheet_name_custom]
        #worksheet.write('A1', str(IfcStore.path), cell_format)
        
        
        (max_row, max_col) = df.shape
         
        # Create a list of column headers, to use in add_table().
        column_settings = []
        for header in df.columns:
            column_settings.append({'header': header})

        # Add the table.
        worksheet.add_table(1, 0, max_row, max_col - 1, {'columns': column_settings})

        # Make the columns wider for clarity.
        worksheet.set_column(0, max_col - 1, 30)
        
        
        
        
          
        #find out from the pandas dataframe in which column the calculation needs to be positioned.
        for header_name in df.columns:
            if header_name == 'Area':
                col_no = df.columns.get_loc("Area")
                column_letter = (xlsxwriter.utility.xl_col_to_name(col_no))
                
                #Works in MS Excel, but not in LibreOffice
                #="Area: " &SUBTOTAL(109;F2:F3821)
               
                total_area='=SUBTOTAL(109,' + str(column_letter) + '3:' + str(column_letter) + str(len(products)) + ')'
                worksheet.write_formula(str(column_letter)+'1', total_area)
                
            if header_name == 'Volume':
                col_no = df.columns.get_loc("Volume")
                column_letter = (xlsxwriter.utility.xl_col_to_name(col_no))
                
                total_volume='=SUBTOTAL(109,' + str(column_letter) + '3:' + str(column_letter) + str(len(products)) + ')'
                worksheet.write_formula(str(column_letter)+'1', total_volume)
                

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()
        os.startfile(excel_file)
        
    
        return {'FINISHED'}
    
    def get_ifcproducttype_name(self, context, ifcproduct):
        
        type_name_list = []
        
        if ifcproduct:
            type_name_list.append(ifcproduct.ObjectType)
            
        if len(type_name_list) == 0:
            type_name_list.append('N/A')
            
        if type_name_list[0] == None:
            type_name_list.append('N/A')
        
        return type_name_list
    
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
    
    def get_isexternal(self, context, ifcproduct):
        
        externality_list = []
     
        if ifcproduct.IsDefinedBy:
            if ifcproduct.IsDefinedBy[0]:
                if ifcproduct.IsDefinedBy[0].is_a() == 'IfcRelDefinesByProperties':
                    if ifcproduct.IsDefinedBy[0].RelatingPropertyDefinition.is_a() == 'IfcPropertySet':
                        for ifcproperty in ifcproduct.IsDefinedBy[0].RelatingPropertyDefinition.HasProperties:
                            if ifcproperty.Name == 'IsExternal':
                                #externality_list.append(ifcproperty.Name)
                                externality_list.append(ifcproperty.NominalValue[0])
                            else:
                                pass
                                        
        if len(externality_list) == 0:
            externality_list.append('N/A')  

        return externality_list
    
    def get_loadbearing(self, context,ifcproduct):
        load_bearing_list = []
        
        if ifcproduct.IsDefinedBy:
            if ifcproduct.IsDefinedBy[0]:
                if ifcproduct.IsDefinedBy[0].is_a() == 'IfcRelDefinesByProperties':
                    if ifcproduct.IsDefinedBy[0].RelatingPropertyDefinition.is_a() == 'IfcPropertySet':
                        for ifcproperty in ifcproduct.IsDefinedBy[0].RelatingPropertyDefinition.HasProperties:
                            if ifcproperty.Name == 'LoadBearing':
                                load_bearing_list.append(ifcproperty.NominalValue[0])
                            else:
                                pass
                                        
        if len(load_bearing_list) == 0:
            load_bearing_list.append('N/A')
                             
        return load_bearing_list
    
    def get_firerating(self, context, ifcproduct):
        fire_rating_list = []    
        
        if ifcproduct.IsDefinedBy:
            if ifcproduct.IsDefinedBy[0]:
                if ifcproduct.IsDefinedBy[0].is_a() == 'IfcRelDefinesByProperties':
                    if ifcproduct.IsDefinedBy[0].RelatingPropertyDefinition.is_a() == 'IfcPropertySet':
                        for ifcproperty in ifcproduct.IsDefinedBy[0].RelatingPropertyDefinition.HasProperties:
                            if ifcproperty.Name == 'FireRating':
                                fire_rating_list.append(ifcproperty.Name)
                                fire_rating_list.append(ifcproperty.NominalValue[0])
                            else:
                                pass
                                        
        if len(fire_rating_list) == 0:
            fire_rating_list.append('N/A')
                             
        return [fire_rating_list]
    
    def get_quantities_length(self, context, ifcproduct):
    
        quantity_length_list = []

        
        for properties in ifcproduct.IsDefinedBy:
            if properties.is_a('IfcRelDefinesByProperties'):
                if properties.RelatingPropertyDefinition.is_a('IfcElementQuantity'):
                    for quantities in properties.RelatingPropertyDefinition.Quantities:
                        if (quantities.Name) == 'Length':
                            quantity_length_list.append(float(quantities.LengthValue))
                            
        if len(quantity_length_list) == 0:
            quantity_length_list.append(None)
                  
        return quantity_length_list
    
    
    def get_quantities_width(self, context, ifcproduct):
    
        quantity_width_list = []

        
        for properties in ifcproduct.IsDefinedBy:
            if properties.is_a('IfcRelDefinesByProperties'):
                if properties.RelatingPropertyDefinition.is_a('IfcElementQuantity'):
                    for quantities in properties.RelatingPropertyDefinition.Quantities:
                        if (quantities.Name) == 'Width':
                            quantity_width_list.append(float(quantities.LengthValue))
                            
        if len(quantity_width_list) == 0:
            quantity_width_list.append(None)
                  
        return quantity_width_list
    
    def get_quantities_height(self, context, ifcproduct):
    
        quantity_height_list = []

        for properties in ifcproduct.IsDefinedBy:
            if properties.is_a('IfcRelDefinesByProperties'):
                if properties.RelatingPropertyDefinition.is_a('IfcElementQuantity'):
                    for quantities in properties.RelatingPropertyDefinition.Quantities:
                        if (quantities.Name) == 'Height':
                            quantity_height_list.append(float(quantities.LengthValue))
                            
        if len(quantity_height_list) == 0:
            quantity_height_list.append(None)
              
        return quantity_height_list
    
    def get_quantities_area(self, context, ifcproduct):
    
        quantity_area_list = []

        for properties in ifcproduct.IsDefinedBy:
            if properties.is_a('IfcRelDefinesByProperties'):
                if properties.RelatingPropertyDefinition.is_a('IfcElementQuantity'):
                    for quantities in properties.RelatingPropertyDefinition.Quantities:
                         if quantities.Name == 'NetArea' or (quantities.Name) == 'NetSideArea':
                            quantity_area_list.append(float(quantities.AreaValue))
                            
        if len(quantity_area_list) == 0:
            quantity_area_list.append(None)                
                  
        return quantity_area_list
    
    def get_quantities_volume(self, context,ifcproduct):
    
        quantity_volume_list = []

        for properties in ifcproduct.IsDefinedBy:
            if properties.is_a('IfcRelDefinesByProperties'):
                if properties.RelatingPropertyDefinition.is_a('IfcElementQuantity'):
                    for quantities in properties.RelatingPropertyDefinition.Quantities:
                        if (quantities.Name) == 'Net Volume':
                            quantity_volume_list.append(float(quantities.VolumeValue))
                            
        if len(quantity_volume_list) == 0:
            quantity_volume_list.append(None) 
          
        return quantity_volume_list
    
    def get_quantities_perimeter(self, context, ifcproduct):
    
        quantity_perimeter_list = []
        
        if ifcproduct.is_a().startswith('IfcSlab'):
            for properties in ifcproduct.IsDefinedBy:
                if properties.is_a('IfcRelDefinesByProperties'):
                    if properties.RelatingPropertyDefinition.is_a('IfcElementQuantity'):
                        for quantities in properties.RelatingPropertyDefinition.Quantities:
                             if quantities.Name == 'Perimeter':
                                quantity_perimeter_list.append(str(quantities.LengthValue))
                                
        if len(quantity_perimeter_list) == 0:
            quantity_perimeter_list.append(None)
                                                                       
        return quantity_perimeter_list   
                
    



class OpenXLSXFile(bpy.types.Operator, ImportHelper):
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
        
        print("Open .xlsx file")
        
        filename, extension = os.path.splitext(self.filepath)
        
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
        
    
        
        workbook_openpyxl = load_workbook(excel_file)
        worksheet_openpyxl = workbook_openpyxl[sheet_name_custom] 
        
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
    
    


class BlenderBIMXLSXPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "BlenderBIM .xlsx"
    bl_idname = "OBJECT_PT_blenderbimxlsxpanel"  # this is not strictly necessary
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tools"
    

    def draw(self, context):
        
        layout = self.layout
        scene = context.scene
        
        
        layout.label(text="General")
        box = layout.box()
        row = box.row()
        row.prop(scene, "my_ifcproduct")
        row = box.row()
        row.prop(scene, "my_ifcbuildingstorey")
        row = box.row()
        row.prop(scene, "my_ifcproduct_name")
        row = box.row()
        row.prop(scene, "my_type")
        row = box.row()
        row.prop(scene, "my_ifcclassification")
        row = box.row()
        row.prop(scene, "my_ifcmaterial")
        
        
        layout.label(text="Pset_Common")
        box = layout.box()
        row = box.row()
        row.prop(scene, "my_isexternal")
        row = box.row()
        row.prop(scene, "my_loadbearing")
        row = box.row()
        row.prop(scene, "my_firerating")
        
        
        layout.label(text="BaseQuantities")
        box = layout.box()
        row = box.row()
        row.prop(scene, "my_length")
        row = box.row()
        row.prop(scene, "my_width")
        row = box.row()
        row.prop(scene, "my_height")
        row = box.row()
        row.prop(scene, "my_area")
        row = box.row()
        row.prop(scene, "my_volume")
        row = box.row()
        row.prop(scene, "my_perimeter")
        
        
     
        self.layout.operator(WriteToXLSX.bl_idname, text="Write IFC data to .xlsx", icon="FILE")
        self.layout.operator(OpenXLSXFile.bl_idname, text="Open .xlsx file", icon="FILE_FOLDER")
        self.layout.operator(FilterIFCElements.bl_idname, text="Filter IFC elements", icon="FILTER")
        self.layout.operator(UnhideIFCElements.bl_idname, text="Unhide IFC elements", icon="LIGHT")
        
     



def register():
    
   
    bpy.types.Scene.my_ifcproduct = bpy.props.BoolProperty(name="IfcProduct",description="Export IfcProduct",default = True)
    bpy.types.Scene.my_ifcbuildingstorey = bpy.props.BoolProperty(name="IfcBuildingStorey",description="Export IfcBuildingStorey",default = True)     
    bpy.types.Scene.my_ifcproduct_name = bpy.props.BoolProperty(name="Name",description="Export IfcProduct Name",default = True)
    bpy.types.Scene.my_type = bpy.props.BoolProperty(name="Type",description="Export IfcObjectType Name",default = True)    
    bpy.types.Scene.my_ifcclassification = bpy.props.BoolProperty(name="IfcClassification",description="Export Classification",default = True)  
    bpy.types.Scene.my_ifcmaterial = bpy.props.BoolProperty(name="IfcMaterial",description="Export Materials",default = True)  
    
    bpy.types.Scene.my_isexternal = bpy.props.BoolProperty(name="IsExternal",description="Export IsExternal",default = True)    
    bpy.types.Scene.my_loadbearing = bpy.props.BoolProperty(name="LoadBearing",description="Export LoadBearing",default = True)  
    bpy.types.Scene.my_firerating = bpy.props.BoolProperty(name="FireRating",description="Export FireRating",default = True)
    
    bpy.types.Scene.my_length = bpy.props.BoolProperty(name="Length",description="Export Length from BaseQuantities",default = True)  
    bpy.types.Scene.my_width = bpy.props.BoolProperty(name="Width",description="Export Width from BaseQuantities",default = True)   
    bpy.types.Scene.my_height = bpy.props.BoolProperty(name="Height",description="Export Height from BaseQuantities",default = True) 
    bpy.types.Scene.my_area = bpy.props.BoolProperty(name="Area",description="Export Area from BaseQuantities",default = True)  
    bpy.types.Scene.my_volume = bpy.props.BoolProperty(name="Volume",description="Export Volume from BaseQuantities",default = True) 
    bpy.types.Scene.my_perimeter = bpy.props.BoolProperty(name="Perimeter",description="Export Perimeter from BaseQuantities",default = True)      
  
    
    
 
            
    bpy.utils.register_class(WriteToXLSX)
    bpy.utils.register_class(OpenXLSXFile)
    bpy.utils.register_class(FilterIFCElements)
    bpy.utils.register_class(UnhideIFCElements)
    bpy.utils.register_class(BlenderBIMXLSXPanel)


def unregister(): 
    bpy.utils.unregister_class(WriteToXLSX)
    bpy.utils.unregister_class(OpenXLSXFile)
    bpy.utils.unregister_class(FilterIFCElements)
    bpy.utils.unregister_class(UnhideIFCElements)
    bpy.utils.unregister_class(BlenderBIMXLSXPanel)
    
    del bpy.types.Scene.my_prop


if __name__ == "__main__":
    register()
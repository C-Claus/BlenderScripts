bl_info = {
    "name": "BlenderBIM OpenOffice XML",
    "author": "C. Claus",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "Tools",
    "description": "BlenderBIM spreadsheet",
    "support": "COMMUNITY",
    }
  
import os
import sys
import time
import site

python_packages_folder = "libs/site/packages"
site.addsitedir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "libs", "site", "packages"))

import bpy
from bpy.props import StringProperty, BoolProperty, IntProperty, EnumProperty
from bpy_extras.io_utils import ImportHelper 
from bpy.types import (Operator, PropertyGroup)


import blenderbim.bim.import_ifc
from blenderbim.bim.ifc import IfcStore
import blenderbim.tool as tool
import ifcopenshell


import openpyxl
from openpyxl import load_workbook
import pandas as pd
import xlsxwriter
import numpy as np
from collections import defaultdict


print ('openpyxl', openpyxl.__version__, openpyxl.__file__)
print ('pandas',pd.__version__, pd.__file__)
print ('xlsxwriter',xlsxwriter.__version__, xlsxwriter.__file__)

class WriteToXLSX(bpy.types.Operator):
    """Write IFC data to .xlsx"""
    bl_idname = "object.write_to_xlsx"
    bl_label = "Simple Object Operator"
    

    def execute(self, context):
        print("Write to .xlsx")
        
        start_time = time.perf_counter()
        
        blenderbim_openoffice_xml_properties = context.scene.blenderbim_openoffice_xml_properties
        my_collection = context.scene.my_collection
        
        print('sheet name: ', blenderbim_openoffice_xml_properties.my_workbook)
        print ('xlsx file: ', blenderbim_openoffice_xml_properties.my_xlsx_file)
        
        ifc_dictionary = defaultdict(list)
        ifc_custom_property_list = []
        
        blenderbim_openoffice_xml_properties.my_workbook = 'Overview'
        blenderbim_openoffice_xml_properties.my_xlsx_file  = IfcStore.path.replace('.ifc','_blenderbim.xlsx') 
        ods_file = IfcStore.path.replace('.ifc','_blenderbim.ods')  
        
        ifc_file = ifcopenshell.open(IfcStore.path)
        products = ifc_file.by_type('IfcProduct')
        

        for product in products:
            
            ##################################################################
            ##########################  GlobalId #############################
            ##################################################################
            ifc_dictionary['GlobalId'].append(str(product.GlobalId))
            
             
            ##################################################################
            ########################### General ##############################
            ##################################################################
            if blenderbim_openoffice_xml_properties.my_ifcproduct:  # 'if condition is True:' is the same as  'if condition:'
                ifc_dictionary['IfcProduct'].append(str(product.is_a()))
                
          
            if blenderbim_openoffice_xml_properties.my_ifcbuildingstorey:  
                ifc_dictionary['IfcBuildingStorey'].append(self.get_ifcbuildingstorey(context, ifcproduct=product,)[0])    
    
           
            if blenderbim_openoffice_xml_properties.my_ifcproduct_name: 
                ifc_dictionary['Name'].append(str(product.Name))
                
            
            if blenderbim_openoffice_xml_properties.my_type:     
                ifc_dictionary['Type'].append(self.get_ifcproducttype_name(context, ifcproduct=product)[0])
            
            if blenderbim_openoffice_xml_properties.my_ifcclassification: 
                ifc_dictionary['Classification'].append(self.get_classification_code(context, ifcproduct=product)[0])
              
            if blenderbim_openoffice_xml_properties.my_ifcmaterial:     
                ifc_dictionary['Material(s)'].append(self.get_materials(context, ifcproduct=product)[0])
                
            
            ##################################################################
            ################### Common Properties ############################
            ##################################################################    
            if blenderbim_openoffice_xml_properties.my_isexternal:    
                ifc_dictionary['IsExternal'].append(self.get_isexternal(context, ifcproduct=product)[0])
                
            if blenderbim_openoffice_xml_properties.my_loadbearing:     
                ifc_dictionary['LoadBearing'].append(self.get_loadbearing(context, ifcproduct=product)[0])
                
            if blenderbim_openoffice_xml_properties.my_firerating:    
                ifc_dictionary['FireRating'].append(self.get_firerating(context, ifcproduct=product)[0])
            
          
            ##################################################################
            ##################### Base Quantities ############################
            ##################################################################
            if blenderbim_openoffice_xml_properties.my_length: 
                ifc_dictionary['Length'].append(self.get_quantities_length(context, ifcproduct=product)[0])
                
            if blenderbim_openoffice_xml_properties.my_width:     
                ifc_dictionary['Width'].append(self.get_quantities_width(context, ifcproduct=product)[0])
                
            if blenderbim_openoffice_xml_properties.my_height:    
                ifc_dictionary['Height'].append(self.get_quantities_height(context, ifcproduct=product)[0])
                  
            if blenderbim_openoffice_xml_properties.my_area:     
                ifc_dictionary['Area'].append(self.get_quantities_area(context, ifcproduct=product)[0])
                
            if blenderbim_openoffice_xml_properties.my_volume:    
                ifc_dictionary['Volume'].append(self.get_quantities_volume(context, ifcproduct=product)[0])
                
            if blenderbim_openoffice_xml_properties.my_perimeter:    
                ifc_dictionary['Perimeter'].append(self.get_quantities_perimeter(context, ifcproduct=product)[0])
                
                
            ##################################################################
            ################### Custom Properties ############################
            ##################################################################
         
            if len(context.scene.my_collection.items) > 1:
                for item in context.scene.my_collection.items:
                    ifc_dictionary[item.name].append(self.get_custom_pset( context,ifcproduct=product,
                                                                    pset_name=str(item.name).split('.')[0],
                                                                    property_name=str(item.name).split('.')[1])[0])   
      

        
        df = pd.DataFrame(ifc_dictionary)
        writer = pd.ExcelWriter(blenderbim_openoffice_xml_properties.my_xlsx_file, engine='xlsxwriter')
        #writer = pd.ExcelWriter(excel_file, engine='odf')
    
        df.to_excel(writer, sheet_name=blenderbim_openoffice_xml_properties.my_workbook, startrow=1, header=False, index=False)
        
        workbook  = writer.book
        #cell_format = workbook.add_format({'bold': True,'border': 1,'bg_color': '#4F81BD','font_color': 'white','font_size':14})
        
        worksheet = writer.sheets[blenderbim_openoffice_xml_properties.my_workbook]
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
        os.startfile(blenderbim_openoffice_xml_properties.my_xlsx_file)
        
        print (time.perf_counter() - start_time, "seconds for the .xlsx to be written")
        
    
        return {'FINISHED'}
    
    
    def get_ifcproducttype_name(self, context, ifcproduct):
        
        type_name_list = []
        
        if ifcproduct:
            type_name_list.append(ifcproduct.ObjectType)
            
        if not type_name_list:
            type_name_list.append(None)
        
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


        #IfcOpeningElement should not be linked directly to the spatial structure of the project,
        #i.e. the inverse relationship ContainedInStructure shall be NIL.
        #It is assigned to the spatial structure through the elements it penetrates.
        if not building_storey_list:
            building_storey_list.append(None)
             
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
                
                                               
        if not assembly_code_list:
            assembly_code_list.append(None)
     
            
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
                          
        if not material_list:
            material_list.append('N/A')
           
        joined_material_list = ' | '.join(material_list)
                             
        return [joined_material_list] 
    
    def get_isexternal(self, context, ifcproduct):
        
        externality_list = []
        
        property_name = 'IsExternal'
     
        if ifcproduct.IsDefinedBy:        
            for ifcreldefinesbyproperties in ifcproduct.IsDefinedBy:
                if (ifcreldefinesbyproperties.is_a()) == 'IfcRelDefinesByProperties':
                    if ifcreldefinesbyproperties.RelatingPropertyDefinition.is_a() == 'IfcPropertySet':
                        if (ifcreldefinesbyproperties.RelatingPropertyDefinition.Name).endswith('Common'):
                            
                            for ifcproperty in (ifcreldefinesbyproperties.RelatingPropertyDefinition.HasProperties):
                                if (ifcproperty.Name == property_name):
                                    #externality_list.append(ifcproperty.Name)
                                    externality_list.append(ifcproperty.NominalValue[0])
                                        
        if not externality_list:
            externality_list.append(None)  

        return externality_list
    
    def get_loadbearing(self, context,ifcproduct):
        load_bearing_list = []
        
        property_name = 'LoadBearing'
        
        if ifcproduct.IsDefinedBy:        
            for ifcreldefinesbyproperties in ifcproduct.IsDefinedBy:
                if (ifcreldefinesbyproperties.is_a()) == 'IfcRelDefinesByProperties':
                    if ifcreldefinesbyproperties.RelatingPropertyDefinition.is_a() == 'IfcPropertySet':
                        if (ifcreldefinesbyproperties.RelatingPropertyDefinition.Name).endswith('Common'):
                           
                            for ifcproperty in (ifcreldefinesbyproperties.RelatingPropertyDefinition.HasProperties):
                                if (ifcproperty.Name == property_name):
                                    load_bearing_list.append(ifcproperty.NominalValue[0])
                            else:
                                pass
                                        
        if not load_bearing_list:
            load_bearing_list.append(None)
                             
        return load_bearing_list
    
    def get_firerating(self, context, ifcproduct):
        fire_rating_list = []    
        
        property_name = 'FireRating'
        
        if ifcproduct.IsDefinedBy:        
            for ifcreldefinesbyproperties in ifcproduct.IsDefinedBy:
                if (ifcreldefinesbyproperties.is_a()) == 'IfcRelDefinesByProperties':
                    if ifcreldefinesbyproperties.RelatingPropertyDefinition.is_a() == 'IfcPropertySet':
                        if (ifcreldefinesbyproperties.RelatingPropertyDefinition.Name).endswith('Common'):
                           
                            for ifcproperty in (ifcreldefinesbyproperties.RelatingPropertyDefinition.HasProperties):
                                if (ifcproperty.Name == property_name):

                                    fire_rating_list.append(ifcproperty.NominalValue[0])
                            else:
                                pass
                                        
        if not fire_rating_list:
            fire_rating_list.append(None)
                             
        return fire_rating_list
    
    def get_quantities_length(self, context, ifcproduct):
    
        quantity_length_list = []

        
        for properties in ifcproduct.IsDefinedBy:
            if properties.is_a('IfcRelDefinesByProperties'):
                if properties.RelatingPropertyDefinition.is_a('IfcElementQuantity'):
                    for quantities in properties.RelatingPropertyDefinition.Quantities:
                        if (quantities.Name) == 'Length':
                            quantity_length_list.append(float(quantities.LengthValue))
                            
        if not quantity_length_list:
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
                            
        if not quantity_width_list:
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
                            
        if not quantity_height_list:
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
                            
        if not quantity_area_list:
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
                            
        if not quantity_volume_list:
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
                                
        if not quantity_perimeter_list:
            quantity_perimeter_list.append(None)
                                                                       
        return quantity_perimeter_list   

    def get_custom_pset(self, context, ifcproduct, pset_name, property_name):
        

        custom_pset_list = []
        
        if ifcproduct.IsDefinedBy:        
            for ifcreldefinesbyproperties in ifcproduct.IsDefinedBy:
                if (ifcreldefinesbyproperties.is_a()) == 'IfcRelDefinesByProperties':
                    if ifcreldefinesbyproperties.RelatingPropertyDefinition.is_a() == 'IfcPropertySet':
                        if pset_name in (ifcreldefinesbyproperties.RelatingPropertyDefinition.Name):
                            for ifcproperty in (ifcreldefinesbyproperties.RelatingPropertyDefinition.HasProperties):
                                
                                if (ifcproperty.Name == property_name):
                                    custom_pset_list.append(ifcproperty.NominalValue[0])
                      
                                        
        if not custom_pset_list:
            custom_pset_list.append(None)
                             
        return custom_pset_list
        

class OpenXLSXFile(bpy.types.Operator, ImportHelper):
    """Open an existing XML file"""
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
        blenderbim_openoffice_xml_properties = context.scene.blenderbim_openoffice_xml_properties
        blenderbim_openoffice_xml_properties.my_xlsx_file  = IfcStore.path.replace('.ifc','_blenderbim.xlsx') 
        filename, extension = os.path.splitext(self.filepath)
        
        #global excel_file
        blenderbim_openoffice_xml_properties.my_xlsx_file = self.filepath
        os.startfile(self.filepath)
        
        return {'FINISHED'}
    
    
    
class FilterIFCElements(bpy.types.Operator):
    """Show the IFC elements you filtered in Excel"""
    bl_idname = "object.filter_ifc_elements"
    bl_label = "select the IFC elements"
    

    def execute(self, context):
        
        print("filter IFC elements")
        
        start_time = time.perf_counter()
   
        blenderbim_openoffice_xml_properties = context.scene.blenderbim_openoffice_xml_properties
        blenderbim_openoffice_xml_properties.my_xlsx_file  = IfcStore.path.replace('.ifc','_blenderbim.xlsx') 
        blenderbim_openoffice_xml_properties.my_workbook = 'Overview'
        
        workbook_openpyxl = load_workbook(blenderbim_openoffice_xml_properties.my_xlsx_file)
        worksheet_openpyxl = workbook_openpyxl[blenderbim_openoffice_xml_properties.my_workbook] 
        
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
        
        print (time.perf_counter() - start_time, "seconds to show the IFC elements")
        
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

    bl_label = "BlenderBIM spreadsheet"
    bl_idname = "OBJECT_PT_blenderbimxlsxpanel"  # this is not strictly necessary
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tools"
 
   
    def draw(self, context):
        
        layout = self.layout
        blenderbim_openoffice_xml_properties = context.scene.blenderbim_openoffice_xml_properties
        
        layout.label(text="General")
        box = layout.box()
        row = box.row()
        row.prop(blenderbim_openoffice_xml_properties, "my_ifcproduct")
        row = box.row()
        row.prop(blenderbim_openoffice_xml_properties, "my_ifcbuildingstorey")
        row = box.row()
        row.prop(blenderbim_openoffice_xml_properties, "my_ifcproduct_name")
        row = box.row()
        row.prop(blenderbim_openoffice_xml_properties, "my_type")
        row = box.row()
        row.prop(blenderbim_openoffice_xml_properties, "my_ifcclassification")
        row = box.row()
        row.prop(blenderbim_openoffice_xml_properties, "my_ifcmaterial")
        
        layout.label(text="Common Properties")
        box = layout.box()
        row = box.row()
        row.prop(blenderbim_openoffice_xml_properties, "my_isexternal")
        row = box.row()
        row.prop(blenderbim_openoffice_xml_properties, "my_loadbearing")
        row = box.row()
        row.prop(blenderbim_openoffice_xml_properties, "my_firerating")
        
        layout.label(text="BaseQuantities")
        box = layout.box()
        row = box.row()
        row.prop(blenderbim_openoffice_xml_properties, "my_length")
        row = box.row()
        row.prop(blenderbim_openoffice_xml_properties, "my_width")
        row = box.row()
        row.prop(blenderbim_openoffice_xml_properties, "my_height")
        row = box.row()
        row.prop(blenderbim_openoffice_xml_properties, "my_area")
        row = box.row()
        row.prop(blenderbim_openoffice_xml_properties, "my_volume")
        row = box.row()
        row.prop(blenderbim_openoffice_xml_properties, "my_perimeter")
        

        
        #layout = self.layout
        layout.label(text="Custom Properties")
        my_collection = context.scene.my_collection
       
        row = layout.row(align=True)
        row.operator("my.collection_actions", text="Add", icon="ADD").action = "add"
        row.operator("my.collection_actions", text="Remove Last", icon="REMOVE").action = "remove"

        for item in my_collection.items:
            layout.prop(item, "name")
        

        layout.label(text="Write to .xlsx")
        self.layout.operator(WriteToXLSX.bl_idname, text="Write IFC data to .xlsx", icon="FILE")
        self.layout.operator(OpenXLSXFile.bl_idname, text="Open .xlsx file", icon="FILE_FOLDER")
        
        layout.label(text="Filter")
        self.layout.operator(FilterIFCElements.bl_idname, text="Filter IFC elements", icon="FILTER")
        self.layout.operator(UnhideIFCElements.bl_idname, text="Unhide IFC elements", icon="LIGHT")
    
        
        

class BlenderBIMOpenOfficeXMLProperties(bpy.types.PropertyGroup):
    
    ###############################################
    ################# General #####################
    ############################################### 
    my_ifcproduct: bpy.props.BoolProperty(name="IfcProduct",description="Export IfcProduct",default=True)
    my_ifcbuildingstorey: bpy.props.BoolProperty(name="IfcBuildingStorey",description="Export IfcBuildingStorey",default = True)     
    my_ifcproduct_name: bpy.props.BoolProperty(name="Name",description="Export IfcProduct Name",default = True)
    my_type: bpy.props.BoolProperty(name="Type",description="Export IfcObjectType Name",default = True)
    my_ifcclassification: bpy.props.BoolProperty(name="IfcClassification",description="Export Classification",default = True)
    my_ifcmaterial: bpy.props.BoolProperty(name="IfcMaterial",description="Export Materials",default = True)
     
    ###############################################
    ############ Common Properties ################
    ###############################################
    my_isexternal: bpy.props.BoolProperty(name="IsExternal",description="Export IsExternal",default = True)
    my_loadbearing: bpy.props.BoolProperty(name="LoadBearing",description="Export LoadBearing",default = True)
    my_firerating: bpy.props.BoolProperty(name="FireRating",description="Export FireRating",default = True)
    
    ###############################################
    ############# BaseQuantities ##################
    ###############################################
    my_length: bpy.props.BoolProperty(name="Length",description="Export Length from BaseQuantities",default = True)  
    my_width: bpy.props.BoolProperty(name="Width",description="Export Width from BaseQuantities",default = True)   
    my_height: bpy.props.BoolProperty(name="Height",description="Export Height from BaseQuantities",default = True) 
    my_area: bpy.props.BoolProperty(name="Area",description="Export Area from BaseQuantities",default = True)  
    my_volume: bpy.props.BoolProperty(name="Volume",description="Export Volume from BaseQuantities",default = True) 
    my_perimeter: bpy.props.BoolProperty(name="Perimeter",description="Export Perimeter from BaseQuantities",default = True)      
  
    ###############################################
    ####### Spreadsheet Properties ################
    ###############################################
    my_workbook: bpy.props.StringProperty(name="my_workbook")
    my_xlsx_file: bpy.props.StringProperty(name="my_xlsx_file")

    
    
    
class MyItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Property",description="Use the PropertySet name and Property name divided by a .",default = "[PropertySet.Property]") 

class MyCollection(bpy.types.PropertyGroup):
    items: bpy.props.CollectionProperty(type=MyItem)

class MyCollectionActions(bpy.types.Operator):
    bl_idname = "my.collection_actions"
    bl_label = "Execute"
    action: bpy.props.EnumProperty(
        items=(
            ("add",) * 3,
            ("remove",) * 3,
        ),
    )
    def execute(self, context):
        my_collection = context.scene.my_collection
        if self.action == "add":           
            item = my_collection.items.add()  # Here keep a handle on the last added item. You can then change its name or whatever afterwards
        if self.action == "remove":
            my_collection.items.remove(len(my_collection.items) - 1)
        return {"FINISHED"}



def register():
    bpy.utils.register_class(MyItem)
    bpy.utils.register_class(MyCollection)
    
    bpy.types.Scene.my_collection = bpy.props.PointerProperty(type=MyCollection)
    bpy.utils.register_class(MyCollectionActions)
    
    
    
    bpy.utils.register_class(BlenderBIMOpenOfficeXMLProperties)
    bpy.types.Scene.blenderbim_openoffice_xml_properties = bpy.props.PointerProperty(type=BlenderBIMOpenOfficeXMLProperties)       
    bpy.utils.register_class(WriteToXLSX)
    bpy.utils.register_class(OpenXLSXFile)
    bpy.utils.register_class(FilterIFCElements)
    bpy.utils.register_class(UnhideIFCElements)
    bpy.utils.register_class(BlenderBIMXLSXPanel)
    
def unregister(): 
    
    bpy.utils.unregister_class(MyItem)
    bpy.utils.unregister_class(MyCollection)
    bpy.utils.unregister_class(MyCollectionActions)
    
    
    
    bpy.utils.unregister_class(BlenderBIMOpenOfficeXMLProperties)
    bpy.utils.unregister_class(WriteToXLSX)
    bpy.utils.unregister_class(OpenXLSXFile)
    bpy.utils.unregister_class(FilterIFCElements)
    bpy.utils.unregister_class(UnhideIFCElements)
    bpy.utils.unregister_class(BlenderBIMXLSXPanel)
    

if __name__ == "__main__":
    register()
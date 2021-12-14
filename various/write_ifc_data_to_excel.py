import os
import bpy
import openpyxl
import ifcopenshell
import xlsxwriter

import logging
import blenderbim.bim.import_ifc

from openpyxl import load_workbook
from blenderbim.bim.ifc import IfcStore


def write_to_excel(ifc_file, excel_file):
    
    ifc_file = ifcopenshell.open(ifc_file)
    products = ifc_file.by_type('IfcProduct')
    
    workbook_xlsx = xlsxwriter.Workbook(excel_file)
    worksheet_xlsx = workbook_xlsx.add_worksheet('IfcProduct')
    
    product_entity_list = [['A1','GlobalId'],['B1','IfcProduct'],['C1','Name'],['D1','Description']]
    
    for i, product_entity in enumerate(product_entity_list):
        worksheet_xlsx.write(product_entity[0], product_entity[1])
        worksheet_xlsx.set_column(i, 1, 25)

    worksheet_xlsx.autofilter('A1:D' + str(len(products)) )

    for i, product in enumerate(products):
        worksheet_xlsx.write('A' + str(i+2), str(product.GlobalId))
        worksheet_xlsx.write('B' + str(i+2), str(product.is_a()))
        worksheet_xlsx.write('C' + str(i+2), str(product.Name))
        worksheet_xlsx.write('D' + str(i+2), str(product.Description))

    workbook_xlsx.close()
    os.startfile(excel_file)
   


def get_filtered_data_from_excel(excel_file):
    workbook_openpyxl = load_workbook(excel_file)
    worksheet_openpyxl = workbook_openpyxl['IfcProduct'] 
    
    global_id_filtered_list = []

    for row in worksheet_openpyxl:     
        if worksheet_openpyxl.row_dimensions[row[0].row].hidden == False:
            for cell in row:  
                if cell in worksheet_openpyxl['A']:  
                    global_id_filtered_list.append(cell.value)
                    
    return global_id_filtered_list[1:]
                
                                            
def select_IFC_elements_in_blender(guid_list):
   
    for guid in guid_list:
        bpy.ops.bim.select_global_id(global_id=guid)
        
         
       
excel_file_path = (os.path.dirname(IfcStore.path) + '\\' + (os.path.basename(IfcStore.path).replace('.ifc','.xlsx')) )

#1 needs to  happen on user input
write_to_excel(ifc_file=IfcStore.path, excel_file=excel_file_path)

#2 check if excel is running and saved before using this function
#select_IFC_elements_in_blender(guid_list=get_filtered_data_from_excel(excel_file=excel_file_path) )   


#mini backlog
#1. export propertyset to a sheet
#2. export materials to a sheet
#3. export quantities to a sheet
#4. find out how to bundle python dependencies in a blender add-on
#5. small user interface with pyqt or blender
#6. check if excel is installed on the system or running
#7. refactor function write_to_excel()
#8. write back data from excel into ifc
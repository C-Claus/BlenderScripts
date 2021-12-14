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
    
    
    workbook = xlsxwriter.Workbook(excel_file)
    worksheet = workbook.add_worksheet('IfcProduct')

    #cell_format = workbook.add_format({'bold': True, 'font_color': 'red'})
    #worksheet.set_row(0, 1, cell_format)


    worksheet.write('A1', 'GlobalId')
    worksheet.write('B1', 'IfcProduct')
    worksheet.write('C1', 'Name')

    worksheet.set_column(0, 1, 25)
    worksheet.set_column(1, 1, 25)
    worksheet.set_column(2, 1, 25)

    worksheet.autofilter('A1:C' + str(len(products)) )

    for i, product in enumerate(products):
        worksheet.write('A' + str(i+2), str(product.GlobalId))
        worksheet.write('B' + str(i+2), str(product.is_a()))
        worksheet.write('C' + str(i+2), str(product.Name))
        
    workbook.close()
    os.startfile(excel_file)


def get_filtered_data_from_excel(excel_file):
    wb = load_workbook(excel_file)
    ws = wb['IfcProduct'] 
    
    global_id_filtered_list = []
    
    #wb.save(filename = excel_file)

    for row in ws:     
        if ws.row_dimensions[row[0].row].hidden == False:
            for cell in row:  
                if cell in ws['A']:  
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



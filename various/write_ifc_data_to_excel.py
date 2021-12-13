import os
import pandas
import openpyxl
import ifcopenshell
import csv
import xlsxwriter

import bpy
import logging
import blenderbim.bim.import_ifc


from openpyxl import load_workbook

from blenderbim.bim.ifc import IfcStore




#excel_file = "C:\\Algemeen\\07_prive\\06_excel_vba\\BlenderBIM.xlsx"
#os.startfile(excel_file)

ifc_file_path = "C:\\Algemeen\\07_prive\\hooiberg.ifc"
excel_file_path = "C:\\Algemeen\\07_prive\\06_excel_vba\\BlenderBIM.xlsx"


#ifc_import_settings = blenderbim.bim.import_ifc.IfcImportSettings.factory(bpy.context, ifc_file_path, logging.getLogger('ImportIFC'))
#ifc_importer = blenderbim.bim.import_ifc.IfcImporter(ifc_import_settings)
#ifc_importer.execute()

ifc_file = ifcopenshell.open(ifc_file_path)

products = ifc_file.by_type('IfcProduct')


def write_to_excel():
    workbook = xlsxwriter.Workbook("C:\\Algemeen\\07_prive\\06_excel_vba\\BlenderBIM.xlsx")
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

    excel_file = "C:\\Algemeen\\07_prive\\06_excel_vba\\BlenderBIM.xlsx"
    os.startfile(excel_file)






def get_filtered_data_from_excel(excel_file):
    wb = load_workbook(excel_file) # use the actual path of your workbook
    ws = wb['IfcProduct'] # use your sheet name instead of Bar
    
    global_id_filtered_list = []

    # iterate over all the rows in the sheet
    for row in ws: 
        # use the row only if it has not been filtered out (i.e., it's not hidden)
        #if ws.row_dimensions[row[0].row].hidden == False:
        #    print (row) # ...or do what you need
   
            
        if ws.row_dimensions[row[0].row].hidden == False:
            for cell in row:  
                if cell in ws['A']:  
                    print (cell.value) 
                    global_id_filtered_list.append(cell.value)
                    
    return global_id_filtered_list[1:]
                
                
    
                
                
def hide_isolate_in_view(guid_list):
    print ('hide isolate in view')
    
    #bpy.ops.object.hide_view_clear()
  
    bpy.ops.object.select_all(action='DESELECT')

    
    for guid in guid_list:
        
        #bpy.context.scene.BIMSearchProperties.global_id = guid
        bpy.ops.bim.select_global_id(global_id=guid)


    #bpy.ops.object.hide_view_set(unselected=True)
    #bpy.data.objects.foreach_set("hide_viewport", (True,) * len(bpy.data.objects))

    #obj = bpy.context.active_object
    #IfcStore.get_file().by_id(obj.BIMObjectProperties.ifc_definition_id).GlobalId
    
            
#get_filtered_data_from_excel(excel_file=excel_file_path)        

#write_to_excel()
hide_isolate_in_view(guid_list=get_filtered_data_from_excel(excel_file=excel_file_path) )    
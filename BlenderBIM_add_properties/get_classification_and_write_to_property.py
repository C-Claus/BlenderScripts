
import ifcopenshell
import ifcopenshell.util.classification
import ifcopenshell.api
from ifcopenshell.api import run

ifc_file_path = "C:\\Users\\cclaus\\OneDrive - 4PS Group BV\\Bureaublad\\Sample models for BIM Client demo\\IFC2X3_Schependomlaan_structural_with_multiple_nlsfb_classifications_per_element.ifc"

ifc_file = ifcopenshell.open(ifc_file_path)

ifc_products = ifc_file.by_type('IfcProduct')



def get_ifc_classification(schema, ifc_product):
    
    classification_list = []

    # Elements may have multiple classification references assigned
    references = ifcopenshell.util.classification.get_references(ifc_product)
    
    if ifc_product:
        for i in references:
            if schema == 'IFC2X3':
                classification_list.append(i.ReferencedSource.Name)
                classification_list.append(i.ItemReference)
                classification_list.append(i.Name)
                classification_list.append('')

            if schema == 'IFC4':
                classification_list.append(i.ReferencedSource.Name)
                classification_list.append(i.Identification)
                classification_list.append(i.Name)
                classification_list.append('')

    if not classification_list:
        classification_list.append('None')  
        
    #joined_classification_list = '\n'.join(classification_list)
        
    print (classification_list)

for ifc_product in ifc_products:
    get_ifc_classification(schema=ifc_file.schema, ifc_product=ifc_product)


def assign_classification_as_propertyset():

    print ('assign propertyset')
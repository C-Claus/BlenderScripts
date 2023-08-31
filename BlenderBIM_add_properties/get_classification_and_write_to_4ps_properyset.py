import ifcopenshell
import ifcopenshell.util.classification
import ifcopenshell.api
from ifcopenshell.api import run
from blenderbim.bim.ifc import IfcStore

ifc_file_path = IfcStore.path
ifc_file = ifcopenshell.open(ifc_file_path)
ifc_products = ifc_file.by_type('IfcProduct')

# Elements may have multiple classification references assigned
for ifc_product in ifc_products:
    references = ifcopenshell.util.classification.get_references(ifc_product)

    for i in references:
        if ifc_file.schema == 'IFC2X3':
            if ifc_product:
                property_set  =  run("pset.add_pset", ifc_file, product=ifc_product, name="4PS Propertyset")
                run("pset.edit_pset", ifc_file, pset=property_set, properties={ "NL-SfB": str(i.ItemReference),
                                                                                "NL-SfB omschrijving": str(i.Name),
                                                                                "NL-SfB versie": str(i.ReferencedSource.Name)})
        if ifc_file.schema == 'IFC4':
                property_set  =  run("pset.add_pset", ifc_file, product=ifc_product, name="4PS Propertyset")
                run("pset.edit_pset", ifc_file, pset=property_set, properties={ "NL-SfB": str(i.Identification),
                                                                                "NL-SfB omschrijving": str(i.Name),
                                                                                "NL-SfB versie": str(i.ReferencedSource.Name)})
ifc_file.write(ifc_file_path)
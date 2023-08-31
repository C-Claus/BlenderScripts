#import bpy
import ifcopenshell
import ifcopenshell.api
from ifcopenshell.api import run
#import blenderbim.bim.ifc
#from blenderbim.bim.ifc import IfcStore
#from collections import OrderedDict
#ifc_file = ifcopenshell.open(IfcStore.path)

#ifc_file_path = "C:\\Users\\cclaus\\OneDrive - 4PS Group BV\Bureaublad\\Sample models for BIM Client demo\\IFC4 and IFC2X3 with and without classification\\IFC4_BIM_demo_excluding_classification.ifc"
#ifc_file_path = "C:\\Users\\cclaus\\OneDrive - 4PS Group BV\Bureaublad\\Sample models for BIM Client demo\\IFC4 and IFC2X3 with and without classification\\IFC4_BIM_demo_including_classification.ifc"

#ifc_file_path = "C:\\Users\\cclaus\\OneDrive - 4PS Group BV\Bureaublad\\Sample models for BIM Client demo\\IFC4 and IFC2X3 with and without classification\\IFC2X3_BIM_demo_excluding_classifcation.ifc"
ifc_file_path = "C:\\Users\\cclaus\\OneDrive - 4PS Group BV\Bureaublad\\Sample models for BIM Client demo\\IFC4 and IFC2X3 with and without classification\\IFC2X3_BIM_demo_including_classification.ifc"




ifc_file = ifcopenshell.open(ifc_file_path)

ifc_walls = ifc_file.by_type('IfcWall')

ifc_beams  = ifc_file.by_type('IfcBeam')

ifc_slabs = ifc_file.by_type('IfcSlab')

ifc_coverings = ifc_file.by_type('IfcCovering')

for ifc_beam in ifc_beams:

    if ifc_beam.Name == 'fundering':

        property_set  =  run("pset.add_pset", ifc_file, product=ifc_beam, name="4PS Propertyset")
        run("pset.edit_pset", ifc_file, pset=property_set, properties={ 
                                                                        "NL-SfB": "16.12",
                                                                        "NL-SfB omschrijving": "funderingsconstructies; voeten en balken, fundatie balken",
                                                                        "NL-SfB versie": "BIM Loket december 2019"
                                                                        })


for ifc_wall in ifc_walls:
  
    if ifc_wall.Name == 'buitenspouwblad':

        property_set  =  run("pset.add_pset", ifc_file, product=ifc_wall, name="4PS Propertyset")
        run("pset.edit_pset", ifc_file, pset=property_set, properties={ 
                                                                        "NL-SfB": "21.11",
                                                                        "NL-SfB omschrijving": "buitenwanden; niet constructief, massieve wanden",
                                                                        "NL-SfB versie": "BIM Loket december 2019"})

    if ifc_wall.Name == 'binnenspouwblad':

        property_set  =  run("pset.add_pset", ifc_file, product=ifc_wall, name="4PS Propertyset")
        run("pset.edit_pset", ifc_file, pset=property_set, properties={ 
                                                                        "NL-SfB": "21.21",
                                                                        "NL-SfB omschrijving": "binnenwanden; constructief, massieve wanden",
                                                                        "NL-SfB versie": "BIM Loket december 2019"})

for ifc_slab in ifc_slabs:

    if ifc_slab.Name == 'betonvloer_beganegrond':

        property_set  =  run("pset.add_pset", ifc_file, product=ifc_slab, name="4PS Propertyset")
        run("pset.edit_pset", ifc_file, pset=property_set, properties={ 
                                                                        "NL-SfB": "13.21",
                                                                        "NL-SfB omschrijving": "vloeren op grondslag; constructief, bodemafsluitingen",
                                                                        "NL-SfB versie": "BIM Loket december 2019"})

for ifc_covering in ifc_coverings:
    if ifc_covering.Name == 'isolatie':

        property_set  =  run("pset.add_pset", ifc_file, product=ifc_covering, name="4PS Propertyset")
        run("pset.edit_pset", ifc_file, pset=property_set, properties={ 
                                                                        "NL-SfB": "42.12",
                                                                        "NL-SfB omschrijving": "binnenwandafwerkingen; bekledingen",
                                                                        "NL-SfB versie": "BIM Loket december 2019"
                                                                        })


  
ifc_file.write(ifc_file_path)

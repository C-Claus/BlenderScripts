import bpy
import ifcopenshell
import ifcopenshell.api
from ifcopenshell.api import run
import blenderbim.bim.ifc
from blenderbim.bim.ifc import IfcStore
from collections import OrderedDict

ifc_file = ifcopenshell.open(IfcStore.path)
building_stories = ifc_file.by_type('IfcBuildingStorey')

level_global_ids        =  OrderedDict()
level_pset_ids          =  OrderedDict()
storey_codes_by_psetid  =  OrderedDict()
level_pset_list         =  ['171','297','374','439','504','616']
storey_codes_list       =  ['UG01','EG00','OG01', 'OG02','OG03','OG04']

for building_storey in building_stories:
    level_global_ids[building_storey.Name] = building_storey.GlobalId

for index, level_name in enumerate(level_global_ids.keys()):
    level_pset_id = level_pset_list[index]
    level_pset_ids[level_name] = level_pset_id

for index, pset_id in enumerate(level_pset_ids.values()):
    storey_code_id = storey_codes_list[index]
    storey_codes_by_psetid[pset_id] = storey_code_id
    
for building_storey in building_stories:             
    for level, pset_id in level_pset_ids.items():
        if level == building_storey.Name:
            storey_code_id = storey_codes_by_psetid[level_pset_ids[level]]
            property_set  =  run("pset.add_pset", ifc_file, product=building_storey, name="Spezifisch")
            run("pset.edit_pset", ifc_file, pset=property_set, properties={ "Pset ID": str(pset_id),
                                                                            "Geschosscode": str(storey_code_id)})
  
ifc_file.write(IfcStore.path)
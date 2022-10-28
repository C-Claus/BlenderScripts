import ifcopenshell.api
import pandas as pd

def get_wall_library(csv_library):
       
    library_data_frame = pd.read_csv(csv_library, ";")
    
    #for index, row in library_data_frame.iterrows():
        #print(row['IfcElement'])
    
    return library_data_frame
    

def create_ifcwalltype_library(ifc_element, ifc_element_type, element_name, ifc_material_layer_set, material_name,pset_common, is_external, load_bearing, fire_rating, width):
    ifcopenshell.api.post_listeners = {}

    ifc_file = ifcopenshell.api.run("project.create_file")
    project = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcProject", name="BlenderBIM Demo")
    library = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcProjectLibrary", name="BlenderBIM Demo Library")

    ifcopenshell.api.run( "project.assign_declaration", ifc_file, definition=library, relating_context=project)
    ifcopenshell.api.run("unit.assign_unit", ifc_file, length={"is_metric": True, "raw": "METERS"})

    material = ifcopenshell.api.run("material.add_material", ifc_file, name=material_name)

    element = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class=ifc_element_type, name=element_name)
    rel = ifcopenshell.api.run("material.assign_material", ifc_file, product=element, type="IfcMaterialLayerSet")

    layer_set = rel.RelatingMaterial
    layer = ifcopenshell.api.run("material.add_layer", ifc_file, layer_set=layer_set, material=material)
    layer.LayerThickness = 0.1


    pset = ifcopenshell.api.run("pset.add_pset", ifc_file, product=element, name="Pset_Name")

    ifcopenshell.api.run("pset.add_pset", ifc_file, product=element, name="Your Property Set Name")
    ifcopenshell.api.run("pset.edit_pset", ifc_file, pset=pset, properties={"foo": "foobar", "foo2": "foobaz"})

    ifcopenshell.api.run("project.assign_declaration", ifc_file, definition=element, relating_context=library)


    ifc_file.write("C:\\Users\\cclaus\\OneDrive - 4PS Group BV\\Bureaublad\\demo" + str(element_name) + ".ifc")


csv_wall_library = "C:\\Algemeen\\00_prive\\BlenderScripts\\BlenderBIMLibrary\\IfcWallLibrary.csv"
get_wall_library(csv_library=csv_wall_library)

for index, row in get_wall_library(csv_library=csv_wall_library).iterrows():
    print(row['IfcElement'])
    
    create_ifcwalltype_library( ifc_element=row['IfcElement'],
                                ifc_element_type=row['IfcElementType'],
                                element_name=row['Name'],
                                ifc_material_layer_set=row['IfcMaterialLayerSet'],
                                material_name=row['Material'],
                                pset_common=row['Pset_Common'],
                                is_external=row['IsExternal'],
                                load_bearing=row['LoadBearing'],
                                fire_rating=row['FireRating'],
                                width=row['Width'])
                                
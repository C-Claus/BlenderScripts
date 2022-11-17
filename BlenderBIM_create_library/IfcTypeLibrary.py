import ifcopenshell.api
import pandas as pd
import bpy

create_seperate_files = True 


def get_type_library(csv_library):
       
    library_data_frame = pd.read_csv(csv_library, ";")
    
    return library_data_frame
    

def create_ifctype_library(ifc_element, ifc_element_type, element_name, ifc_material_layer_set, material_name,layer_set_name,classification, item_reference,pset_common, is_external, load_bearing, fire_rating, width, rgb):
    
    ifcopenshell.api.post_listeners = {}

    ifc_file = ifcopenshell.api.run("project.create_file")
    project = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcProject", name="BlenderBIM Demo")
    library = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcProjectLibrary", name="BlenderBIM Demo Library")

    ifcopenshell.api.run( "project.assign_declaration", ifc_file, definition=library, relating_context=project)
    ifcopenshell.api.run("unit.assign_unit", ifc_file, length={"is_metric": True, "raw": "METERS"})

    
    #############################
    ### Add MaterialLayerSet ####
    #############################
    material = ifcopenshell.api.run("material.add_material", ifc_file, name=material_name)
    
    element = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class=ifc_element_type, name=element_name)
    rel = ifcopenshell.api.run("material.assign_material", ifc_file, product=element, type="IfcMaterialLayerSet")
    
    layer_set = rel.RelatingMaterial
    layer_set.LayerSetName = layer_set_name
    layer = ifcopenshell.api.run("material.add_layer", ifc_file, layer_set=layer_set, material=material)
    layer.LayerThickness = width/1000
   
    
    #######################
    ### Add PsetCommon ####
    #######################
    pset = ifcopenshell.api.run("pset.add_pset", ifc_file, product=element, name=pset_common)

    ifcopenshell.api.run("pset.add_pset", ifc_file, product=element, name=pset_common)
    ifcopenshell.api.run("pset.edit_pset", ifc_file, pset=pset, properties={"IsExternal": is_external, "LoadBearing": load_bearing, "FireRating":fire_rating})
    
    
    ##################
    ### Add style ####
    ################## 
    context = ifc_file.createIfcGeometricRepresentationContext()
    style = ifcopenshell.api.run("style.add_style", ifc_file, name=material_name)
    
    red = float(rgb.split(',')[0])
    green = float(rgb.split(',')[1])
    blue = float(rgb.split(',')[2])
    
   
    ifcopenshell.api.run(
        "style.add_surface_style",
        ifc_file,
        style=style,
        attributes={
            "SurfaceColour": {
                "Name": None,
                "Red": red,
                "Green": green,
                "Blue": blue,
            },
            "DiffuseColour": {
                "Name": None,
                "Red": red,
                "Green": green,
                "Blue": blue,
            },
            "Transparency": 0.0,
            "ReflectanceMethod": "PLASTIC",
        },
    )
    ifcopenshell.api.run(
        "style.assign_material_style",
        ifc_file,
        material=material,
        style=style,
        context=context,
    )
   
        
        
    result = ifcopenshell.api.run("classification.add_classification", ifc_file, classification='NLSfb')   
    
    ifcopenshell.api.run(
            "classification.add_reference",
            ifc_file,
            product=element,
            identification=str(item_reference),
            name=str(classification),
            classification=result,
        )


    ifcopenshell.api.run("project.assign_declaration", ifc_file, definition=element, relating_context=library)

    print (element_name)
    ifc_file.write("C:\\Algemeen\\00_prive\\BlenderScripts\\BlenderBIM_create_library\\IFC_type_library\\" + str(element_name) + ".ifc")


########################################################
### Call the methods which loop through the CSV file ###
########################################################
csv_type_library = "C:\\Algemeen\\00_prive\\BlenderScripts\\BlenderBIM_create_library\\binnenwanden_bibliotheek_met_hatch.csv"
get_type_library(csv_library=csv_type_library)

for index, row in get_type_library(csv_library=csv_type_library).iterrows():
    

    create_ifctype_library(        ifc_element=row['IfcElement'],
                                ifc_element_type=row['IfcElementType'],
                                element_name=row['Name'],
                                ifc_material_layer_set=row['IfcMaterialLayerSet'],
                                material_name=row['Material'],
                                layer_set_name=row['LayerSetName'],
                                classification=row['Classification'],
                                item_reference=row['ItemReference'],
                                pset_common=row['Pset_Common'],
                                is_external=row['IsExternal'],
                                load_bearing=row['LoadBearing'],
                                fire_rating=row['FireRating'],
                                width=row['Width'],
                                rgb=row['RGB'])
                        

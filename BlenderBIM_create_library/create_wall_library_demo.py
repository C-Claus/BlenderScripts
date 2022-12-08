#import bpy
import ifcopenshell.api
import pandas as pd
import numpy
import bpy

ifc_file = ifcopenshell.api.run("project.create_file")
project = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcProject", name="BlenderBIM Demo")

site = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcSite", name="My Site")
building = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcBuilding", name="wall_library")
storey = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcBuildingStorey", name="00_ground_floor")
ifcopenshell.api.run("unit.assign_unit", ifc_file, length={"is_metric": True, "raw": "METERS"})



model = ifcopenshell.api.run("context.add_context", ifc_file, context_type="Model")
plan = ifcopenshell.api.run("context.add_context", ifc_file, context_type="Plan")

representations = {
    "body": ifcopenshell.api.run(
        "context.add_context",
        ifc_file,
        context_type="Model",
        context_identifier="Body",
        target_view="MODEL_VIEW",
        parent=model,
    ),
    "annotation": ifcopenshell.api.run(
        "context.add_context",
        ifc_file,
        context_type="Plan",
        context_identifier="Annotation",
        target_view="PLAN_VIEW",
        parent=plan,
    ),
}


def get_type_library(csv_library):
       
    library_data_frame = pd.read_csv(csv_library, ";")
    
    return library_data_frame
    

def create_ifctype_library(ifc_element, ifc_element_type, element_name, ifc_material_layer_set, material_name,layer_set_name,classification, item_reference,pset_common, is_external, load_bearing, fire_rating, width, rgb):
    
    #ifcopenshell.api.post_listeners = {}

    
    #library = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcProjectLibrary", name="BlenderBIM Demo Library")

    #ifcopenshell.api.run( "project.assign_declaration", ifc_file, definition=library, relating_context=project)
    

    
    #############################
    ### Add MaterialLayerSet ####
    #############################
    material = ifcopenshell.api.run("material.add_material", ifc_file, name=material_name)
    
    element = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class=ifc_element_type, name=element_name)
    
    #element.GlobalId = ifcopenshell.guid.new()
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


    ifcopenshell.api.run("project.assign_declaration", ifc_file, definition=element, relating_context=project)
    
    
    occurrence = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class=ifc_element, name=element_name)
    
    print (occurrence)
    ifcopenshell.api.run("type.assign_type", ifc_file, related_object=occurrence, relating_type=element)

    #representation = ifcopenshell.api.run("geometry.add_profile_representation", ifc_file, context=representations["body"], profile=profile, depth=5)


    # A 4x4 matrix representing the location and rotation of the element, in the form:
    # [ [ x_x, y_x, z_x, x   ]
    #   [ x_y, y_y, z_y, y   ]
    #   [ x_z, y_z, z_z, z   ]
    #   [ 0.0, 0.0, 0.0, 1.0 ] ]
    # The position is given by the last column: (x, y, z)
    # The rotation is described by the first three columns, by explicitly specifying the local X, Y, Z axes.
    # The first column is a normalised vector of the local X axis: (x_x, x_y, x_z)
    # The second column is a normalised vector of the local Y axis: (y_x, y_y, y_z)
    # The third column is a normalised vector of the local Z axis: (z_x, z_y, z_z)
    # The axes follow a right-handed coordinate system.
    # Objects are never scaled, so the scale factor of the matrix is always 1.      
    matrix_1 = numpy.array(
                (
                    (0.0, 0.0, 1.0, 0.0),
                    (0.0, 1.0, 0.0, 0.0),
                    (1.0, 0.0, 0.0, 0.0),
                    (0.0, 0.0, 0.0, 1.0),
                )
            )
            
            
            
                   
    ifcopenshell.api.run("geometry.edit_object_placement",ifc_file, product=occurrence, matrix=matrix_1) 
    ifcopenshell.api.run("spatial.assign_container", ifc_file, relating_structure=storey, product=occurrence)

    #print (element_name)
ifc_file.write("C:\\Algemeen\\00_prive\\BlenderScripts\\BlenderBIM_create_library\\IFC_type_library\\demo_library.ifc")


########################################################
### Call the methods which loop through the CSV file ###
########################################################
csv_type_library = "C:\\Algemeen\\00_prive\\BlenderScripts\\BlenderBIM_create_library\\type_library.csv"
get_type_library(csv_library=csv_type_library)

for index, row in get_type_library(csv_library=csv_type_library).iterrows():
    
    print (index, row)
    
    
    create_ifctype_library(     ifc_element=row['IfcElement'],
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
  
    
                        
element_name="demo_library"
folder_path = "C:\\Algemeen\\00_prive\\BlenderScripts\\BlenderBIM_create_library\\IFC_type_library\\"
filename = str(element_name) + ".ifc"
file_path = (folder_path + filename)
ifc_file.write(file_path)


def load_ifc_automatically():

    if (bool(ifc_file)) == True:
        project = ifc_file.by_type('IfcProject')
        
        if project is not None:
            for i in project:
                collection_name = 'IfcProject/' + i.Name
                
            collection = bpy.data.collections.get(str(collection_name))
             
            if collection is not None:
                for obj in collection.objects:
                    bpy.data.objects.remove(obj, do_unlink=True)
                    
                bpy.data.collections.remove(collection)
                
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)         
        bpy.ops.bim.load_project(filepath=file_path)
               
load_ifc_automatically()

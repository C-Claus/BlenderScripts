import ifcopenshell
from ifcopenshell.api import run 
import numpy

ifc_file = ifcopenshell.file()
project = run("root.create_entity", ifc_file, ifc_class="IfcProject", name="Demo_Library")

run("unit.assign_unit", ifc_file)

context = run("context.add_context", ifc_file, context_type="Model")
body = run("context.add_context", ifc_file, context_type="Model", context_identifier="Body", target_view="MODEL_VIEW", parent=context)
site = run("root.create_entity", ifc_file, ifc_class="IfcSite", name="site_library")
building = run("root.create_entity", ifc_file, ifc_class="IfcBuilding", name="building")
storey = run("root.create_entity", ifc_file, ifc_class="IfcBuildingStorey", name="00_ground_floor")

model = ifcopenshell.api.run("context.add_context", ifc_file, context_type="Model")
plan = ifcopenshell.api.run("context.add_context", ifc_file, context_type="Plan")

run("aggregate.assign_object", ifc_file, relating_object=project, product=site)
run("aggregate.assign_object", ifc_file, relating_object=site, product=building)
run("aggregate.assign_object", ifc_file, relating_object=building, product=storey)


run( "project.assign_declaration", ifc_file, definition=project, relating_context=project)
run("unit.assign_unit", ifc_file, length={"is_metric": True, "raw": "METERS"})

def read_from_csv():
    print ('read from csv')

def create_wall():
    print ('create wall')
    ifc_material = run("material.add_material", ifc_file, name="brick")

    ifc_walltype = run("root.create_entity", ifc_file, ifc_class="IfcWallType", name="wall_demo")
    relating_material = run("material.assign_material", ifc_file, product=ifc_walltype, type="IfcMaterialLayerSet")
    layer_set = relating_material.RelatingMaterial
    layer = run("material.add_layer", ifc_file, layer_set=layer_set, material=ifc_material)
    layer.LayerThickness = 0.2
    #run("project.assign_declaration", ifc_file, definition=ifc_walltype, relating_context=project)
    
    ifc_walltype_instance = run("root.create_entity", ifc_file, ifc_class="IfcWall", relating_type=ifc_walltype)
    
    
    print(ifc_walltype_instance)
    
    
    #representation = run("geometry.add_wall_representation",ifc_file,context=body)
    
    representation = run("geometry.add_wall_representation",ifc_file,context=body,length=5,height=3,thickness=layer.LayerThickness,)
    
    
    matrix_1 = numpy.array(
            (
                (0.0, 0.0, 1.0, 0.0),
                (0.0, 1.0, 0.0, 0.0),
                (1.0, 0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0, 1.0),
            )
        )
        
    run("geometry.edit_object_placement",ifc_file,product=ifc_walltype_instance ,matrix=matrix_1,is_si=False)
    run("spatial.assign_container", ifc_file, relating_structure=storey, product=ifc_walltype_instance)
    #run("project.assign_declaration", ifc_file, definition=ifc_walltype_instance, relating_context=project)





    """  

    ifc_material = run("material.add_material", ifc_file, name="brick")
    ifc_wall = run("root.create_entity", ifc_file, ifc_class="IfcWallType", name="wall_name")
    relating_material = run("material.assign_material", ifc_file, product=ifc_wall, type="IfcMaterialLayerSet")

    layer_set = relating_material.RelatingMaterial
    layer_set.LayerSetName = "brick"

    layer = run("material.add_layer", ifc_file, layer_set=layer_set, material=ifc_material)
    layer.LayerThickness = 0.2
    layer.Material = ifc_material

    matrix_1 = numpy.array(
            (
                (0.0, 0.0, 1.0, 0.0),
                (0.0, 1.0, 0.0, 0.0),
                (1.0, 0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0, 1.0),
            )
        )

    occurrence = run("root.create_entity", ifc_file, ifc_class="IfcWall", name="wall_name")
    run("type.assign_type", ifc_file, related_object=occurrence, relating_type=ifc_wall)
    run("geometry.edit_object_placement", ifc_file, product=occurrence, matrix=matrix_1)
    run("spatial.assign_container", ifc_file, relating_structure=storey, product=occurrence)

    run("project.assign_declaration", ifc_file, definition=ifc_wall, relating_context=project)

    """


    

def create_beam():
    #create material
    #create ifcmaterialprofileset
    #assign material to profileset
    #create type
    #create occurence
    #place occurence
    #representation = run("geometry.add_profile_representation", ifc_file, context=representations["body"], profile=profile, depth=5)
    print ('create beam')


create_wall()

print (ifc_file)

folder_path = "C:\\Algemeen\\00_prive\\BlenderScripts\\BlenderBIM_create_objects\\ifc_library\\" 
filename = "place_ifcwalltype_instance.ifc"
file_path = (folder_path + filename)
print (file_path)
ifc_file.write(file_path)
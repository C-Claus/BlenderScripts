import bpy
import ifcopenshell
from ifcopenshell.api import run
import numpy

ifc_file = ifcopenshell.file()

project = run("root.create_entity", ifc_file, ifc_class="IfcProject", name="Demo")

run("unit.assign_unit", ifc_file, length={"is_metric": True, "raw": "METERS"})

context = run("context.add_context", ifc_file, context_type="Model")
body = run("context.add_context", ifc_file,context_type="Model", context_identifier="Body", target_view="MODEL_VIEW", parent=context)


# Create a site, building, and storey. Many hierarchies are possible.
site = run("root.create_entity", ifc_file, ifc_class="IfcSite", name="My Site")
building = run("root.create_entity", ifc_file, ifc_class="IfcBuilding", name="Building A")
storey = run("root.create_entity", ifc_file, ifc_class="IfcBuildingStorey", name="Ground Floor")

# Since the site is our top level location, assign it to the project
# Then place our building on the site, and our storey in the building
run("aggregate.assign_object", ifc_file, relating_object=project, product=site)
run("aggregate.assign_object", ifc_file, relating_object=site, product=building)
run("aggregate.assign_object", ifc_file, relating_object=building, product=storey)


ifc_material = run("material.add_material", ifc_file, name="brick")


style = run("style.add_style", ifc_file, name=ifc_material.Name)
run(
    "style.add_surface_style",
    ifc_file,
    style=style,
    attributes={
        "SurfaceColour": {
            "Name": ifc_material.Name,
            "Red": 0.8,
            "Green": 0.5,
            "Blue": 0.2,
        },
        "Transparency": 0,
        "ReflectanceMethod": "PLASTIC",
    },
)
run(
    "style.assign_material_style",
    ifc_file,
    material=ifc_material,
    style=style,
    context=context,
)

ifc_walltype = run("root.create_entity", ifc_file, ifc_class="IfcWallType", name="wall_demo")
relating_material = run("material.assign_material", ifc_file, product=ifc_walltype, type="IfcMaterialLayerSet")
layer_set = relating_material.RelatingMaterial
layer = run("material.add_layer", ifc_file, layer_set=layer_set, material=ifc_material)
layer.LayerThickness = 0.2


ifc_walltype_instance = run("root.create_entity", ifc_file, ifc_class="IfcWall")
run("type.assign_type", ifc_file, related_object=ifc_walltype_instance, relating_type=ifc_walltype)

representation = run("geometry.add_wall_representation",ifc_file,context=body,length=5,height=6,thickness=layer.LayerThickness)

matrix_1 = numpy.array(
            (
                (1.0, 0.0, 0.0, 0.0),
                (0.0, 1.0, 0.0, 0.0),
                (0.0, 0.0, 1.0, 0.0),
                (0.0, 0.0, 0.0, 1.0),
            )
        )
    
run("geometry.edit_object_placement",ifc_file,product=ifc_walltype_instance ,matrix=matrix_1,is_si=False)
run("spatial.assign_container", ifc_file, relating_structure=storey, product=ifc_walltype_instance)

run("geometry.assign_representation", ifc_file, product=ifc_walltype_instance, representation=representation)


folder_path = "C:\\Algemeen\\00_prive\\BlenderScripts\\BlenderBIM_create_objects\\ifc_library\\" 
filename = "place_ifcwalltype_instance_1.ifc"
file_path = (folder_path + filename)
print (file_path)
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
                
        for material in bpy.data.materials:
            material.user_clear()
            bpy.data.materials.remove(material)
        
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)         
        bpy.ops.bim.load_project(filepath=file_path)
               
load_ifc_automatically()

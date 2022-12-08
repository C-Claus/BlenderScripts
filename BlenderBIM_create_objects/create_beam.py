import bpy
import numpy
import ifcopenshell.api


ifc_file = ifcopenshell.api.run("project.create_file")
project = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcProject", name="BlenderBIM Demo")
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



site = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcSite", name="My Site")
building = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcBuilding", name="Building A")
storey = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcBuildingStorey", name="Ground Floor")

ifcopenshell.api.run("aggregate.assign_object", ifc_file, relating_object=project, product=site)
ifcopenshell.api.run("aggregate.assign_object", ifc_file, relating_object=site, product=building)
ifcopenshell.api.run("aggregate.assign_object", ifc_file, relating_object=building, product=storey)

element_name='simple_beam'
material = ifcopenshell.api.run("material.add_material", ifc_file, name='beam_material')
profile = ifc_file.create_entity("IfcRectangleProfileDef", ProfileType="AREA", XDim=0.9, YDim=0.5)

element = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class='IfcBeamType', name=element_name)
rel = ifcopenshell.api.run("material.assign_material", ifc_file, product=element, type="IfcMaterialProfileSet")
profile_set = rel.RelatingMaterial
material_profile = ifcopenshell.api.run( "material.add_profile", ifc_file, profile_set=profile_set, material=material)
ifcopenshell.api.run("material.assign_profile", ifc_file, material_profile=material_profile, profile=profile)

#or use:
#material_profile = ifcopenshell.api.run("material.add_profile", ifc_file, profile_set=profile_set, material=material, profile=profile)
profile.ProfileName = "square_profile"

occurrence = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcBeam", name=element_name, )
ifcopenshell.api.run("type.assign_type", ifc_file, related_object=occurrence, relating_type=element)

representation = ifcopenshell.api.run("geometry.add_profile_representation", ifc_file, context=representations["body"], profile=profile, depth=5)


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





context = ifc_file.createIfcGeometricRepresentationContext()
style = ifcopenshell.api.run("style.add_style", ifc_file, name="concrete")
ifcopenshell.api.run(
            "style.add_surface_style",
            ifc_file,
            style=style,
            attributes={
                "SurfaceColour": {
                    "Name": None,
                    "Red": 2.2,
                    "Green": 0.8,
                    "Blue": 0.5,
                },
                "DiffuseColour": {
                    "Name": None,
                    "Red": 2.2,
                    "Green": 0.8,
                    "Blue": 0.5,
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
        
 
 
        
ifcopenshell.api.run("geometry.assign_representation", ifc_file, product=occurrence, representation=representation)


######################################################################################
#########################  Write file and load into BlenderBIM #######################
######################################################################################
folder_path = "C:\\Algemeen\\00_prive\\BlenderScripts\\BlenderBIM_create_objects\\ifc_library\\" 
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
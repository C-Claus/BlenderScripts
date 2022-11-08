import ifcopenshell
from ifcopenshell.api import run

# Create a blank model
ifc_file = ifcopenshell.file()

# All projects must have one IFC Project element
project = run("root.create_entity", ifc_file, ifc_class="IfcProject", name="My Project")

# Geometry is optional in IFC, but because we want to use geometry in this example, let's define units
# Assigning without arguments defaults to metric units
run("unit.assign_unit", ifc_file)

# Let's create a modeling geometry context, so we can store 3D geometry (note: IFC supports 2D too!)
context = run("context.add_context", ifc_file, context_type="Model")
# In particular, in this example we want to store the 3D "body" geometry of objects, i.e. the body shape
body = run(
    "context.add_context", ifc_file,
    context_type="Model", context_identifier="Body", target_view="MODEL_VIEW", parent=context
)

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


# Create a site, building, and storey. Many hierarchies are possible.
site = run("root.create_entity", ifc_file, ifc_class="IfcSite", name="My Site")
building = run("root.create_entity", ifc_file, ifc_class="IfcBuilding", name="Building A")
storey = run("root.create_entity", ifc_file, ifc_class="IfcBuildingStorey", name="Ground Floor")

# Since the site is our top level location, assign it to the project
# Then place our building on the site, and our storey in the building
run("aggregate.assign_object", ifc_file, relating_object=project, product=site)
run("aggregate.assign_object", ifc_file, relating_object=site, product=building)
run("aggregate.assign_object", ifc_file, relating_object=building, product=storey)



element_name='my_beam'
element = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class='IfcBeamType', name=element_name)
material = ifcopenshell.api.run("material.add_material", ifc_file, name='beam_material')
profile = ifc_file.create_entity("IfcRectangleProfileDef", ProfileType="AREA", XDim=0.5, YDim=0.6)
rel = ifcopenshell.api.run("material.assign_material", ifc_file, product=element, type="IfcMaterialProfileSet")
profile_set = rel.RelatingMaterial
material_profile = ifcopenshell.api.run( "material.add_profile", ifc_file, profile_set=profile_set, material=material)
ifcopenshell.api.run("material.assign_profile", ifc_file, material_profile=material_profile, profile=profile)

occurrence = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcBeam", name=element_name)
ifcopenshell.api.run("type.assign_type", ifc_file, related_object=occurrence, relating_type=element)

representation = ifcopenshell.api.run("geometry.add_profile_representation", ifc_file, context=representations["body"], profile=profile, depth=3)


ifcopenshell.api.run("spatial.assign_container", ifc_file, relating_structure=storey, product=occurrence)
ifcopenshell.api.run("geometry.assign_representation", ifc_file, product=occurrence, representation=representation)








# Let's create a new wall
wall = run("root.create_entity", ifc_file, ifc_class="IfcWall")
# Add a new wall-like body geometry, 5 meters long, 3 meters high, and 200mm thick
representation = run("geometry.add_wall_representation", ifc_file, context=body, length=5, height=3, thickness=0.2)
# Assign our new body geometry back to our wall
run("geometry.assign_representation", ifc_file, product=wall, representation=representation)

# Place our wall in the ground floor
run("spatial.assign_container", ifc_file, relating_structure=storey, product=wall)

# Write out to a file
ifc_file.write("C:\\Algemeen\\00_prive\\BlenderScripts\\BlenderBIM_create_objects\\ifc_library\\simple_wall.ifc")
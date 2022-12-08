import ifcopenshell.api

ifcopenshell.api.post_listeners = {}

ifc_file = ifcopenshell.api.run("project.create_file")
project = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcProject", name="BlenderBIM Demo")
#library = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcProjectLibrary", name="BlenderBIM Demo Library")
ifcopenshell.api.run( "project.assign_declaration", ifc_file, definition=project, relating_context=project)
ifcopenshell.api.run("unit.assign_unit", ifc_file, length={"is_metric": True, "raw": "METERS"})

material = ifcopenshell.api.run("material.add_material", ifc_file, name="Material Name")
element = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class='IfcWallType', name='demo_wall')
rel = ifcopenshell.api.run("material.assign_material", ifc_file, product=element, type="IfcMaterialLayerSet")

layer_set = rel.RelatingMaterial
layer = ifcopenshell.api.run("material.add_layer", ifc_file, layer_set=layer_set, material=material)
layer.LayerThickness = 0.1

ifcopenshell.api.run("project.assign_declaration", ifc_file, definition=element, relating_context=project)

ifc_file.write("C:\\Algemeen\\00_prive\\BlenderScripts\\BlenderBIM_create_objects\\ifc_library\\simple_wall.ifc")
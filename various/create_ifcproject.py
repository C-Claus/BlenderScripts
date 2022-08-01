import bpy


bpy.context.scene.BIMProjectProperties.template_file = 'IFC4 Demo Library.ifc'

bpy.ops.bim.select_library_file(filepath="C:\\Users\\cclaus\\AppData\\Roaming\\Blender Foundation\\Blender\\3.1\\scripts\\addons\\blenderbim\\bim\\data\\libraries\\IFC4 Demo Library.ifc")




bpy.ops.bim.create_project()

bpy.ops.bim.append_library_element(definition=20)
bpy.ops.bim.append_library_element(definition=25)
bpy.ops.bim.append_library_element(definition=29)
bpy.ops.bim.append_library_element(definition=33)
bpy.ops.bim.append_library_element(definition=37)
bpy.ops.bim.append_library_element(definition=41)
bpy.ops.bim.append_library_element(definition=47)
bpy.ops.bim.append_library_element(definition=53)
bpy.ops.bim.append_library_element(definition=58)
bpy.ops.bim.append_library_element(definition=62)
bpy.ops.bim.append_library_element(definition=66)
bpy.ops.bim.append_library_element(definition=71)
bpy.ops.bim.append_library_element(definition=76)
bpy.ops.bim.append_library_element(definition=81)
bpy.ops.bim.append_library_element(definition=86)
bpy.ops.bim.append_library_element(definition=91)
bpy.ops.bim.append_library_element(definition=95)
bpy.ops.bim.append_library_element(definition=159)
bpy.ops.bim.append_library_element(definition=225)

bpy.ops.export_ifc.bim(filepath="C:\\Algemeen\\07_prive\\08_ifc_bestanden\\create_demo.ifc", should_save_as=False)

bpy.context.scene.BIMModelProperties.ifc_class = 'IfcWallType'

bpy.ops.bim.add_type_instance()

bpy.ops.bim.dynamically_void_product(obj="IfcWall/Wall")

""" 
for i in range(1, 10):
    bpy.ops.bim.create_project()


    bpy.ops.bim.assign_class(obj="Grid", ifc_class="IfcGrid")

    bpy.ops.mesh.add_grid()
    bpy.ops.export_ifc.bim(filepath="C:\\Algemeen\\07_prive\\08_ifc_bestanden\\program" + str(i) + ".ifc", should_save_as=False)
"""
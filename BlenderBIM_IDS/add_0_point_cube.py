import bpy
import ifcopenshell.api
from ifcopenshell.api import run

from blenderbim.bim.ifc import IfcStore

ifc = IfcStore.path

ifc_file = ifcopenshell.open(ifc)
ifc_buildingelementproxies = ifc_file.by_type('IfcBuildingElementProxy')
# Clear existing objects
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

bpy.ops.mesh.primitive_cube_add(size=1.0,
                                enter_editmode=False,
                                align='WORLD',
                                location=(0, 0, 0))
                                

cube = bpy.context.active_object
cube.scale = (1, 1, 1)  
cube.location = (-0.5, -0.5, 0.5)
cube.name = '0-point'

#bpy.context.space_data.context = 'SCENE'
#bpy.context.space_data.context = 'OBJECT'

#bpy.context.scene.BIMRootProperties.ifc_class = 'IfcBuildingElementProxy'

bpy.ops.bim.assign_class(ifc_class="IfcBuildingElementProxy",
                         predefined_type="COMPLEX",
                         userdefined_type="")
                         
propertyset_name = '0_point_properties'   
for ifc_buildingelementproxy in (ifc_buildingelementproxies):
    print (ifc_buildingelementproxy)
                        
    pset    =   run("pset.add_pset",
                    ifc_file,
                    product=ifc_buildingelementproxy,
                    name=propertyset_name)
                    
    print (pset)
                    
    run("pset.edit_pset",
        ifc_file,
        pset=pset,
        properties={ "0_point": "0,0,0",
                     "psetid": "my_id" })
#add cube mesh
#assign ifc class to that mesh
#give ifc class specific properties
#when running script again it should check for that specific properties

IfcStore.file
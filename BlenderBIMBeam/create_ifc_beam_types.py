import math
import uuid
import time
import tempfile
import ifcopenshell
from collections import OrderedDict
 
import bpy

O = 0., 0., 0.
X = 1., 0., 0.
Y = 0., 1., 0.
Z = 0., 0., 1.

# Creates an IfcAxis2Placement3D from Location, Axis and RefDirection specified as Python tuples
def create_ifcaxis2placement(ifcfile, point=O, dir1=Z, dir2=X):
    point = ifcfile.createIfcCartesianPoint(point)
    dir1 = ifcfile.createIfcDirection(dir1)
    dir2 = ifcfile.createIfcDirection(dir2)
    axis2placement = ifcfile.createIfcAxis2Placement3D(point, dir1, dir2)
    return axis2placement

# Creates an IfcLocalPlacement from Location, Axis and RefDirection, specified as Python tuples, and relative placement
def create_ifclocalplacement(ifcfile, point=O, dir1=Z, dir2=X, relative_to=None):
    axis2placement = create_ifcaxis2placement(ifcfile,point,dir1,dir2)
    ifclocalplacement2 = ifcfile.createIfcLocalPlacement(relative_to,axis2placement)
    return ifclocalplacement2

create_guid = lambda: ifcopenshell.guid.compress(uuid.uuid1().hex)

ifcfile = ifcopenshell.file()

organisation = ifcfile.createIfcOrganization()
organisation.Name = "OS Arch Community"

app = ifcfile.createIfcApplication()
app.ApplicationDeveloper = organisation
app.Version = "0.7"
app.ApplicationFullName = "IfcOpenShell v0.7.0-1b1fd1e6"

person = ifcfile.createIfcPerson()
person.FamilyName="C. Claus"

organisation_person = ifcfile.createIfcPersonAndOrganization()
organisation_person.ThePerson = person
organisation_person.TheOrganization = organisation


owner_history= ifcfile.createIfcOwnerHistory()
owner_history.OwningUser = organisation_person
owner_history.OwningApplication = app
owner_history.ChangeAction= "NOCHANGE"
owner_history.CreationDate= int(time.time())

#  Global unit definitions
LengthUnit = ifcfile.createIfcSIUnit()
LengthUnit.UnitType = "LENGTHUNIT"
LengthUnit.Prefix = "MILLI"
LengthUnit.Name="METRE"

#AreaUnit = ifc_file.createIfcSIUnit("AREAUNIT" , None, "SQUARE_METRE")
AreaUnit = ifcfile.createIfcSIUnit()
AreaUnit.UnitType = "AREAUNIT"
AreaUnit.Name="SQUARE_METRE"


VolumeUnit = ifcfile.createIfcSIUnit()
VolumeUnit.UnitType = "VOLUMEUNIT"
VolumeUnit.Name="CUBIC_METRE"


PlaneAngleUnit = ifcfile.createIfcSIUnit()
PlaneAngleUnit.UnitType = "PLANEANGLEUNIT"
PlaneAngleUnit.Name  ="RADIAN"

AngleUnit = ifcfile.createIfcMeasureWithUnit()
AngleUnit.UnitComponent =PlaneAngleUnit 
AngleUnit.ValueComponent = ifcfile.createIfcPlaneAngleMeasure(math.pi/180)

DimExp = ifcfile.createIfcDimensionalExponents(0,0,0,0,0,0,0)

ConvertBaseUnit = ifcfile.createIfcConversionBasedUnit()
ConvertBaseUnit.Dimensions = DimExp
ConvertBaseUnit.UnitType="PLANEANGLEUNIT"
ConvertBaseUnit.Name="DEGREE"
ConvertBaseUnit.ConversionFactor = AngleUnit

UnitAssignment=ifcfile.createIfcUnitAssignment([LengthUnit , AreaUnit , VolumeUnit ,ConvertBaseUnit])

axis_X = ifcfile.createIfcDirection(X)
axis_Y = ifcfile.createIfcDirection(Y)
axis_Z = ifcfile.createIfcDirection(Z)
Pnt_O = ifcfile.createIfcCartesianPoint(O)

WorldCoordinateSystem = ifcfile.createIfcAxis2Placement3D()
WorldCoordinateSystem.Location=Pnt_O
WorldCoordinateSystem.Axis = axis_Z
WorldCoordinateSystem.RefDirection = axis_X

context = ifcfile.createIfcGeometricRepresentationContext()
context.ContextType = "Model"
context.CoordinateSpaceDimension = 3
context.Precision = 1.e-05
context.WorldCoordinateSystem = WorldCoordinateSystem


footprint_context = ifcfile.createIfcGeometricRepresentationSubContext()
footprint_context.ContextIdentifier = 'Footprint'
footprint_context.ContextType = "Model"
footprint_context.ParentContext = context
footprint_context.TargetView = 'MODEL_VIEW'

project = ifcfile.createIfcProject(create_guid())
project.OwnerHistory = owner_history
project.Name = "OSArch project"
project.RepresentationContexts = [context]
project.UnitsInContext = UnitAssignment

site_placement = create_ifclocalplacement(ifcfile)
site = ifcfile.createIfcSite(create_guid(), owner_history, "site", None, None, site_placement, None, None, "ELEMENT", None, None, None, None, None)

building_placement = create_ifclocalplacement(ifcfile, relative_to=site_placement)
building = ifcfile.createIfcBuilding(create_guid(), owner_history, 'osarch_building', None, None, building_placement, None, None, "ELEMENT", None, None, None)

storey_placement = create_ifclocalplacement(ifcfile, relative_to=building_placement)



building_storey = ifcfile.createIfcBuildingStorey(  create_guid(),
                                                    owner_history,
                                                    'building_storey',
                                                    None,
                                                    None, 
                                                    storey_placement,
                                                    None,
                                                    None,
                                                    "ELEMENT",
                                                    3000)
container_storey = ifcfile.createIfcRelAggregates(create_guid(), owner_history, "Building Container", None, building, [building_storey])

    
container_site = ifcfile.createIfcRelAggregates(create_guid(), owner_history, "Site Container", None, site, [building])
container_project = ifcfile.createIfcRelAggregates(create_guid(), owner_history, "Project Container", None, project, [site])


def create_ifcbeamtype():
    print ('create ifcbeamtype')
    
    x1 = 0
    y1 = -2
    
    
    ifc_beam = ifcopenshell.api.run("root.create_entity", ifcfile, ifc_class="IfcBeam", name="test")
    ifc_beam_type = ifcopenshell.api.run("root.create_entity", ifcfile, ifc_class="IfcBeamType")
    ifcopenshell.api.run("type.assign_type", ifcfile, related_object=ifc_beam, relating_type=ifc_beam_type)
    
    pnt1 = ifcfile.createIfcCartesianPoint( (x1,y1,z) )
    pnt2 = ifcfile.createIfcCartesianPoint( (x2,y2,z) )
    pnt3 = ifcfile.createIfcCartesianPoint( (x3,y3,z) )
    pnt4 = ifcfile.createIfcCartesianPoint( (x4,y4,z) )
    pnt5 = ifcfile.createIfcCartesianPoint( (x5,y5,z) ) 
    pnt6 = ifcfile.createIfcCartesianPoint( (x6,y6,z) ) 
    pnt7 = ifcfile.createIfcCartesianPoint( (x7,y7,z) ) 
    pnt8 = ifcfile.createIfcCartesianPoint( (x8,y8,z) ) 
   
    wall_line_x 	 = ifcfile.createIfcPolyline([pnt1,pnt2,pnt3,pnt4])
    wall_line_y      = ifcfile.createIfcPolyline([pnt5,pnt6,pnt7,pnt8])
    
    ifcclosedprofile_x = ifcfile.createIfcArbitraryClosedProfileDef("AREA", None, wall_line_x) 
    ifcclosedprofile_y = ifcfile.createIfcArbitraryClosedProfileDef("AREA", None, wall_line_y) 
    ifc_direction    = ifcfile.createIfcDirection(Z)
    
    point = ifcfile.createIfcCartesianPoint((0.0,0.0,0.0))
    dir1 = ifcfile.createIfcDirection((0., 0., 1.))
    dir2 = ifcfile.createIfcDirection((1., 0., 0.))
    
    axis2placement = ifcfile.createIfcAxis2Placement3D(point, dir1, dir2)
    wall_solid_x = ifcfile.createIfcExtrudedAreaSolid(ifcclosedprofile_x,  axis2placement, ifc_direction, 200)
    wall_solid_y = ifcfile.createIfcExtrudedAreaSolid(ifcclosedprofile_y,  axis2placement, ifc_direction, 200)
    
    shape_representation 	= ifcfile.createIfcShapeRepresentation( ContextOfItems=context,
                                                                RepresentationIdentifier='Body', 
                                                                RepresentationType='SweptSolid',
                                                                Items=[wall_solid_x, wall_solid_y])
                                                                
    ifcopenshell.api.run("geometry.assign_representation", ifcfile, product=ifc_beam_type, representation=shape_representation)
    ifcopenshell.api.run("spatial.assign_container", ifcfile, product=ifc_beam, relating_structure=building_storey_list[0])
    
    
    
#create_ifcbeamtype()

filename                    = "demo_beams.ifc"
folder_path                 = "C:\\Algemeen\\07_prive\\08_ifc_bestanden\\"


file_path = (folder_path + filename)
ifcfile.write(file_path)

def load_ifc_automatically():

    if (bool(ifcfile)) == True:
        project = ifcfile.by_type('IfcProject')
        
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













"""

file_path = "C:\\Algemeen\\00_prive\\08_ifc_bestanden\\beam_types.ifc"



bpy.ops.bim.create_project()
bpy.ops.export_ifc.bim(filepath=file_path, should_save_as=True)


def create_beam():
    
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

    bpy.ops.bim.assign_class(ifc_class="IfcBeamType", predefined_type="BEAM", userdefined_type="")


    
    
    #bpy.context.object.BIMObjectMaterialProperties.material_type = 'IfcMaterialProfileSet'
    
    
    
    #bpy.ops.bim.enable_editing_material_set_item(obj="IfcBeamType/Empty", material_set_item=66)
    #bpy.ops.bim.assign_parameterized_profile(ifc_class="IfcRectangleProfileDef", material_profile=66)
    #bpy.context.object.BIMObjectMaterialProperties.material_set_item_profile_attributes[2].float_value = 0.2
    #bpy.context.object.BIMObjectMaterialProperties.material_set_item_profile_attributes[3].float_value = 0.2
    #bpy.ops.bim.edit_material_set_item(material_set_item=66)









def create_material(material_name):
    
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    #bpy.ops.material.new()
    #bpy.data.materials.new(name="MaterialName")
    #bpy.context.object.active_material.name = "wood"

    #bpy.context.object.active_material.diffuse_color = (0.8, 0.448207, 0.0270887, 1)


    #bpy.ops.bim.add_material(obj="wood")

    #bpy.ops.bim.add_style()A
    
    activeObject = bpy.context.active_object #Set active object to variable
    mat = bpy.data.materials.new(name=material_name) #set new material to variable
    activeObject.data.materials.append(mat) #add the material to the object
    #bpy.context.object.active_material.diffuse_color = (1, 0, 0) #change color
    
    bpy.ops.bim.add_material(obj=material_name)
    
    





create_material(material_name="steel")

create_beam()





#add material
#bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
#bpy.ops.material.new()


#bpy.context.object.active_material.name = "wood"

#bpy.context.object.active_material.diffuse_color = (0.8, 0.448207, 0.0270887, 1)


#bpy.ops.bim.add_material(obj="wood")

#bpy.ops.bim.add_style()




ifcfile = ifcopenshell.open(file_path)


def load_ifc_automatically():

    if (bool(ifcfile)) == True:
        project = ifcfile.by_type('IfcProject')
        ifc_types = ifcfile.by_type('IfcElementType')
        
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

"""
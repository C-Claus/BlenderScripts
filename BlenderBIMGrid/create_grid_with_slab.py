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


filename = "demo.ifc"
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


# Defining project and representation contexts 
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


# IFC hierarchy creation
site_placement = create_ifclocalplacement(ifcfile)
site = ifcfile.createIfcSite(create_guid(), owner_history, "site", None, None, site_placement, None, None, "ELEMENT", None, None, None, None, None)

building_placement = create_ifclocalplacement(ifcfile, relative_to=site_placement)
building = ifcfile.createIfcBuilding(create_guid(), owner_history, 'osarch_building', None, None, building_placement, None, None, "ELEMENT", None, None, None)

storey_placement = create_ifclocalplacement(ifcfile, relative_to=building_placement)
elevation = 0.0
building_storey = ifcfile.createIfcBuildingStorey(create_guid(), owner_history, '00_ground_floor', None, None, storey_placement, None, None, "ELEMENT", elevation)

container_storey = ifcfile.createIfcRelAggregates(create_guid(), owner_history, "Building Container", None, building, [building_storey])
container_site = ifcfile.createIfcRelAggregates(create_guid(), owner_history, "Site Container", None, site, [building])
container_project = ifcfile.createIfcRelAggregates(create_guid(), owner_history, "Project Container", None, project, [site])


def create_grid(grids_x_distance_between, grids_y_distance_between, grids_x_direction_amount, grids_y_direction_amount, overlap):
    
    grids_x_direction_amount
    grids_y_direction_amount
    
    grids_x_dictionary = OrderedDict()
    grids_y_dictionary = OrderedDict()
 
    x = -grids_x_distance_between
    y = -grids_y_distance_between

    for x_grids in range(1, int(grids_x_direction_amount), 1):
        x += grids_x_distance_between 
        grids_x_dictionary[x_grids] = x
        
    for y_grids in range(1, int(grids_y_direction_amount), 1):
        y += grids_y_distance_between 
        grids_y_dictionary[y_grids] = y
             
    x_min = list(grids_x_dictionary.items())[0][1]
    x_max = list(grids_x_dictionary.items())[-1][1]
    
    y_min = list(grids_y_dictionary.items())[0][1]
    y_max = list(grids_y_dictionary.items())[-1][1]
    
    x_min_overlap = x_min-overlap
    x_max_overlap = x_max+overlap
    
    y_min_overlap = y_min-overlap
    y_max_overlap = y_max+overlap
    
    polylineSet = []
    gridX = []
    gridY = []
    
    for i_grid in grids_x_dictionary.items():
        
        point_1 = ifcfile.createIfcCartesianPoint((i_grid[1],y_min_overlap))
        point_2 = ifcfile.createIfcCartesianPoint((i_grid[1],y_max_overlap))
        
        Line = ifcfile.createIfcPolyline( [point_1 , point_2] )
        polylineSet.append(Line)
        
        grid = ifcfile.createIfcGridAxis()
        grid.AxisTag = str(i_grid[0]) + "X"
        grid.AxisCurve = Line
        grid.SameSense = True
        gridX.append(grid)
        
    for i_grid in grids_y_dictionary.items():
        
        point_1 = ifcfile.createIfcCartesianPoint((x_min_overlap,i_grid[1]))
        point_2 = ifcfile.createIfcCartesianPoint((x_max_overlap,i_grid[1]))
        
        Line = ifcfile.createIfcPolyline( [point_1 , point_2] )
        polylineSet.append(Line)
        
        grid = ifcfile.createIfcGridAxis()
        grid.AxisTag = str(i_grid[0]) + "Y"
        grid.AxisCurve = Line
        grid.SameSense = True
        gridY.append(grid)
        
      
    # Defining the grid 
    PntGrid = ifcfile.createIfcCartesianPoint( O )

    myGridCoordinateSystem = ifcfile.createIfcAxis2Placement3D()
    myGridCoordinateSystem.Location= PntGrid
    myGridCoordinateSystem.Axis = axis_Z
    myGridCoordinateSystem.RefDirection = axis_X

    grid_placement = ifcfile.createIfcLocalPlacement()
    grid_placement.PlacementRelTo = storey_placement
    grid_placement.RelativePlacement = myGridCoordinateSystem

    grid_curvedSet =  ifcfile.createIfcGeometricCurveSet(polylineSet)

    gridShape_Reppresentation = ifcfile.createIfcShapeRepresentation()
    gridShape_Reppresentation.ContextOfItems = footprint_context
    gridShape_Reppresentation.RepresentationIdentifier = 'FootPrint'
    gridShape_Reppresentation.RepresentationType = 'GeometricCurveSet'
    gridShape_Reppresentation.Items = [grid_curvedSet]

    grid_Representation = ifcfile.createIfcProductDefinitionShape()
    grid_Representation.Representations  = [gridShape_Reppresentation]

    myGrid = ifcfile.createIfcGrid(create_guid() , owner_history)
    myGrid.ObjectPlacement = grid_placement
    myGrid.Representation = grid_Representation
    myGrid.UAxes=gridX
    myGrid.VAxes=gridY

     
    container_SpatialStructure= ifcfile.createIfcRelContainedInSpatialStructure(create_guid() , owner_history)
    container_SpatialStructure.Name='BuildingStoreyContainer'
    container_SpatialStructure.Description = 'BuildingStoreyContainer for Elements'
    container_SpatialStructure.RelatingStructure = site
    container_SpatialStructure.RelatedElements = [myGrid]
    


def create_slab(slab_length_x, slab_length_y, slab_thickness):
    
    ifc_slab 	= ifcopenshell.api.run("root.create_entity", ifcfile, ifc_class="IfcSlab",name="slab_grid")
    ifc_slabtype= ifcopenshell.api.run("root.create_entity", ifcfile, ifc_class="IfcSlabType")
    ifcopenshell.api.run("type.assign_type", ifcfile, related_object=ifc_slab, relating_type=ifc_slabtype)
    
    pnt1 = ifcfile.createIfcCartesianPoint( (0.0,0.0,0.0) )
    pnt2 = ifcfile.createIfcCartesianPoint( (0.0,slab_length_y,0.0) )
    pnt3 = ifcfile.createIfcCartesianPoint( (slab_length_x,slab_length_y,0.0) )
    pnt4 = ifcfile.createIfcCartesianPoint( (slab_length_x,0.0,0.0) )
  
  
    slab_line 	= ifcfile.createIfcPolyline([pnt1,pnt2,pnt3,pnt4])
    ifcclosedprofile = ifcfile.createIfcArbitraryClosedProfileDef("AREA", None, slab_line)
    
    ifcdir = ifcfile.createIfcDirection(Z)
    
    point = ifcfile.createIfcCartesianPoint((0.0,0.0,0.0))
    dir1 = ifcfile.createIfcDirection((0., 0., 1.))
    dir2 = ifcfile.createIfcDirection((1., 0., 0.))
    axis2placement = ifcfile.createIfcAxis2Placement3D(point, dir1, dir2)

    
    extrusion = 100.0
    slab_solid = ifcfile.createIfcExtrudedAreaSolid(ifcclosedprofile,  axis2placement, ifcdir, extrusion)
    shape_representation 	= ifcfile.createIfcShapeRepresentation( ContextOfItems=context,
                                                        RepresentationIdentifier='Body', 
                                                        RepresentationType='SweptSolid',
                                                        Items=[slab_solid])
                                                        
    ifcopenshell.api.run("geometry.assign_representation", ifcfile, product=ifc_slabtype, representation=shape_representation)
    rel = ifcopenshell.api.run("spatial.assign_container", ifcfile, product=ifc_slab, relating_structure=building_storey) 

        
    
grids_x_direction_amount = 5.0
grids_y_direction_amount = 7.0 
grids_x_distance_between = 1000.0
grids_y_distance_between = 1000.0 
overlap                  = 1000.0   
  
slab_length_x = grids_x_direction_amount*grids_x_distance_between - 2*grids_x_distance_between 
slab_length_y = grids_y_direction_amount*grids_y_distance_between - 2*grids_y_distance_between 
slab_thickness =  100.0  
 
create_grid(grids_x_distance_between,
            grids_y_distance_between,
            grids_x_direction_amount,
            grids_y_direction_amount,
            overlap
            )
            
create_slab(slab_length_x,
            slab_length_y,
            slab_thickness )
            

 
file_path = ("C:\\Algemeen\\07_prive\\08_ifc_bestanden\\" + filename)
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
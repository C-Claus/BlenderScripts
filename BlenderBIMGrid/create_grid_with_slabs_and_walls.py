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
building_storey_list = []

def create_building_storeys(building_storeys_amount, elevation, building_storey_height):
    
    for i in range(0, building_storeys_amount):
    
        elevation += building_storey_height
        building_storey = ifcfile.createIfcBuildingStorey(  create_guid(),
                                                            owner_history,
                                                            '0' + str(i) + '_building_storey',
                                                            None,
                                                            None, 
                                                            storey_placement,
                                                            None,
                                                            None,
                                                            "ELEMENT",
                                                            float(elevation)-float(building_storey_height))
        container_storey = ifcfile.createIfcRelAggregates(create_guid(), owner_history, "Building Container", None, building, [building_storey])
        building_storey_list.append(building_storey)
    
container_site = ifcfile.createIfcRelAggregates(create_guid(), owner_history, "Site Container", None, site, [building])
container_project = ifcfile.createIfcRelAggregates(create_guid(), owner_history, "Project Container", None, project, [site])



def create_grid(grids_x_distance_between, grids_y_distance_between, grids_x_direction_amount, grids_y_direction_amount, grid_extends):

    grids_x_dictionary = OrderedDict()
    grids_y_dictionary = OrderedDict()
 
    x = -float(grids_x_distance_between)
    y = -float(grids_y_distance_between)

    for x_grids in range(0, int(grids_x_direction_amount), 1):
        x += float(grids_x_distance_between)
        grids_x_dictionary[x_grids] = x
        
    for y_grids in range(0, int(grids_y_direction_amount), 1):
        y += grids_y_distance_between 
        grids_y_dictionary[y_grids] = y
             
    x_min = list(grids_x_dictionary.items())[0][1]
    x_max = list(grids_x_dictionary.items())[-1][1]
    
    y_min = list(grids_y_dictionary.items())[0][1]
    y_max = list(grids_y_dictionary.items())[-1][1]
    
    x_min_overlap = x_min-grid_extends
    x_max_overlap = x_max+grid_extends
    
    y_min_overlap = y_min-grid_extends
    y_max_overlap = y_max+grid_extends
    
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
    

def create_slab(length_x, length_y, slab_thickness):
     
    for building_storey in building_storey_list: 
    
        elevation = (building_storey.Elevation)
        
        ifc_slab 	= ifcopenshell.api.run("root.create_entity", ifcfile, ifc_class="IfcSlab", name="slab_which_follows_grid" )
        ifc_slabtype= ifcopenshell.api.run("root.create_entity", ifcfile, ifc_class="IfcSlabType")
        ifcopenshell.api.run("type.assign_type", ifcfile, related_object=ifc_slab, relating_type=ifc_slabtype)
        
        pnt1 = ifcfile.createIfcCartesianPoint( (0.0,0.0,float(elevation)) )
        pnt2 = ifcfile.createIfcCartesianPoint( (0.0,length_y,float(elevation)) )
        pnt3 = ifcfile.createIfcCartesianPoint( (length_x,length_y,float(elevation)) )
        pnt4 = ifcfile.createIfcCartesianPoint( (length_x,0.0,float(elevation)) )
      
      
        slab_line 	= ifcfile.createIfcPolyline([pnt1,pnt2,pnt3,pnt4])
        ifcclosedprofile = ifcfile.createIfcArbitraryClosedProfileDef("AREA", None, slab_line)
        ifc_direction = ifcfile.createIfcDirection(Z)
        
        point = ifcfile.createIfcCartesianPoint((0.0,0.0,0.0))
        dir1 = ifcfile.createIfcDirection((0., 0., 1.))
        dir2 = ifcfile.createIfcDirection((1., 0., 0.))
        axis2placement = ifcfile.createIfcAxis2Placement3D(point, dir1, dir2)
        
        extrusion = slab_thickness
        slab_solid = ifcfile.createIfcExtrudedAreaSolid(ifcclosedprofile,  axis2placement, ifc_direction, extrusion)
        shape_representation 	= ifcfile.createIfcShapeRepresentation( ContextOfItems=context,
                                                                        RepresentationIdentifier='Body', 
                                                                        RepresentationType='SweptSolid',
                                                                        Items=[slab_solid])
                                                                        
        ifcopenshell.api.run("geometry.assign_representation", ifcfile, product=ifc_slabtype, representation=shape_representation)
        ifcopenshell.api.run("spatial.assign_container", ifcfile, product=ifc_slab, relating_structure=building_storey) 
    
    
def create_wall_interior(length_x, length_y, wall_interior_thickness, slab_thickness, building_storey_height):
    print ("create wall")  
    
    extrusion=(building_storey_height-slab_thickness)
    
    for building_storey in building_storey_list: 
    
        elevation = (building_storey.Elevation)
        
        ifc_wall 	= ifcopenshell.api.run("root.create_entity", ifcfile, ifc_class="IfcWall", name="wall_interior_which_follows_grid" )
        ifc_walltype= ifcopenshell.api.run("root.create_entity", ifcfile, ifc_class="IfcWallType")
        ifcopenshell.api.run("type.assign_type", ifcfile, related_object=ifc_wall, relating_type=ifc_walltype) 
        
        
        pnt1 = ifcfile.createIfcCartesianPoint( (0.0,0.0,float(elevation)+slab_thickness) )
        pnt2 = ifcfile.createIfcCartesianPoint( (0.0,wall_interior_thickness,float(elevation)+slab_thickness) )
        pnt3 = ifcfile.createIfcCartesianPoint( (length_x,wall_interior_thickness,float(elevation)+slab_thickness) )
        pnt4 = ifcfile.createIfcCartesianPoint( (length_x,0.0,float(elevation)+slab_thickness) )
        
      
        
        pnt5 = ifcfile.createIfcCartesianPoint( (0.0,wall_interior_thickness,float(elevation)+slab_thickness) ) 
        pnt6 = ifcfile.createIfcCartesianPoint( (0.0,length_y,float(elevation)+slab_thickness) ) 
        pnt7 = ifcfile.createIfcCartesianPoint( (wall_interior_thickness,length_y,float(elevation)+slab_thickness) ) 
        pnt8 = ifcfile.createIfcCartesianPoint( (wall_interior_thickness,wall_interior_thickness,float(elevation)+slab_thickness) ) 
      
      
          
        wall_line_x 	 = ifcfile.createIfcPolyline([pnt1,pnt2,pnt3,pnt4])
        wall_line_y      = ifcfile.createIfcPolyline([pnt5,pnt6,pnt7,pnt8])
        
        ifcclosedprofile_x = ifcfile.createIfcArbitraryClosedProfileDef("AREA", None, wall_line_x) 
        ifcclosedprofile_y = ifcfile.createIfcArbitraryClosedProfileDef("AREA", None, wall_line_y) 
        ifc_direction    = ifcfile.createIfcDirection(Z)
        
        point = ifcfile.createIfcCartesianPoint((0.0,0.0,0.0))
        dir1 = ifcfile.createIfcDirection((0., 0., 1.))
        dir2 = ifcfile.createIfcDirection((1., 0., 0.))
        
        axis2placement = ifcfile.createIfcAxis2Placement3D(point, dir1, dir2)
        wall_solid_x = ifcfile.createIfcExtrudedAreaSolid(ifcclosedprofile_x,  axis2placement, ifc_direction, extrusion)
        wall_solid_y = ifcfile.createIfcExtrudedAreaSolid(ifcclosedprofile_y,  axis2placement, ifc_direction, extrusion)
        
      
        shape_representation 	= ifcfile.createIfcShapeRepresentation( ContextOfItems=context,
                                                                        RepresentationIdentifier='Body', 
                                                                        RepresentationType='SweptSolid',
                                                                        Items=[wall_solid_x, wall_solid_y])
        
        
        ifcopenshell.api.run("geometry.assign_representation", ifcfile, product=ifc_walltype, representation=shape_representation)
        ifcopenshell.api.run("spatial.assign_container", ifcfile, product=ifc_wall, relating_structure=building_storey) 

def create_wall_exterior(length_x, length_y, wall_interior_thickness, wall_covering_thickness, wall_exterior_thickness, cavity_thickness, slab_thickness, building_storey_height):
    print ("create wall exterior") 
    
    x1 = -wall_covering_thickness-cavity_thickness-wall_exterior_thickness
    y1 = -wall_covering_thickness-cavity_thickness-wall_exterior_thickness
    x2 = -wall_covering_thickness-cavity_thickness-wall_exterior_thickness
    y2 = -cavity_thickness-wall_exterior_thickness
    x3 = length_x
    y3 = -cavity_thickness-wall_exterior_thickness
    x4 = length_x
    y4 = -wall_covering_thickness-cavity_thickness-wall_exterior_thickness
    
    
    x5 = -wall_covering_thickness-cavity_thickness-wall_exterior_thickness
    y5 = -wall_covering_thickness-cavity_thickness-wall_exterior_thickness
    x6 = -wall_covering_thickness-cavity_thickness-wall_exterior_thickness
    y6 = length_y
    x7 = -cavity_thickness-wall_exterior_thickness
    y7 = length_y
    x8 = -cavity_thickness-wall_exterior_thickness
    y8 = -wall_covering_thickness-cavity_thickness-wall_exterior_thickness
    
    extrusion=(building_storey_height-slab_thickness)
    
    for building_storey in building_storey_list: 
    
        z = (building_storey.Elevation)
        
        ifc_wall 	= ifcopenshell.api.run("root.create_entity", ifcfile, ifc_class="IfcWall", name="wall_exterior_which_follows_grid" )
        ifc_walltype= ifcopenshell.api.run("root.create_entity", ifcfile, ifc_class="IfcWallType")
        ifcopenshell.api.run("type.assign_type", ifcfile, related_object=ifc_wall, relating_type=ifc_walltype) 
        
        
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

        wall_solid_x = ifcfile.createIfcExtrudedAreaSolid(ifcclosedprofile_x,  axis2placement, ifc_direction, extrusion+slab_thickness)
        wall_solid_y = ifcfile.createIfcExtrudedAreaSolid(ifcclosedprofile_y,  axis2placement, ifc_direction, extrusion+slab_thickness)
        
      
        shape_representation 	= ifcfile.createIfcShapeRepresentation( ContextOfItems=context,
                                                                        RepresentationIdentifier='Body', 
                                                                        RepresentationType='SweptSolid',
                                                                        Items=[wall_solid_x, wall_solid_y])
        
        
        ifcopenshell.api.run("geometry.assign_representation", ifcfile, product=ifc_walltype, representation=shape_representation)
        ifcopenshell.api.run("spatial.assign_container", ifcfile, product=ifc_wall, relating_structure=building_storey) 
           
        
        
        mymaterial = ifcfile.createIfcMaterial("brick")
        material_layer = ifcfile.createIfcMaterialLayer(mymaterial, 0.2, None)
        material_layer_set = ifcfile.createIfcMaterialLayerSet([material_layer], None)
        material_layer_set_usage = ifcfile.createIfcMaterialLayerSetUsage(material_layer_set, "AXIS2", "POSITIVE", -0.1)
        
        style = ifcopenshell.api.run("style.add_style", ifcfile, name="brick")
        ifcopenshell.api.run(
            "style.add_surface_style",
            ifcfile,
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
            ifcfile,
            material=mymaterial,
            style=style,
            context=context,
        )
        
        ifcfile.createIfcRelAssociatesMaterial(create_guid(), owner_history, RelatedObjects=[ifc_wall], RelatingMaterial=material_layer_set_usage)
        
        
def create_covering(length_x, length_y, wall_interior_thickness, slab_thickness, slab_covering_thickness, building_storey_height):
    print ("create covering")
    
    for building_storey in building_storey_list: 
    
        elevation = (building_storey.Elevation)
        
        ifc_covering	= ifcopenshell.api.run("root.create_entity", ifcfile, ifc_class="IfcCovering", name="slab_covering_which_follows_grid" )
        ifc_coveringtype= ifcopenshell.api.run("root.create_entity", ifcfile, ifc_class="IfcCoveringType")
        ifcopenshell.api.run("type.assign_type", ifcfile, related_object=ifc_covering, relating_type=ifc_coveringtype)
        
        pnt1 = ifcfile.createIfcCartesianPoint( (wall_interior_thickness,wall_interior_thickness,float(elevation)+slab_thickness) )
        pnt2 = ifcfile.createIfcCartesianPoint( (wall_interior_thickness,length_y-wall_interior_thickness,float(elevation+slab_thickness)) )
        pnt3 = ifcfile.createIfcCartesianPoint( (length_x-wall_interior_thickness,length_y-wall_interior_thickness,float(elevation+slab_thickness)) )
        pnt4 = ifcfile.createIfcCartesianPoint( (length_x-wall_interior_thickness,wall_interior_thickness,float(elevation+slab_thickness)) )
      
      
        covering_line 	= ifcfile.createIfcPolyline([pnt1,pnt2,pnt3,pnt4])
        ifcclosedprofile = ifcfile.createIfcArbitraryClosedProfileDef("AREA", None, covering_line)
        ifc_direction = ifcfile.createIfcDirection(Z)
        
        point = ifcfile.createIfcCartesianPoint((0.0,0.0,0.0))
        dir1 = ifcfile.createIfcDirection((0., 0., 1.))
        dir2 = ifcfile.createIfcDirection((1., 0., 0.))
        axis2placement = ifcfile.createIfcAxis2Placement3D(point, dir1, dir2)
        
        extrusion = slab_covering_thickness
        covering_solid = ifcfile.createIfcExtrudedAreaSolid(ifcclosedprofile,  axis2placement, ifc_direction, extrusion)
        shape_representation 	= ifcfile.createIfcShapeRepresentation( ContextOfItems=context,
                                                                        RepresentationIdentifier='Body', 
                                                                        RepresentationType='SweptSolid',
                                                                        Items=[covering_solid])
                                                                        
        ifcopenshell.api.run("geometry.assign_representation", ifcfile, product=ifc_coveringtype, representation=shape_representation)
        ifcopenshell.api.run("spatial.assign_container", ifcfile, product=ifc_covering, relating_structure=building_storey)
    
        
        material_concrete = ifcopenshell.api.run("material.add_material", ifcfile, name="concrete")
        
        style = ifcopenshell.api.run("style.add_style", ifcfile, name="concrete")
        ifcopenshell.api.run(
            "style.add_surface_style",
            ifcfile,
            style=style,
            attributes={
                "SurfaceColour": {
                    "Name": None,
                    "Red": 1.8,
                    "Green": 1.8,
                    "Blue": 1.5,
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
            ifcfile,
            material=material_concrete,
            style=style,
            context=context,
        )
        
        ifcfile.createIfcRelAssociatesMaterial(create_guid(), owner_history, RelatedObjects=[ifc_covering], RelatingMaterial=material_concrete)
        
        

def create_wall_insulation(length_x, length_y, wall_interior_thickness, wall_covering_thickness, slab_thickness, building_storey_height):
    print ("create wall insulation")  
    
    x1 = -wall_covering_thickness
    y1 = -wall_covering_thickness
    x2 = -wall_covering_thickness
    y2 = 0.0
    x3 = length_x
    y3 = 0.0
    x4 = length_x
    y4 = -wall_covering_thickness
    x5 = -wall_covering_thickness
    y5 = 0.0
    x6 = -wall_covering_thickness
    y6 = length_y
    x7 = 0.0
    y7 = length_y
    x8 = 0.0
    y8 = 0.0

    
    extrusion=(building_storey_height-slab_thickness)
    
    for building_storey in building_storey_list: 
    
        z = (building_storey.Elevation) 
        
        ifc_wall_insulation 	= ifcopenshell.api.run("root.create_entity", ifcfile, ifc_class="IfcCovering", name="wall_insulation_which_follows_grid" )
        ifc_walltype_insulation = ifcopenshell.api.run("root.create_entity", ifcfile, ifc_class="IfcCoveringType")
        ifcopenshell.api.run("type.assign_type", ifcfile, related_object=ifc_wall_insulation, relating_type=ifc_walltype_insulation) 
        
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
        wall_solid_x = ifcfile.createIfcExtrudedAreaSolid(ifcclosedprofile_x,  axis2placement, ifc_direction, extrusion+slab_thickness)
        wall_solid_y = ifcfile.createIfcExtrudedAreaSolid(ifcclosedprofile_y,  axis2placement, ifc_direction, extrusion+slab_thickness)
        
      
        shape_representation 	= ifcfile.createIfcShapeRepresentation( ContextOfItems=context,
                                                                        RepresentationIdentifier='Body', 
                                                                        RepresentationType='SweptSolid',
                                                                        Items=[wall_solid_x, wall_solid_y])
        
        
        ifcopenshell.api.run("geometry.assign_representation", ifcfile, product=ifc_walltype_insulation, representation=shape_representation)
        ifcopenshell.api.run("spatial.assign_container", ifcfile, product=ifc_wall_insulation, relating_structure=building_storey)   
        
    
        
        material_insulation = ifcopenshell.api.run("material.add_material", ifcfile, name="insulation")
        
        style = ifcopenshell.api.run("style.add_style", ifcfile, name="insulation")
        ifcopenshell.api.run(
            "style.add_surface_style",
            ifcfile,
            style=style,
            attributes={
                "SurfaceColour": {
                    "Name": None,
                    "Red": 2.2,
                    "Green": 2.5,
                    "Blue": 0.1,
                },
                "DiffuseColour": {
                    "Name": None,
                    "Red": 2.2,
                    "Green": 2.5,
                    "Blue": 0.1,
                },
                "Transparency": 0.0,
                "ReflectanceMethod": "PLASTIC",
            },
        )
        ifcopenshell.api.run(
            "style.assign_material_style",
            ifcfile,
            material=material_insulation,
            style=style,
            context=context,
        )
        
        ifcfile.createIfcRelAssociatesMaterial(create_guid(), owner_history, RelatedObjects=[ifc_wall_insulation], RelatingMaterial=material_insulation) 
   
   
def create_foundation(wall_interior_thickness, wall_covering_thickness, cavity_thickness, wall_exterior_thickness,foundation_beam_height):
    print ('create foundation')
    
    x1 = 0.0-wall_covering_thickness-cavity_thickness-wall_exterior_thickness
    y1 = 0.0-wall_covering_thickness-cavity_thickness-wall_exterior_thickness
    x2 = 0.0-wall_covering_thickness-cavity_thickness-wall_exterior_thickness
    y2 = wall_interior_thickness
    x3 = length_x
    y3 = wall_interior_thickness
    x4 = length_x
    y4 = 0.0-wall_covering_thickness-cavity_thickness-wall_exterior_thickness

    x5 = 0.0-wall_covering_thickness-cavity_thickness-wall_exterior_thickness
    y5 = wall_interior_thickness
    x6 = 0.0
    x6 = 0.0-wall_covering_thickness-cavity_thickness-wall_exterior_thickness
    y6 = length_y
    x7 = wall_interior_thickness
    y7 = length_y
    x8 = wall_interior_thickness
    y8 = wall_interior_thickness
    


        
    
    z = (building_storey_list[0].Elevation)-foundation_beam_height
        
    ifc_foundation 	= ifcopenshell.api.run("root.create_entity", ifcfile, ifc_class="IfcBeam", name="foundation_insulation_which_follows_grid" )
    ifc_foundationtype = ifcopenshell.api.run("root.create_entity", ifcfile, ifc_class="IfcBeamType")
    ifcopenshell.api.run("type.assign_type", ifcfile, related_object=ifc_foundation, relating_type=ifc_foundationtype) 
    
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
    wall_solid_x = ifcfile.createIfcExtrudedAreaSolid(ifcclosedprofile_x,  axis2placement, ifc_direction, foundation_beam_height)
    wall_solid_y = ifcfile.createIfcExtrudedAreaSolid(ifcclosedprofile_y,  axis2placement, ifc_direction, foundation_beam_height)
    
  
    shape_representation 	= ifcfile.createIfcShapeRepresentation( ContextOfItems=context,
                                                                    RepresentationIdentifier='Body', 
                                                                    RepresentationType='SweptSolid',
                                                                    Items=[wall_solid_x, wall_solid_y])
    
    
    ifcopenshell.api.run("geometry.assign_representation", ifcfile, product=ifc_foundationtype, representation=shape_representation)
    ifcopenshell.api.run("spatial.assign_container", ifcfile, product=ifc_foundation, relating_structure=building_storey_list[0])
    
     
#######################################################################################################
###################################   Config parameters   #############################################
#######################################################################################################
filename                    = "demo.ifc"
folder_path                 = "C:\\Algemeen\\07_prive\\08_ifc_bestanden\\"

building_storeys_amount     = 2         # is the n number of building storeys, can't be 0 or less than 0
elevation                   = 0.0       # is where the first of the building storeys start
building_storey_height      = 3000      # is the equal distance between the building storeys
   
grids_x_direction_amount    = 10        # is the n number of grids in x direction
grids_y_direction_amount    = 5         # is the n number of grids in y direction
grids_x_distance_between    = 600.0     # is the distance between the x grids, always should be a float
grids_y_distance_between    = 1200.0    # is the distance between the y grids, always should be a float
grid_extends                = 2000.0    # is the distance on how much the grid extends

slab_thickness              = 200.0  
wall_interior_thickness     = 200.0
wall_exterior_thickness     = 100.0
wall_covering_thickness     = 150.0
cavity_thickness            = 100.0
slab_covering_thickness     = 150.0
foundation_beam_height      = 1000.0

length_x = float(grids_x_direction_amount)*grids_x_distance_between - grids_x_distance_between  # calculates the total length in x direction
length_y = float(grids_y_direction_amount)*grids_y_distance_between - grids_y_distance_between  # calculates the total length in y direction
length_z = building_storey_height




###########################
### Calling the methods ###
###########################
create_building_storeys(building_storeys_amount,
                        elevation,
                        building_storey_height)
                        
create_grid(grids_x_distance_between,
            grids_y_distance_between,
            grids_x_direction_amount,
            grids_y_direction_amount,
            grid_extends)

create_foundation(  wall_interior_thickness,
                    wall_covering_thickness,
                    cavity_thickness,
                    wall_exterior_thickness,
                    foundation_beam_height,)
  
create_slab(length_x,
            length_y,
            slab_thickness )
  
create_wall_interior(length_x,
            length_y,
            wall_interior_thickness,
            slab_thickness,
            building_storey_height )
            
create_wall_exterior(length_x,
                     length_y,
                     wall_interior_thickness,
                     wall_exterior_thickness,
                     wall_covering_thickness,
                     cavity_thickness,
                     slab_thickness,
                     building_storey_height,
                     )
            
create_wall_insulation(length_x,
                        length_y,
                        wall_interior_thickness,
                        wall_covering_thickness,
                        slab_thickness,
                        building_storey_height )
            
create_covering(length_x,
                length_y,
                wall_interior_thickness,
                slab_thickness,
                slab_covering_thickness,
                building_storey_height )
                
                
                
#########################################################
### Removing the IFC from BlenderBIM and reloading it ###
#########################################################
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
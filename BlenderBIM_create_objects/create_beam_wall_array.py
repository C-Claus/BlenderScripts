import os
import bpy
import numpy
import ifcopenshell.api


 
#filename = os.path.join("_PATH_", "_FILE_NAME_.py")
#exec(compile(open(filename).read(), filename, 'exec'))





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





def create_beam_array(beam_name, beam_profile_x, beam_profile_y, beam_length_x, beam_total_length_n_y, beam_inbetween_distance):
    element_name=beam_name
    material_concrete = ifcopenshell.api.run("material.add_material", ifc_file, name='concrete')
    
    
    profile = ifc_file.create_entity("IfcRectangleProfileDef", ProfileType="AREA", XDim=beam_profile_x,YDim=beam_profile_y)
    
   
    #profile = ifc_file.create_entity("IfcIShapeProfileDef",
    #                            #ProfileType="AREA",
    #                            OverallWidth=beam_profile_x,#0.3,
    #                            OverallDepth=beam_profile_y,
    #                            WebThickness=0.01,
    #                            FlangeThickness=0.01,
    #                            FilletRadius=0.02,
    #                            ) 
   
    
    element = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class='IfcBeamType', name=element_name)
    
    rel = ifcopenshell.api.run("material.assign_material", ifc_file, product=element, type="IfcMaterialProfileSet")
    profile_set = rel.RelatingMaterial
    #material_profile = ifcopenshell.api.run( "material.add_profile", ifc_file, profile_set=profile_set, material=material)
    #ifcopenshell.api.run("material.assign_profile", ifc_file, material_profile=material_profile, profile=profile)

    profile.ProfileName = "square_profile"
    #or use:
    material_profile = ifcopenshell.api.run("material.add_profile", ifc_file, profile_set=profile_set, material=material_concrete, profile=profile)


    #occurrence = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcBeam", name=element_name, )
    #ifcopenshell.api.run("type.assign_type", ifc_file, related_object=occurrence, relating_type=element)
    #representation = ifcopenshell.api.run("geometry.add_profile_representation", ifc_file, context=representations["body"], profile=profile, depth=5)


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

        
    #beam on the y0 axis
    for i in range(0, beam_total_length_n_y, beam_inbetween_distance )[:-1]:
        matrix_2 = numpy.array(
                        (
                            (1.0, 0.0, 0.0, beam_profile_x/2),
                            (1.0, 1.0, 1.0, i+(beam_profile_x/2)),
                            (0.0, 0.0, 0.0, 0.0),
                            (0.0, 0.0, 0.0, 1.0),
                        )
                    )
                    
        matrix_2 = numpy.array(matrix_2)
        
        occurrence = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcBeam", name=element_name )
        representation = ifcopenshell.api.run("geometry.add_profile_representation", ifc_file, context=representations["body"], profile=profile, depth=beam_inbetween_distance-beam_profile_x)        
        ifcopenshell.api.run("geometry.edit_object_placement",ifc_file, product=occurrence, matrix=matrix_2) 
        ifcopenshell.api.run("spatial.assign_container", ifc_file, relating_structure=storey, product=occurrence)
        ifcopenshell.api.run("geometry.assign_representation", ifc_file, product=occurrence, representation=representation)
    
    #beam on the y axis with beamx offset
    for i in range(0, beam_total_length_n_y, beam_inbetween_distance )[:-1]:
        matrix_3 = numpy.array(
                        (
                            (1.0, 1.0, 0.0, beam_length_x-beam_profile_x/2),
                            (1.0, 1.0, 1.0, i+(beam_profile_x/2)),
                            (0.0, 0.0, 0.0, 0.0),
                            (0.0, 0.0, 0.0, 1.0),
                        )
                    )
                    
        matrix_3 = numpy.array(matrix_3)
        
        occurrence = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcBeam", name=element_name )
        representation = ifcopenshell.api.run("geometry.add_profile_representation", ifc_file, context=representations["body"], profile=profile, depth=beam_inbetween_distance-beam_profile_x)        
        ifcopenshell.api.run("geometry.edit_object_placement",ifc_file, product=occurrence, matrix=matrix_3) 
        ifcopenshell.api.run("spatial.assign_container", ifc_file, relating_structure=storey, product=occurrence)
        ifcopenshell.api.run("geometry.assign_representation", ifc_file, product=occurrence, representation=representation)     
    
    #beam on the x axis
    for i in range(0, beam_total_length_n_y, beam_inbetween_distance ): 
        
        matrix_1 = numpy.array(
                    (
                        (0.0, 0.0, 1.0, 0.0),
                        (1.0, 1.0, 0.0, i),
                        (0.0, 0.0, 0.0, 0.0),
                        (0.0, 0.0, 0.0, 1.0),
                    )
                )
                
        matrix_1 = numpy.array(matrix_1)
        
        occurrence = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcBeam", name=element_name )
        representation = ifcopenshell.api.run("geometry.add_profile_representation", ifc_file, context=representations["body"], profile=profile, depth=beam_length_x)
                
        ifcopenshell.api.run("geometry.edit_object_placement",ifc_file, product=occurrence, matrix=matrix_1) 
        ifcopenshell.api.run("spatial.assign_container", ifc_file, relating_structure=storey, product=occurrence)
        
        ifcopenshell.api.run("geometry.assign_representation", ifc_file, product=occurrence, representation=representation)
        
        
   
    
        

length_x = 10.0 #float(grids_x_direction_amount)*grids_x_distance_between - grids_x_distance_between
length_y = 10.0
#total_y = 10.0
#total_x = 5.0      


beam_name = 'beam_200x200mm'
beam_length_x = 3
beam_profile_y = 0.6
beam_profile_x = 0.1
beam_total_length_n_y = 5
beam_inbetween_distance = 1#=beam_length_y = 3





def create_slab(length_x, length_y, slab_thickness, slab_name):
    
    
    print ('create slab') 
    
    slab_name = 'slab_1'
    
    ifc_slab 	= ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcSlabType", name=slab_name )
    rel = ifcopenshell.api.run("material.assign_material", ifc_file, product=ifc_slab, type="IfcMaterialLayerSet")
    
  
    occurrence = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcSlab", name=slab_name )
    
    
    #material_concrete = ifcopenshell.api.run("material.add_material", ifc_file, name='concrete')
    #material_concrete = ifcopenshell.api.run("material.add_material_set", ifc_file, set_type="IfcMaterialLayerSet")
    
    material = ifcopenshell.api.run("material.add_material", ifc_file)
    material.Name = 'concrete'
    
    material_set = ifcopenshell.api.run("material.add_material_set", ifc_file, set_type="IfcMaterialLayerSet")
    material_set.LayerSetName = "concrete"
    

    ifcopenshell.api.run("material.add_layer", ifc_file, layer_set=material_set, material=material)
    ifcopenshell.api.run("material.assign_material", ifc_file, product=ifc_slab, material=material_set)
        
        
        
        
        
    #ifcopenshell.api.run("material.assign_material", ifc_file, product=ifc_slab, material=material_concrete)
    
    ifcopenshell.api.run("spatial.assign_container", ifc_file, relating_structure=storey, product=occurrence)
    
    context = ifc_file.createIfcGeometricRepresentationContext()
    rep = ifc_file.createIfcShapeRepresentation(ContextOfItems=context)
    
    ifcopenshell.api.run("geometry.assign_representation", ifc_file, product=occurrence, representation=rep)
    
    #representation 	= ifc_file.createIfcShapeRepresentation( ContextOfItems=context,
    #                                                                RepresentationIdentifier='Body', 
    #                                                                RepresentationType='SweptSolid',
    #                                                                Items=[slab_solid])
    
    
    
    #context = ifc_file.createIfcGeometricRepresentationContext()
    #rep = ifc_file.createIfcShapeRepresentation()
    #ifcopenshell.api.run("geometry.assign_representation", ifc_file, product=ifc_slab, representation=rep)
    
    
    #representation = ifcopenshell.api.run("geometry.add_profile_representation", ifc_file, context=representations["body"], profile=profile, depth=beam_length_x)
    
   
    #material_concrete.LayerSetName == "concrete"
    #assert material.is_a("IfcMaterialLayerSet")
    
    #representation = ifcopenshell.api.run("geometry.add_profile_representation", ifc_file, context=representations["body"], profile=profile, depth=beam_length_x)
                
    #    ifcopenshell.api.run("geometry.edit_object_placement",ifc_file, product=occurrence, matrix=matrix_1) 
    #    ifcopenshell.api.run("spatial.assign_container", ifc_file, relating_structure=storey, product=occurrence)
        
    #    ifcopenshell.api.run("geometry.assign_representation", ifc_file, product=occurrence, representation=representation)
    
    
    
    
    #rel = ifcopenshell.api.run("material.assign_material", ifc_file, product=element, type="IfcMaterialLayerSet")
  
    
    #element_name = slab_name
    
    #element = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class='IfcBeamType', name=element_name)
     
    #material_concrete = ifcopenshell.api.run("material.add_material", ifc_file, name='concrete')
    #rel = ifcopenshell.api.run("material.assign_material", ifc_file, product=element, type="IfcMaterialLayerSet")
    
    
    #element = ifcopenshell.api.run("root.create_entity", self.file, ifc_class="IfcWall")
    #rel = ifcopenshell.api.run("material.assign_material", self.file, product=element, type="IfcMaterialLayerSet")
    
    """
    elevation = 0.2
    
    ifc_slab 	= ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcSlab", name="slab" )
    ifc_slabtype= ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcSlabType")
    ifcopenshell.api.run("type.assign_type", ifc_file, related_object=ifc_slab, relating_type=ifc_slabtype)
    
    pnt1 = ifc_file.createIfcCartesianPoint( (0.0,0.0,float(elevation)) )
    pnt2 = ifc_file.createIfcCartesianPoint( (0.0,length_y,float(elevation)) )
    pnt3 = ifc_file.createIfcCartesianPoint( (length_x,length_y,float(elevation)) )
    pnt4 = ifc_file.createIfcCartesianPoint( (length_x,0.0,float(elevation)) )
  
  
    slab_line 	= ifc_file.createIfcPolyline([pnt1,pnt2,pnt3,pnt4])
    ifcclosedprofile = ifc_file.createIfcArbitraryClosedProfileDef("AREA", None, slab_line)
    ifc_direction = ifc_file.createIfcDirection(Z)
    
    point = ifc_file.createIfcCartesianPoint((0.0,0.0,0.0))
    dir1 = ifc_file.createIfcDirection((0., 0., 1.))
    dir2 = ifc_file.createIfcDirection((1., 0., 0.))
    axis2placement = ifc_file.createIfcAxis2Placement3D(point, dir1, dir2)
    
    extrusion = slab_thickness
    slab_solid = ifc_file.createIfcExtrudedAreaSolid(ifcclosedprofile,  axis2placement, ifc_direction, extrusion)
    shape_representation 	= ifc_file.createIfcShapeRepresentation( ContextOfItems=context,
                                                                    RepresentationIdentifier='Body', 
                                                                    RepresentationType='SweptSolid',
                                                                    Items=[slab_solid])
                                                                    
    ifcopenshell.api.run("geometry.assign_representation", ifc_file, product=ifc_slabtype, representation=shape_representation)
    ifcopenshell.api.run("spatial.assign_container", ifc_file, product=ifc_slab, relating_structure=storey) 
    
    """

create_slab(length_x=length_x, length_y=length_y, slab_thickness=0.2, slab_name='hoi')


def create_walls():
    print ('create walls' )
    
    material_wall = ifcopenshell.api.run("material.add_material", ifc_file, name='wall_material')
    
    #create materiallayerset
    #coordinates 
    
    
    
    
    

            
     
     
            
    
create_beam_array(beam_name, beam_profile_x, beam_profile_y, beam_length_x, beam_total_length_n_y, beam_inbetween_distance)

######################################################################################
#########################  Write file and load into BlenderBIM #######################
######################################################################################
folder_path = "C:\\Algemeen\\00_prive\\BlenderScripts\\BlenderBIM_create_objects\\ifc_library\\" 
filename = str(beam_name) + ".ifc"
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
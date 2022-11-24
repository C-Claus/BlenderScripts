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
    material = ifcopenshell.api.run("material.add_material", ifc_file, name='beam_material')
    profile = ifc_file.create_entity("IfcRectangleProfileDef", ProfileType="AREA", XDim=beam_profile_x,YDim=beam_profile_y)

    element = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class='IfcBeamType', name=element_name)
    rel = ifcopenshell.api.run("material.assign_material", ifc_file, product=element, type="IfcMaterialProfileSet")
    profile_set = rel.RelatingMaterial
    material_profile = ifcopenshell.api.run( "material.add_profile", ifc_file, profile_set=profile_set, material=material)
    ifcopenshell.api.run("material.assign_profile", ifc_file, material_profile=material_profile, profile=profile)

    profile.ProfileName = "square_profile"
    #or use:
    #material_profile = ifcopenshell.api.run("material.add_profile", ifc_file, profile_set=profile_set, material=material, profile=profile)


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

          

    for i in range(0, beam_total_length_n_y, beam_inbetween_distance )[:-1]:
        matrix_2 = numpy.array(
                        (
                            (0.0, 1.0, 0.0, beam_profile_y/2),
                            (1.0, 1.0, 1.0, i+(beam_profile_y/2)),
                            (1.0, 0.0, 0.0, 0.0),
                            (0.0, 0.0, 0.0, 1.0),
                        )
                    )
                    
        matrix_2 = numpy.array(matrix_2)
        
        occurrence = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcBeam", name=element_name )
        representation = ifcopenshell.api.run("geometry.add_profile_representation", ifc_file, context=representations["body"], profile=profile, depth=beam_inbetween_distance-beam_profile_y)        
        ifcopenshell.api.run("geometry.edit_object_placement",ifc_file, product=occurrence, matrix=matrix_2) 
        ifcopenshell.api.run("spatial.assign_container", ifc_file, relating_structure=storey, product=occurrence)
        ifcopenshell.api.run("geometry.assign_representation", ifc_file, product=occurrence, representation=representation)
        
    for i in range(0, beam_total_length_n_y, beam_inbetween_distance )[:-1]:
        matrix_3 = numpy.array(
                        (
                            (0.0, 1.0, 0.0, beam_length_x-beam_profile_y/2),
                            (1.0, 1.0, 1.0, i+(beam_profile_y/2)),
                            (1.0, 0.0, 0.0, 0.0),
                            (0.0, 0.0, 0.0, 1.0),
                        )
                    )
                    
        matrix_3 = numpy.array(matrix_3)
        
        occurrence = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcBeam", name=element_name )
        representation = ifcopenshell.api.run("geometry.add_profile_representation", ifc_file, context=representations["body"], profile=profile, depth=beam_inbetween_distance-beam_profile_y)        
        ifcopenshell.api.run("geometry.edit_object_placement",ifc_file, product=occurrence, matrix=matrix_3) 
        ifcopenshell.api.run("spatial.assign_container", ifc_file, relating_structure=storey, product=occurrence)
        ifcopenshell.api.run("geometry.assign_representation", ifc_file, product=occurrence, representation=representation)     

    for i in range(0, beam_total_length_n_y, beam_inbetween_distance ): 
        
        matrix_1 = numpy.array(
                    (
                        (0.0, 0.0, 1.0, 0.0),
                        (0.0, 1.0, 0.0, i),
                        (1.0, 0.0, 0.0, 0.0),
                        (0.0, 0.0, 0.0, 1.0),
                    )
                )
                
        matrix_1 = numpy.array(matrix_1)
        
        occurrence = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcBeam", name=element_name )
        representation = ifcopenshell.api.run("geometry.add_profile_representation", ifc_file, context=representations["body"], profile=profile, depth=beam_length_x)
                
        ifcopenshell.api.run("geometry.edit_object_placement",ifc_file, product=occurrence, matrix=matrix_1) 
        ifcopenshell.api.run("spatial.assign_container", ifc_file, relating_structure=storey, product=occurrence)
        
        ifcopenshell.api.run("geometry.assign_representation", ifc_file, product=occurrence, representation=representation)

        """
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
        """

beam_name = 'beam_200x200mm'
beam_length_x = 3
beam_profile_y = 0.2
beam_profile_x = 0.2
beam_total_length_n_y = 5
beam_inbetween_distance = 1#=beam_length_y = 3


column_name = 'column_200x200mm'
column_length_x = 3
column_profile_y = 0.2
column_profile_x = 0.2
#column_total_length_n_y = 5
#column_inbetween_distance = 2 

def create_column_array(column_name, column_profile_x, column_profile_y, column_length_y, column_total_length_n_y, column_inbetween_distance, beam_profile_y, beam_profile_x, beam_length_x):
    print ('create column array')

    #beam_name, beam_profile_x, beam_profile_y, beam_length_x, beam_total_length_n_y, beam_inbetween_distance)

    #IfcRoundedRectangleProfileDef
    material = ifcopenshell.api.run("material.add_material", ifc_file, name='column_material')
    #profile = ifc_file.create_entity("IfcRectangleProfileDef", ProfileType="AREA", XDim=column_profile_x,YDim=column_profile_y)
    
    #profile = ifc_file.create_entity("IfcRoundedRectangleProfileDef", ProfileType="AREA", XDim=column_profile_x,YDim=column_profile_y. RoundingRadius=0.02)
    
    """
    profile = ifc_file.create_entity("IfcRectangleHollowProfileDef",
                                    ProfileType="AREA",
                                    XDim=column_profile_x,
                                    YDim=column_profile_y,
                                    WallThickness=0.01,
                                    InnerFilletRadius=0.02,
                                    OuterFilletRadius=0.02)
    """                                
                                    
    profile = ifc_file.create_entity("IfcIShapeProfileDef",
                                    #ProfileType="AREA",
                                    OverallWidth=0.2,
                                    OverallDepth=0.2,
                                    WebThickness=0.01,
                                    FlangeThickness=0.01,
                                    FilletRadius=0.02,
                                    )                            
                                    
                                    
                                    
    
    

    element = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class='IfcColumnType', name=column_name)
    rel = ifcopenshell.api.run("material.assign_material", ifc_file, product=element, type="IfcMaterialProfileSet")
    profile_set = rel.RelatingMaterial
    material_profile = ifcopenshell.api.run( "material.add_profile", ifc_file, profile_set=profile_set, material=material)
    ifcopenshell.api.run("material.assign_profile", ifc_file, material_profile=material_profile, profile=profile)

    profile.ProfileName = "square_profile"


    for i in range(0, column_total_length_n_y, column_inbetween_distance ): 
        
        print (i)
        
        matrix_y = numpy.array(
                        (
                            (1.0, 0.0, 0.0, column_profile_x/2),
                            (0.0, 1.0, 0.0, i),
                            (0.0, 0.0, 1.0, beam_profile_x/2),
                            (0.0, 0.0, 0.0, 0.0),
                        )
                    )
                    
        matrix_y = numpy.array(matrix_y)
        
        print (matrix_y)

        occurrence = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcColumn", name=column_name )
        
        #representation = ifcopenshell.api.run("geometry.add_profile_representation", ifc_file, context=representations["body"], profile=profile, depth=beam_inbetween_distance-beam_profile_y)  
        representation = ifcopenshell.api.run("geometry.add_profile_representation", ifc_file, context=representations["body"], profile=profile, depth=column_length_x)       
        
        ifcopenshell.api.run("geometry.edit_object_placement",ifc_file, product=occurrence, matrix=matrix_y) 
        #ifcopenshell.api.run("geometry.edit_object_placement",ifc_file, product=occurrence) 
       
        ifcopenshell.api.run("spatial.assign_container", ifc_file, relating_structure=storey, product=occurrence)
        ifcopenshell.api.run("geometry.assign_representation", ifc_file, product=occurrence, representation=representation)
        
        
        
    for i in range(0, column_total_length_n_y, column_inbetween_distance ): 
        
        print (i)
        
        matrix_y = numpy.array(
                        (
                            (1.0, 0.0, 0.0, beam_length_x-(column_profile_x/2)),
                            (0.0, 1.0, 0.0, i),
                            (0.0, 0.0, 1.0, beam_profile_x/2),
                            (0.0, 0.0, 0.0, 0.0),
                        )
                    )
                    
        matrix_y = numpy.array(matrix_y)
        
        print (matrix_y)

        occurrence = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcColumn", name=column_name )
        
        #representation = ifcopenshell.api.run("geometry.add_profile_representation", ifc_file, context=representations["body"], profile=profile, depth=beam_inbetween_distance-beam_profile_y)  
        representation = ifcopenshell.api.run("geometry.add_profile_representation", ifc_file, context=representations["body"], profile=profile, depth=column_length_x)       
        
        ifcopenshell.api.run("geometry.edit_object_placement",ifc_file, product=occurrence, matrix=matrix_y) 
        #ifcopenshell.api.run("geometry.edit_object_placement",ifc_file, product=occurrence) 
       
        ifcopenshell.api.run("spatial.assign_container", ifc_file, relating_structure=storey, product=occurrence)
        ifcopenshell.api.run("geometry.assign_representation", ifc_file, product=occurrence, representation=representation) 
 


            
     
     
            
    
create_beam_array(beam_name, beam_profile_x, beam_profile_y, beam_length_x, beam_total_length_n_y, beam_inbetween_distance)
create_column_array(column_name, column_profile_x, column_profile_y, column_length_x, beam_total_length_n_y, beam_inbetween_distance, beam_profile_y, beam_profile_x, beam_length_x)

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
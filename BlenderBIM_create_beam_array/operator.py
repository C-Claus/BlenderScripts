import os
import bpy
import numpy
import ifcopenshell.api
from ifcopenshell.api import run

print ('hallo uit operator')

class CreateArray(bpy.types.Operator):
    """Create Beam Array"""
    bl_idname = "create.array"
    bl_label = "Create array"

    def execute(self, context):

        file_path = "C:\\Algemeen\\07_ifcopenshell\\00_ifc\\02_ifc_library\\model.ifc"

        ifc_file = self.create_project(file_path)
        
        self.load_ifc(ifc_file, file_path)


        return {'FINISHED'}


    def create_project(self, file_path):
        

        model = ifcopenshell.file()


        # All projects must have one IFC Project element
        project = run("root.create_entity", model, ifc_class="IfcProject", name="My Project")

        # Geometry is optional in IFC, but because we want to use geometry in this example, let's define units
        # Assigning without arguments defaults to metric units
        run("unit.assign_unit", model)

        # Let's create a modeling geometry context, so we can store 3D geometry (note: IFC supports 2D too!)
        context = run("context.add_context", model, context_type="Model")

        # In particular, in this example we want to store the 3D "body" geometry of objects, i.e. the body shape
        body = run("context.add_context", model, context_type="Model",
            context_identifier="Body", target_view="MODEL_VIEW", parent=context)

        # Create a site, building, and storey. Many hierarchies are possible.
        site = run("root.create_entity", model, ifc_class="IfcSite", name="My Site")
        building = run("root.create_entity", model, ifc_class="IfcBuilding", name="Building A")
        storey = run("root.create_entity", model, ifc_class="IfcBuildingStorey", name="Ground Floor")

        # Since the site is our top level location, assign it to the project
        # Then place our building on the site, and our storey in the building
        run("aggregate.assign_object", model, relating_object=project, product=site)
        run("aggregate.assign_object", model, relating_object=site, product=building)
        run("aggregate.assign_object", model, relating_object=building, product=storey)

        #self.create_wall(model, body, storey)
        self.create_beam(model, body, storey)



        model.write(file_path)

        return model

 
    def create_wall(self, model, body, storey):
        wall = run("root.create_entity", model, ifc_class="IfcWall")
        # Add a new wall-like body geometry, 5 meters long, 3 meters high, and 200mm thick
        representation = run("geometry.add_wall_representation", model, context=body, length=10, height=6, thickness=0.2)
        # Assign our new body geometry back to our wall
        run("geometry.assign_representation", model, product=wall, representation=representation)

        # Place our wall in the ground floor
        run("spatial.assign_container", model, relating_structure=storey, product=wall)

    def create_beam(self, model, body, storey):

        #create material
        material_concrete = run("material.add_material", model, name='concrete')

        #create profile
        profile = model.create_entity("IfcRectangleProfileDef", ProfileType="AREA", XDim=200,YDim=500)

        beam = run("root.create_entity", model, ifc_class='IfcBeamType', name='my_beam')

        rel = run("material.assign_material", model, product=beam, type="IfcMaterialProfileSet")

        profile_set = rel.RelatingMaterial

        material_profile = run("material.add_profile", model, profile_set=profile_set, material=material_concrete)

        run("material.assign_profile", model, material_profile=material_profile, profile=profile)

        profile.ProfileName = "square_profile"

        occurrence = run("root.create_entity", model, ifc_class="IfcBeam", name='beam_name' )

        run("type.assign_type", model, related_object=occurrence, relating_type=beam)



        model_ = run("context.add_context", model, context_type="Model")
        plan = run("context.add_context", model, context_type="Plan")


        representations = {
            "body": run(
                "context.add_context",
                model,
                context_type="Model",
                context_identifier="Body",
                target_view="MODEL_VIEW",
                parent=model_,
            ),
            "annotation": run(
                "context.add_context",
                model,
                context_type="Plan",
                context_identifier="Annotation",
                target_view="PLAN_VIEW",
                parent=plan,
            ),
        }
  
         

        
        matrix_origin = numpy.array(
                            (
                                (1.0, 0.0, 0.0, 0.0),
                                (1.0, 1.0, 1.0, 0.0),
                                (0.0, 0.0, 0.0, 0.0),
                                (0.0, 0.0, 0.0, 0.0),
                            )
                        ) 
        occurrence =  run("root.create_entity", model, ifc_class="IfcBeam", name='element_name')
        representation = run("geometry.add_profile_representation", model, context=representations["body"], profile=profile, depth=5)

        run("geometry.edit_object_placement",model, product=occurrence, matrix=matrix_origin) 
        run("spatial.assign_container", model, relating_structure=storey, product=occurrence)
        run("geometry.assign_representation", model, product=occurrence, representation=representation)


        for i in range(0, 10, 1):
            matrix_x = numpy.array(
                            (
                                (1.0, 0.0, 0.0, i),
                                (1.0, 1.0, 1.0, 0.0),
                                (0.0, 0.0, 0.0, 0.0),
                                (0.0, 0.0, 0.0, 1.0),
                            )
                        )
                        
            matrix_x = numpy.array(matrix_x)

            occurrence =  run("root.create_entity", model, ifc_class="IfcBeam", name='element_name')
            representation = run("geometry.add_profile_representation", model, context=representations["body"], profile=profile, depth=5) 
        
            run("geometry.edit_object_placement",model, product=occurrence, matrix=matrix_x) 
            run("spatial.assign_container", model, relating_structure=storey, product=occurrence)
            run("geometry.assign_representation", model, product=occurrence, representation=representation)




    def create_beam_array(self, ifc_file, representations, beam_name, beam_profile_x, beam_profile_y, beam_length_x, beam_total_length_n_y, beam_inbetween_distance):

        print ('hallo uit beam array')
        element_name=beam_name
        material_concrete = ifcopenshell.api.run("material.add_material", ifc_file, name='concrete')
        
        profile = model.create_entity("IfcRectangleProfileDef", ProfileType="AREA", XDim=beam_profile_x,YDim=beam_profile_y)
        
    
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
        material_profile = ifcopenshell.api.run( "material.add_profile", ifc_file, profile_set=profile_set, material=material_concrete)
        ifcopenshell.api.run("material.assign_profile", ifc_file, material_profile=material_profile, profile=profile)

        profile.ProfileName = "square_profile"
        #or use:
        #material_profile = ifcopenshell.api.run("material.add_profile", ifc_file, profile_set=profile_set, material=material_concrete, profile=profile)


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

           
        
        

        

    def load_ifc(self, ifc_file, file_path):

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
                    
        


         
        



"""

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
        
        

length_x = 20.0
length_y = 20.0
beam_name = 'beam_200x200mm'
beam_length_x = 7
beam_profile_y = 0.7
beam_profile_x = 0.2
beam_total_length_n_y = 10
beam_inbetween_distance = 2



create_beam_array(beam_name, beam_profile_x, beam_profile_y, beam_length_x, beam_total_length_n_y, beam_inbetween_distance)

beam_name = 'beam'
folder_path = "C:\\Algemeen\\07_ifcopenshell\\00_ifc\\02_ifc_library\\" 
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

"""

def register():
    bpy.utils.register_class(CreateArray)


def unregister():
    bpy.utils.unregister_class(CreateArray)
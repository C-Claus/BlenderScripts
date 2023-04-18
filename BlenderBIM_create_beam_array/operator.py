import os
import bpy
import numpy as np
import ifcopenshell.api
from ifcopenshell.api import run
from . import operator
import math

#https://github.com/buildingSMART/IFC4.3.x-development/blob/master/docs/schemas/shared/IfcSharedBldgElements/Entities/IfcWall.md
#1 make checbox to include insulation
#2 make button which bakes an IfcRelAggregates to an IfcProjectLibrary
#3 should behave as an IfcWall, test with IfcOpeningElements
class CreateBeamArray(bpy.types.Operator):
    """Create Beam Array"""
    bl_idname = "create.array"
    bl_label = "Create Beam System"

    def execute(self, context):

        file_path = "C:\\Algemeen\\07_ifcopenshell\\00_ifc\\02_ifc_library\\model.ifc"

        ifc_file = self.create_project(context,file_path)
        
        self.load_ifc(ifc_file, file_path)

        return {'FINISHED'}


    def create_project(self, context, file_path):

        dimension_properties = context.scene.dimension_properties
        
        model = ifcopenshell.file()
        project = run("root.create_entity", model, ifc_class="IfcProject", name="My Project")
        run("unit.assign_unit", model)
        
        #, length={"is_metric": True, "raw": "METERS"})
        #run("unit.assign_unit", ifc_file, length={"is_metric": True, "raw": "MILIMETERS"})

        context = run("context.add_context", model, context_type="Model")
        body = run("context.add_context", model, context_type="Model",context_identifier="Body", target_view="MODEL_VIEW", parent=context)

        site = run("root.create_entity", model, ifc_class="IfcSite", name="My Site")
        building = run("root.create_entity", model, ifc_class="IfcBuilding", name="Building A")
        storey = run("root.create_entity", model, ifc_class="IfcBuildingStorey", name="Ground Floor")

        run("aggregate.assign_object", model, relating_object=project, product=site)
        run("aggregate.assign_object", model, relating_object=site, product=building)
        run("aggregate.assign_object", model, relating_object=building, product=storey)



        beam_name = 'my_beam'
 
        x_dim = dimension_properties.my_profile_x
        y_dim = dimension_properties.my_profile_y
        center_to_center_distance = dimension_properties.my_center_to_center_distance
        covering_thickness = 0.02
        beam_length_y = dimension_properties.my_height - x_dim/1000 - (x_dim/1000)/2
        total_length_x = float(dimension_properties.my_length)
        x_N = dimension_properties.my_n


        self.create_beam_array(model, body, storey, beam_name, x_dim, y_dim, center_to_center_distance, x_N, beam_length_y, total_length_x)

        if dimension_properties.my_insulation:
            self.create_insulation(model, body, storey, center_to_center_distance, x_dim, y_dim, x_N, beam_length_y, total_length_x)

        if dimension_properties.my_covering_interior:
            isexternal = False
            self.create_covering(isexternal, model, body, storey, center_to_center_distance, x_dim, y_dim, x_N, beam_length_y, covering_thickness, total_length_x)

        if dimension_properties.my_covering_exterior:
            isexternal = True
            self.create_covering(isexternal, model, body, storey, center_to_center_distance, x_dim, y_dim, x_N, beam_length_y, covering_thickness, total_length_x)
        
        

        model.write(file_path)

        ifc_file = ifcopenshell.open(file_path)
        products = ifc_file.by_type('IfcProduct')

        global_id_list = []
        for product in products:
            global_id_list.append(product.GlobalId)


        #rel_aggregates = ifc_file.createIfcRelAggregates('1AEAi$cjvFNxxkPAdOIzkr', global_id_list)
        #print ('REL AGGREGATES', rel_aggregates)

        # set the Name attribute of the IfcRelAggregates object
        #rel_aggregates.Name = "Example Aggregation"

        # add the IfcRelAggregates object to the IFC file
        #ifc_file.add(rel_aggregates)

        return model

    def create_covering(self, isexternal, model, body, storey, center_to_center_distance, x_dim, y_dim, x_N, beam_length_y, covering_thickness, total_length_x):
        print ('create coviering')

        

        style = run("style.add_style", model, name="My style")
   
        run("style.add_surface_style", model, style=style, ifc_class="IfcSurfaceStyleShading", attributes={
                    "SurfaceColour": { "Name": None, "Red": 2.2, "Green": 2.2, "Blue": 2.2 }
                })

        if isexternal == False:

            matrix_x = np.array(
                                (
                                    (1.0, 0.0, 0.0, -(x_dim/1000)/2),
                                    (1.0, 1.0, 1.0, -(x_dim/1000)/2),
                                    (0.0, 0.0, 0.0, (-y_dim/1000)/2),
                                    (0.0, 0.0, 0.0, 1.0),
                                )
                            )

            wall = run("root.create_entity", model, ifc_class="IfcCovering",name="insulation")
            
            representation = run("geometry.add_wall_representation", model, context=body, length=total_length_x, height=beam_length_y+(x_dim/1000)*2, thickness=covering_thickness)
            run("geometry.assign_representation", model, product=wall, representation=representation)
            run("geometry.edit_object_placement",model, product=wall, matrix=matrix_x) 
            run("spatial.assign_container", model, relating_structure=storey, product=wall)
            run("style.assign_representation_styles", model, shape_representation=representation, styles=[style])

        #top covering
        if isexternal == True:
            matrix_x = np.array(
                                (
                                    (1.0, 0.0, 0.0, -(x_dim/1000)/2),
                                    (1.0, 1.0, 1.0, -(x_dim/1000)/2),
                                    (0.0, 0.0, 0.0, (y_dim/1000)/2+covering_thickness),
                                    (0.0, 0.0, 0.0, 1.0),
                                )
                            )

            wall = run("root.create_entity", model, ifc_class="IfcCovering",name="insulation")
            
            representation = run("geometry.add_wall_representation", model, context=body, length=total_length_x-center_to_center_distance+(x_dim/1000), height=beam_length_y+(x_dim/1000)*2, thickness=covering_thickness)
            run("geometry.assign_representation", model, product=wall, representation=representation)
            run("geometry.edit_object_placement",model, product=wall, matrix=matrix_x) 
            run("spatial.assign_container", model, relating_structure=storey, product=wall)
            run("style.assign_representation_styles", model, shape_representation=representation, styles=[style])


    def create_insulation(self, model, body, storey, center_to_center_distance, x_dim, y_dim, x_N, beam_length_y, total_length_x):

        style = run("style.add_style", model, name="My style")
   
        run("style.add_surface_style", model, style=style, ifc_class="IfcSurfaceStyleShading", attributes={
                    "SurfaceColour": { "Name": None, "Red": 1., "Green": 1.0, "Blue": 0. }
                })
      
        for i in np.arange(0, total_length_x+center_to_center_distance, center_to_center_distance)[:-1]:
           
            matrix_x = np.array(
                            (
                                (1.0, 0.0, 0.0, (x_dim/1000)/2+i),
                                (1.0, 1.0, 1.0, (x_dim/1000)/2),
                                (0.0, 0.0, 0.0, y_dim/1000/2),
                                (0.0, 0.0, 0.0, 1.0),
                            )
                        )
                        
            matrix_x = np.array(matrix_x)

            wall = run("root.create_entity", model, ifc_class="IfcCovering",name="insulation")
          
            representation = run("geometry.add_wall_representation", model, context=body, length=center_to_center_distance-x_dim/1000, height=beam_length_y, thickness=y_dim/1000)
            run("geometry.assign_representation", model, product=wall, representation=representation)
            run("geometry.edit_object_placement",model, product=wall, matrix=matrix_x) 
            run("spatial.assign_container", model, relating_structure=storey, product=wall)
            run("style.assign_representation_styles", model, shape_representation=representation, styles=[style])

    def create_beam_array(self, model, body, storey, beam_name, x_dim, y_dim, center_to_center_distance, x_N, beam_length_y, total_length_x):

        profile_offset_y = (x_dim/1000)/2

        style = run("style.add_style", model, name="My style")
   
        run("style.add_surface_style", model, style=style, ifc_class="IfcSurfaceStyleShading", attributes={
                    "SurfaceColour": { "Name": None, "Red": 1., "Green": 0.5, "Blue": 0. }
                })

        material_concrete = run("material.add_material", model, name='wood')
        profile = model.create_entity("IfcRectangleProfileDef", ProfileType="AREA", XDim=x_dim,YDim=y_dim)
        #profile = model.create_entity("IfcIShapeProfileDef",
        #                            ProfileType="AREA",
        #                            OverallWidth=x_dim,
        #                            OverallDepth=y_dim,
        #                            WebThickness=0.1,
        #                            FlangeThickness=0.1,
        #                            FilletRadius=0.2,
        #                            ) 
    
        member= run("root.create_entity", model, ifc_class='IfcMemberType', name=beam_name)
        rel = run("material.assign_material", model, product=member, type="IfcMaterialProfileSet")
        profile_set = rel.RelatingMaterial
        material_profile = run("material.add_profile", model, profile_set=profile_set, material=material_concrete)
        run("material.assign_profile", model, material_profile=material_profile, profile=profile)
        profile.ProfileName = "square_profile"

        #occurrence = run("root.create_entity", model, ifc_class="IfcBeam", name=beam_name )
        #run("type.assign_type", model, related_object=occurrence, relating_type=member)
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


        for x in np.arange(0, total_length_x+center_to_center_distance, center_to_center_distance):
          
            matrix_x = np.array(
                            (
                                (1.0, 0.0, 0.0, x),
                                (1.0, 1.0, 1.0, profile_offset_y),
                                (0.0, 0.0, 0.0, 0.0),
                                (0.0, 0.0, 0.0, 1.0),
                            )
                        )
                        
            matrix_x = np.array(matrix_x)

            occurrence =  run("root.create_entity", model, ifc_class="IfcMember", name=beam_name)
            representation = run("geometry.add_profile_representation",
                                model,
                                context=representations["body"],
                                profile=profile,
                                depth=beam_length_y) 
        
            run("geometry.edit_object_placement",model, product=occurrence, matrix=matrix_x) 
            run("spatial.assign_container", model, relating_structure=storey, product=occurrence)
            run("geometry.assign_representation", model, product=occurrence, representation=representation)
            run("style.assign_representation_styles", model, shape_representation=representation, styles=[style])

        #bottom beam
        matrix_y = np.array(
                            (
                                (1.0, 1.0, 1.0, -(x_dim/1000)/2),
                                (1.0, 0.0, 0.0, 0.0),
                                (0.0, 0.0, 0.0, 0.0),
                                (0.0, 0.0, 0.0, 1.0),
                            )
                        )
                        
        matrix_y = np.array(matrix_y)
        occurrence =  run("root.create_entity", model, ifc_class="IfcMember", name=beam_name)
        representation = run("geometry.add_profile_representation",
                            model,
                            context=representations["body"],
                            profile=profile,
                            depth=total_length_x+(x_dim/1000)) 
    
        run("geometry.edit_object_placement",model, product=occurrence, matrix=matrix_y) 
        run("spatial.assign_container", model, relating_structure=storey, product=occurrence)
        run("geometry.assign_representation", model, product=occurrence, representation=representation)
        run("style.assign_representation_styles", model, shape_representation=representation, styles=[style])


        #top beam
        matrix_y = np.array(
                            (
                                (1.0, 1.0, 1.0, -(x_dim/1000)/2),
                                (1.0, 0.0, 0.0, beam_length_y+(x_dim/1000)),
                                (0.0, 0.0, 0.0, 0.0),
                                (0.0, 0.0, 0.0, 1.0),
                            )
                        )
                        
        matrix_y = np.array(matrix_y)
        occurrence =  run("root.create_entity", model, ifc_class="IfcBeam", name=beam_name)
        representation = run("geometry.add_profile_representation",
                            model,
                            context=representations["body"],
                            profile=profile,
                            depth=total_length_x+(x_dim/1000)) 
    
        run("geometry.edit_object_placement",model, product=occurrence, matrix=matrix_y) 
        run("spatial.assign_container", model, relating_structure=storey, product=occurrence)
        run("geometry.assign_representation", model, product=occurrence, representation=representation)
        run("style.assign_representation_styles", model, shape_representation=representation, styles=[style])
       
    

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
                    

def register():
    bpy.utils.register_class(CreateBeamArray)



def unregister():
    bpy.utils.unregister_class(CreateBeamArray)

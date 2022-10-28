import bpy
import ifcopenshell
import blenderbim.bim.import_ifc
from blenderbim.bim.ifc import IfcStore

file_path = "C:\\Algemeen\\00_prive\\08_ifc_bestanden\\beam_types.ifc"



bpy.ops.bim.create_project()
bpy.ops.export_ifc.bim(filepath=file_path, should_save_as=True)


def create_beam():
    
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

    bpy.ops.bim.assign_class(ifc_class="IfcBeamType", predefined_type="BEAM", userdefined_type="")


    
    
    bpy.context.object.BIMObjectMaterialProperties.material_type = 'IfcMaterialProfileSet'
    
    
    
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

"""
o = bpy.data.objects.new( "empty", None )

# due to the new mechanism of "collection"
bpy.context.scene.collection.objects.link( o )

# empty_draw was replaced by empty_display
o.empty_display_size = 2
o.empty_display_type = 'PLAIN_AXES'

"""




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
                
                
        """     
        if ifc_types is not None:
            
            for i in ifc_types:
                collection_name_types = 'Types'
                    
            collection_types = bpy.data.collections.get(str(collection_name_types))
            
            if collection_types is not None:
                for obj in collection.objects:
                    bpy.data.objects.remove(obj, do_unlink=True)
                    
                bpy.data.collections.remove(collection_types)
            
        """          
            
                
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)         
        bpy.ops.bim.load_project(filepath=file_path)
               
load_ifc_automatically()
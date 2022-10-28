import ifcopenshell
import csv
import pandas as pd

#option 1 use csv library

#for k, v in wall_dictonary:
#   k['IfcElement'] 
#   k['IfcElementType']

def get_library(csv_library):
    
    library_list = []
    library_dict = {}
    
    ifc_element_list = []
    ifc_element_type_list = []
    ifc_material_list = []
    ifc_pset_list = []
    
    
    
    
    with open(csv_library, newline='') as library_file:
        library = csv.reader(library_file, delimiter=' ', quotechar='|')
        
        for i, row in enumerate(library):
            
            print (i, row)
            if i>0:
            
                for j in row:                    

                  
                    ifc_element = (j.split(';')[0])
                    ifc_element_type = (j.split(';')[1])
                    ifc_material = (j.split(';')[2])
                    
                    
                    ifc_element_list.append(ifc_element)
                    ifc_element_type_list.append(ifc_element_type)
                    ifc_material_list.append(ifc_material)
                    
            if i==0:
                ifc_element = (row[0].split(';')[0])
                ifc_element_type = (row[0].split(';')[1])
                       
                library_dict[ifc_element] = ifc_element_list
                library_dict[ifc_element_type] = ifc_element_type_list
                library_dict['ifc_material_list'] = ifc_material_list
                
  
                
    
                
    print ("hallo",library_dict)  
    
    
             
    
csv_library = "C:\\Algemeen\\00_prive\\BlenderScripts\\BlenderBIMLibrary\\IfcWallLibrary.csv"          
get_library(csv_library=csv_library)            


#option 2 use pandas 
def get_wall_library():
 
        
    library_data_frame = pd.read_csv(csv_library, ";")
    

 
    
   
    #print (library_data_frame['IfcElement'].values)
    
    for element in (library_data_frame.values):
        print (element)
      
      
      
"""  
       
def create_ifc_library():
    print ('create ifc library')    
    
    import ifcopenshell.api
    
    

class LibraryGenerator:
    def generate(self):
        ifcopenshell.api.pre_listeners = {}  # I don't know if it's useful but I don't want to break anything so I'm keeping this
        ifcopenshell.api.post_listeners = {}

        self.file = ifcopenshell.api.run("project.create_file")
        self.project = ifcopenshell.api.run(
            "root.create_entity", self.file, ifc_class="IfcProject", name="BlenderBIM Demo"
        )
        self.library = ifcopenshell.api.run(
            "root.create_entity", self.file, ifc_class="IfcProjectLibrary", name="BlenderBIM Demo Library"
        )
        ifcopenshell.api.run(
            "project.assign_declaration", self.file, definition=self.library, relating_context=self.project
        )
        ifcopenshell.api.run("unit.assign_unit", self.file, length={"is_metric": True, "raw": "METERS"})
        self.material = ifcopenshell.api.run("material.add_material", self.file, name="Unknown")

        for thickness in range(1, 501):
            self.create_layer_type("IfcWallType", "Wall_" + str(thickness).zfill(4), thickness / 1000)

        self.file.write(get_path("IFC4 Wall Library.ifc"))

    def create_layer_type(self, ifc_class, name, thickness):
        element = ifcopenshell.api.run("root.create_entity", self.file, ifc_class=ifc_class, name=name)
        rel = ifcopenshell.api.run("material.assign_material", self.file, product=element, type="IfcMaterialLayerSet")
        layer_set = rel.RelatingMaterial
        layer = ifcopenshell.api.run("material.add_layer", self.file, layer_set=layer_set, material=self.material)
        layer.LayerThickness = thickness
        ifcopenshell.api.run("project.assign_declaration", self.file, definition=element, relating_context=self.library)
        return element


def get_path(filename):
    import bpy
    from pathlib import Path
    folder = Path(bpy.data.filepath).parent
    return str(folder / filename)


if __name__ == "__main__":
    LibraryGenerator().generate()

   
   
   
   
    
"""    
    
    
    
    
    
#get_wall_library()

#get_library()
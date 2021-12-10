
import requests
from bs4 import BeautifulSoup
import pandas as pd
import bpy
import mathutils
from itertools import repeat


#initialize requests and beatifulsoup
wiki_url = "https://nl.wikipedia.org/wiki/Lijst_van_baksteenformaten"
response = requests.get(url=wiki_url,)
soup = BeautifulSoup(response.text, 'html.parser')

#find title and heading
title = soup.find(id="firstHeading")

#use beautifulsoup to parse table and pass it into pandas module
brick_table = soup.find_all("table",{"class":"wikitable sortable"})


df = pd.read_html(str(brick_table))
df = pd.concat(df)

#(1 tm1 1) Belgische formaten
no_index = 11


formaat = (df.iloc[no_index].Formaat)
breedte = (df.iloc[no_index].Breedte)
hoogte = (df.iloc[no_index].Hoogte)
lengte = (df.iloc[no_index].Lengte)


name_collection =  "wiki_brick"
name_object = str(formaat)
name_mesh = str(formaat)


def add_brick(head_joint, bed_joint, brick_length, brick_width, brick_thickness):
    
    scale_factor = 1000
    
    mesh_name = name_mesh + "_"   + str(brick_width) + "x" + str(brick_length) + "x" + str(brick_thickness)
    collection_name = bpy.data.collections.new(name_collection)
    bpy.context.scene.collection.children.link(collection_name)
    
    vertices_whole_brick = [  (0,0,0),
                        (0,brick_width/scale_factor,0),
                        (brick_length/scale_factor,brick_width/scale_factor,0),
                        (brick_length/scale_factor,0,0),
                        
                        (0,0,brick_thickness/scale_factor),
                        (0,brick_width/scale_factor,brick_thickness/scale_factor),
                        (brick_length/scale_factor,brick_width/scale_factor,brick_thickness/scale_factor),
                        (brick_length/scale_factor,0,brick_thickness/scale_factor)
                        ]

    edges_whole_brick = []

    faces_whole_brick = [(0,1,2,3),
             (4,5,6,7),
             (0,4,5,1), 
             (1,5,6,2),
             (2,6,7,3),
             (3,7,4,0)
             ]

    new_mesh = bpy.data.meshes.new(name_mesh)
    new_mesh.from_pydata(vertices_whole_brick, edges_whole_brick, faces_whole_brick)
    
    
    new_mesh.update()
    
    new_object = bpy.data.objects.new(mesh_name, new_mesh)
    
    """
    
    (new_object.data.vertices[0].co) = (0,0,0)
    (new_object.data.vertices[1].co) = (0,brick_width/scale_factor,0)
    (new_object.data.vertices[2].co) = (brick_length/scale_factor,brick_width/scale_factor,0)
    (new_object.data.vertices[3].co) = (brick_length/scale_factor,0,0)
    
    (new_object.data.vertices[4].co) = (0,0,brick_thickness/scale_factor)
    (new_object.data.vertices[5].co) = (0,brick_width/scale_factor,brick_thickness/scale_factor)
    (new_object.data.vertices[6].co) = (brick_length/scale_factor,brick_width/scale_factor,brick_thickness/scale_factor)
    (new_object.data.vertices[7].co) = (brick_length/scale_factor,0,brick_thickness/scale_factor)
    
    """
    
    collection_name.objects.link(new_object)
    


def remove_brick_collection():
    
    bpy.ops.object.select_all(action='DESELECT')
    
    if (bool(bpy.data.collections.get(name_collection))) == True:
      
        collection = bpy.data.collections.get(name_collection)
        bpy.data.collections.remove(collection)
        
    else:
        print ("no collection found")
        
        
remove_brick_collection()   
     
add_brick(  head_joint=0.01, 
            bed_joint=0.01,
            brick_length=(lengte), 
            brick_width=(breedte),
            brick_thickness=(hoogte)
            )
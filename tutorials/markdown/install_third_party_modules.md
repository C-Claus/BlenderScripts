# Getting data from Wikipedia to create geometry with Blender

This script shows how one is able to install third party modules in Blender to eventually create geometry from wikipedia data. The final result is a brick wall with data harvest from wikipedia.

## Script to install third-party modules in Blender's Python on Windows 10

In this example a webcrawler is used to harvest brick dimensions from a wikipedia table. These dimensions are used in Blender to create brick walls made from different brick sizes. Third-party modules in the bundled Python folder need to be installed.

The modules needed are:
 - beautifulsoup4
 - pandas
 - lxml



## 1. Run Blender in Administrator Mode 

![Adminstrator_Blender](https://github.com/C-Claus/02_Blender_Python_scripts/blob/master/tutorials/images/00_run_as_adminstrator.png)



## 2. Copy paste this in the scripting module of Blender

In the scripting module of Blender, use the following script. This script installs the modules in the python Blender folder.

```python
import subprocess
import bpy

py_exec = bpy.app.binary_path_python

# ensure pip is installed & update
subprocess.call([str(py_exec), "-m", "ensurepip", "--user"])
subprocess.call([str(py_exec), "-m", "pip", "install", "--upgrade", "pip"])

# install dependencies using pip
subprocess.call([str(py_exec),"-m", "pip", "install", "--user", "beautifulsoup4"])
subprocess.call([str(py_exec),"-m", "pip", "install", "--user", "pandas"])
subprocess.call([str(py_exec),"-m", "pip", "install", "--user", "lxml"])
```
Under Window -> Toggle System Console to see the Python output.


## 3. Restart Blender

Restart Blender, in the following script the URL https://nl.wikipedia.org/wiki/Lijst_van_baksteenformaten is used to parse data from wikipedia tables.
This script uses the modules beautifulsoup and pandas to get one type of brick dimensions from wikipedia.

```python

import requests
from bs4 import BeautifulSoup
import pandas as pd

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

formaat = (df.iloc[5].Formaat)
breedte = (df.iloc[5].Breedte)
hoogte = (df.iloc[5].Hoogte)
lengte = (df.iloc[5].Lengte)

```


Run this script and Blender console will give back the data from wikipedia to the console for one brick, the Charleroi brick. Because it's fifth in the table.


```python
100
Charleroi
100
65
210
```
or use ```python print df``` to see the entire output:

![Console_Blender](https://github.com/C-Claus/02_Blender_Python_scripts/blob/master/tutorials/images/console_blender.png)

# Creating the geometry

From these values a simple mesh geometry in Blender is constructed. In this function we can use the data we just collected from Wikipedia.

```python
name_collection =  "brick_collection"
name_object = str(formaat)
name_mesh = str(formaat)


def add_brick(head_joint, bed_joint, brick_length, brick_width, brick_thickness):
    
    scale_factor = 1000
    
    mesh_name = name_mesh + "_"   + str((brick_width/scale_factor)) + "x" + str((brick_length/scale_factor)) + "x" + str((brick_thickness/scale_factor))
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
    collection_name.objects.link(new_object)
```

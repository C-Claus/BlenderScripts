

## Script to install third-party modules in Blender's Python on Windows 10

In this example a webcrawler is used to harvest brick dimensions from a wikipedia table. These dimensions are used in Blender to create brick walls made from different brick sizes. Before be able to webcrawl from Blender we need to install third-party modules in the bundled Python folder which comes with installing Blender.

The modules needed are:
 - beautifulsoup4
 - pandas
 - lxml



## 1. Run Blender in Administrator Mode 

![Adminstrator_Blender](https://github.com/C-Claus/02_Blender_Python_scripts/blob/master/tutorials/images/00_run_as_adminstrator.png)



## 2. Copy paste this in the scripting module of Blender

In the scripting module of Blender, use the following script. 

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
or use ```ptyhon print df``` to see the entire output:

![Console_Blender](https://github.com/C-Claus/02_Blender_Python_scripts/blob/master/tutorials/images/console_blender.png)


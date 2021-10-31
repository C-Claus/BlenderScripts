

## Script to install third-party modules in Blender's Python on Windows 10

In this example a webcrawler is used to harvest brick dimensions from a wikipedia table. These dimensions are used in Blender to create brick walls made from different brick sizes. Before be able to webcrawl from Blender we need to install third-party modules in the bundled Python folder which comes with installing Blender.

The modules needed are:
 - beautifulsoup4
 - pandas
 - lxml



## 1. Run Blender in Administrator Mode 




## 2. Copy paste this in the script module of Blender

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

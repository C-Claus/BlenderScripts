

## Script to install third-party modules in Blender's Python on Windows 10

## Run Blender in Administrator Mode 


## Copy paste this in the script module of Blender

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

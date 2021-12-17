#BlenderBIM Excel

#Summary
This is a proof of concept Python script which explores the possibilities of extracting useful information from an IFC. 
The information is exported to Excel. The end user uses MS Excel to make filters. These filters can be applied 
in the BlenderBIM add-on to highlight the filtered IFC elements.

#Dependencies & set up instructions (Tested on Windows 10)
- Blender
- BlenderBIM add-on 
- ifcopenshell
- xlsxwriter
- openpyxl

To install the modules in Blender navigate to

```C:\Program Files\Blender Foundation\Blender 2.93\2.93\python\Scripts```

open Command Prompt and type:

```pip install xlsxwriter```

```pip install openpyxl```

The ```ifcopenshell``` modules comes when you install the BlenderBIM add-on.


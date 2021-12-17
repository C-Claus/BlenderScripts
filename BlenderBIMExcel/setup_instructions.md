# BlenderBIM Excel

# Summary
This is a proof of concept Python script which explores the possibilities of extracting useful information from an IFC. 
The information is exported to Excel. The end user uses MS Excel to make filters. These filters can be applied 
in the BlenderBIM add-on to highlight the filtered IFC elements.

# Dependencies & set up instructions (Tested on Windows 10)
- Blender 2.93
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


Importing an existing IFC using the BlenderBIM add-on:

![image](https://user-images.githubusercontent.com/14906760/146614060-0ffc6d3d-1b91-4da8-b971-870417135abf.png)


The function ```#write_to_excel_from_ifc(ifc_file=IfcStore.path, excel_file=excel_file_path)``` opens the IFC file and writes the IFC information to Excel and opens Excel for you.
The Excel file is saved in the same location as where you saved your .ifc file.

![image](https://user-images.githubusercontent.com/14906760/146614294-44158ef5-2cdc-4c81-bb81-718958c636fd.png)

The IFC data is presented in tabular data. The IfcBuildingStorey is instantiated for each IfcGuid so the filter functionality in Excel is useful.
The IfcGuid is used to filter to show the elements in the BlenderBIM add-on.

We can filter on the following items in Excel: ```IfcWall```, ```IfcWallStandardCase```, ```00 begane grond``` and ```binnenblad``` 
It gives us the following result:

![image](https://user-images.githubusercontent.com/14906760/146614606-a71da7ca-78c9-4dca-85d0-777d6a582650.png)

Now saving the Excel file and calling the function

```select_IFC_elements_in_blender(guid_list=get_filtered_data_from_excel(excel_file=excel_file_path), excel_file=excel_file_path)```

Makes all the elements visible in Blender

# BlenderBIM Excel

# Summary
This is a proof of concept Python script which explores the possibilities of extracting useful information from an IFC. 
The information is exported to Excel. The end user uses MS Excel to make filters. These filters can be applied 
in the BlenderBIM add-on to highlight the filtered IFC elements.

# Why does this script exist?
IFC is a very useful open standard for exchanging Building Information. BlenderBIM is an open source add-on which is able to modify, read and update IFC files.
MS Excel is a widely used spreadsheet program. The idea is to bundle the possibilities of MS Excel with BlenderBIM add-on . This way the end user can experience a fast workflow to do the following tasks:
- Checking IFC according to the IDM
- Creating schedules in Excel from IFC
- Writing back data from Excel to IFC

# Dependencies & set up instructions (Tested on Windows 10)

Software/dependency | Version 
------------ | ------------- 
Blender | 2.93
BlenderBIM add-on | 0.0.211117
ifcopenshell | 
xlsxwriter |
openpyxl | 

To install the modules in Blender navigate to

```C:\Program Files\Blender Foundation\Blender 2.93\2.93\python\Scripts```

open Command Prompt and type:

```pip install xlsxwriter```

```pip install openpyxl```

The ```ifcopenshell``` modules comes when you install the BlenderBIM add-on.


Importing an existing IFC using the BlenderBIM add-on:

![image](https://user-images.githubusercontent.com/14906760/146614060-0ffc6d3d-1b91-4da8-b971-870417135abf.png)


The function ```write_to_excel_from_ifc(ifc_file=IfcStore.path, excel_file=excel_file_path)``` opens the IFC file and writes the IFC information to Excel and opens Excel for you.
The Excel file is saved in the same location as where you saved your .ifc file.

![image](https://user-images.githubusercontent.com/14906760/146614294-44158ef5-2cdc-4c81-bb81-718958c636fd.png)

The IFC data is presented in tabular data. The IfcBuildingStorey is instantiated for each IfcGuid so the filter functionality in Excel is useful.
The IfcGuid is used to filter to show the elements in the BlenderBIM add-on.

We can filter on the following items in Excel: ```IfcWall```, ```IfcWallStandardCase```, ```00 begane grond``` and ```binnenblad``` 
It gives us the following result:

![image](https://user-images.githubusercontent.com/14906760/146614606-a71da7ca-78c9-4dca-85d0-777d6a582650.png)

Now saving the Excel file and calling the function

```select_IFC_elements_in_blender(guid_list=get_filtered_data_from_excel(excel_file=excel_file_path), excel_file=excel_file_path)```

Makes all the filtered Excel elements visible in Blender:

![image](https://user-images.githubusercontent.com/14906760/146614951-1e27494a-d287-4d6c-8afd-c544d1177215.png)

Now we see all ```03 Metselwerk - kalkzandsteen C``` on the IfcBuildingStorey called  ```00 begane grond```. if we want to see all ```03 Metselwerk - kalkzandsteen C``` on each IfcBuildingStorey we can just easily filter it in Excel and call the function again, don't forget to save the Excel file!:

```select_IFC_elements_in_blender(guid_list=get_filtered_data_from_excel(excel_file=excel_file_path), excel_file=excel_file_path)```

![image](https://user-images.githubusercontent.com/14906760/146615667-3f195607-5122-4846-aa95-e05dc6bf446d.png)

If we want to make everything visible again we can call the following function:

```unhide_all()```

![image](https://user-images.githubusercontent.com/14906760/146615769-679d0b2d-5227-4d48-a3f6-aec06deed651.png)

So we can make every Excel filter combination visible in Blender, which could also be used for an animated timeline of the construction:

![image](https://user-images.githubusercontent.com/14906760/146639418-2e6db32c-5eb2-492a-b404-a3a74ac1daa6.png)

![image](https://user-images.githubusercontent.com/14906760/146639280-f48ef78d-9a75-46a5-8c95-3e070d0d5a89.png)

![image](https://user-images.githubusercontent.com/14906760/146639390-225b9586-d20c-45fd-af02-93a5d1a4c7d7.png)


Future work for this script:
- adding a Graphical User Interface which allows the end-user control over what they want to export to MS Excel.
- adding a column in MS excel for user defined parameters which can be written back to IFC.






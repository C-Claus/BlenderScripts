## BlenderBIM Open Office XML

BlenderBIM Open Office XML is a Blender add-on which creates [Open Office XML files](https://en.wikipedia.org/wiki/Office_Open_XML) from an IFC file using the BlenderBIM add-on. 

Open Open Office XML and [IFC](https://www.buildingsmart.org/standards/bsi-standards/industry-foundation-classes/) are both open file formats. Open Office XML can be used for the creation of spreadsheets which can be read by either Microsoft Excel or LibreOffice for example.
IFC is an open format widely used for BIM interoperability in the construction industry. 

### What's the added value of this Blender add-on?
The add-on enables architects, contractors and other stakeholders to do the following
- Easily quantify an .ifc file. 
- Makes it possible to visualize IFC elements from a filtered spreadsheet.
- Check an .ifc file if it's modelled conform the [BIM Base IDS](https://www.bimloket.nl//documents/BIM-ILS_infographicA4_2020_UK_021.pdf)

## Quickstart
### 1. Open an .ifc file and check what you would like to export and click the button 'Write IFC data to .xlsx'. It writes each IFC element to a row.  
In this example I used this freely available sample [model](https://github.com/jakob-beetz/DataSetSchependomlaan).

![alt text](https://github.com/C-Claus/BlenderScripts/blob/master/BlenderBIMOpenOfficeXML/images/00_Blender.png)

### 2. Filter the file using LibreOffice or Microsoft Excel and save it.

The filtered spreadsheet in [LibreOffice](https://www.libreoffice.org/)
![alt text](https://github.com/C-Claus/BlenderScripts/blob/master/BlenderBIMOpenOfficeXML/images/01_filtered_openoffice_libre.png)

The filtered spreadsheet in Microsoft Excel
![alt text](https://github.com/C-Claus/BlenderScripts/blob/master/BlenderBIMOpenOfficeXML/images/01_filtered_openoffice_excel.png)

### 3. Click the 'Filter IFC elements' button to show what you filtered.
Leave the saved spreadsheet open to show the IFC elements, with the button 'Open .xlsx file' it's possible to open previously exported IFC files which correspond with that IFC file.
![alt text](https://github.com/C-Claus/BlenderScripts/blob/master/BlenderBIMOpenOfficeXML/images/03_filtered_openoffice_libre_blender.png)






## Installation instructions & dependencies
### Dependencies

The BlenderBIM has been developed and tested with the following dependecies on Windows 10.

module/software | version
---- | -----
Blender | 2.93
blenderbim add-on | 0.211117
pandas | 1.3.5
xlsxwriter | 3.0.2
openpyxl | 3.0.9
ifcopenshell | comes with the BlenderBIM add-on

### Installation on Windows
With the installation of Blender on your system it comes with Python installed.
Navigate to where you have Blender installed, normally this is:

```C:\Program Files\Blender Foundation\Blender 2.93\2.93\python\Scripts```

Open Command Prompt by typing ```cmd``` in the Windows Explorer.

![alt_text](https://github.com/C-Claus/BlenderScripts/blob/master/BlenderBIMOpenOfficeXML/images/04_command_promt.png)

Type in the following commands in Command Prompt to download and install the dependencies. 

```pip install pandas```

```pip install xlsxwriter```

```pip install openpyxl```

### Installation on Linux

## How to use the BlenderBIMOpenOfficeXML add-on in detail


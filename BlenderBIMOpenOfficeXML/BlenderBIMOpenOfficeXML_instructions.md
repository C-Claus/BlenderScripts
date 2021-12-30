## BlenderBIM Open Office XML

BlenderBIM Open Office XML is a Blender add-on which creates [Open Office XML files](https://en.wikipedia.org/wiki/Office_Open_XML) from an IFC file using the [BlenderBIM add-on.](https://blenderbim.org/) 

Open Open Office XML and [IFC](https://www.buildingsmart.org/standards/bsi-standards/industry-foundation-classes/) are both open file formats. Open Office XML can be used for the creation of spreadsheets which can be read by either Microsoft Excel or LibreOffice for example.
IFC is an open format widely used for BIM interoperability in the construction industry. 

### What's the added value of this Blender add-on?
The add-on enables architects, contractors and other stakeholders to do the following
- Easily quantify an .ifc file. 
- Makes it possible to visualize IFC elements from a filtered spreadsheet.
- Check an .ifc file if it's modelled conform the [BIM Base IDS](https://www.bimloket.nl//documents/BIM-ILS_infographicA4_2020_UK_021.pdf)

## Quickstart
### 1. Import an .ifc file using the BlenderBIM add-on and check what you would like to export and click the button 'Write IFC data to .xlsx'. It writes each IFC element to a row.  
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
Blender | 2.93 & 3.0.0
blenderbim add-on | 0.211117
pandas | 1.3.5
xlsxwriter | 3.0.2
openpyxl | 3.0.9
ifcopenshell | comes with the BlenderBIM add-on


## Installation on Windows 10

### 1.  Open Blender as Administrator
![alt_text](https://github.com/C-Claus/BlenderScripts/blob/master/BlenderBIMOpenOfficeXML/images/00_install/00_run_blender_as_administrator.png)

### 2.  Open the scripting tab in Blender
![alt_text](https://github.com/C-Claus/BlenderScripts/blob/master/BlenderBIMOpenOfficeXML/images/00_install/01_open_Scripting_tab.png)

### 3.  Open the python file which installs the necessary modules, you can this python script [here](https://github.com/C-Claus/BlenderScripts/blob/master/BlenderBIMOpenOfficeXML/Blender_install_modules.py)
![alt_text](https://github.com/C-Claus/BlenderScripts/blob/master/BlenderBIMOpenOfficeXML/images/00_install/02_open_file.png)

### 4. Your Blender now should look like this
![alt_text](https://github.com/C-Claus/BlenderScripts/blob/master/BlenderBIMOpenOfficeXML/images/00_install/03_scripting_file_opened.png)

### 5. Toggle the System Console to see what the script is doing
![alt_text](https://github.com/C-Claus/BlenderScripts/blob/master/BlenderBIMOpenOfficeXML/images/00_install/04_toggle_the_system_console.png)


### 6. Run the script, the script downloads three modules from the internet which the add-on needs, [pandas](https://pandas.pydata.org/), [xlsxwriter](https://xlsxwriter.readthedocs.io/) [and openpyxl](https://openpyxl.readthedocs.io/en/stable/).
![alt_text](https://github.com/C-Claus/BlenderScripts/blob/master/BlenderBIMOpenOfficeXML/images/00_install/06_run_the_script_by_pressing_the_play_button.png)


### 7. Take a look at the System console to see if the downloads succeeded, if you get a ```PermissionError: [WinError5] Acces is denied``` it means Blender has no Administrator rights or you are using Blender from a user account. In my case I already installed the modules.
![alt_text](https://github.com/C-Claus/BlenderScripts/blob/master/BlenderBIMOpenOfficeXML/images/00_install/07_feedback_console.png)

### 8. Click on the Layout tab in Blender
![alt_text](https://github.com/C-Claus/BlenderScripts/blob/master/BlenderBIMOpenOfficeXML/images/00_install/08_click_on_the_layout_tab.png)

### 9. Go to Edit -> Preferences
![alt_text](https://github.com/C-Claus/BlenderScripts/blob/master/BlenderBIMOpenOfficeXML/images/00_install/09_go_to_edit_preferences.png)

### 10. Go to Add-ons -> Install
![alt_text](https://github.com/C-Claus/BlenderScripts/blob/master/BlenderBIMOpenOfficeXML/images/00_install/10_click_install.png)


### 11. Open the .zip file. You can find this zip file [here](https://github.com/C-Claus/BlenderScripts/blob/master/BlenderBIMOpenOfficeXML/BlenderBIMOpenOfficeXML.zip).
![alt_text](https://github.com/C-Claus/BlenderScripts/blob/master/BlenderBIMOpenOfficeXML/images/00_install/11_open_the_zip.png)

### 12. Search the Add-on and enabled it by checking it.
![alt_text](https://github.com/C-Claus/BlenderScripts/blob/master/BlenderBIMOpenOfficeXML/images/00_install/12_add_on_enabled.png)


### 13. Click ```N```, you should see the add-on under the ```Tools``` tab in Blender
![alt_text](https://github.com/C-Claus/BlenderScripts/blob/master/BlenderBIMOpenOfficeXML/images/00_install/13_under_the_tools_tab.png)

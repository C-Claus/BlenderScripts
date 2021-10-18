# Create and assign property set
import ifcopenshell 
import ifcopenshell.api


ifc_file = 'C:\\Algemeen\\07_prive\\00_BlenderBIM_IDM\\00_ifc\\brick_wall.ifc'
ifcfile = ifcopenshell.open(ifc_file)
products = ifcfile.by_type("IfcProduct")
owner_history = ifcfile.by_type("IfcOwnerHistory")[0]

walls=[]

for i in products:
    if i.is_a("IfcWall"):
        walls.append(i) 

property_values = [
    ifcfile.createIfcPropertySingleValue("Some Property Set Name ", "Some Property  Name", ifcfile.create_entity("IfcText", "Some Value"), None),
]   

for wall in walls:
    property_set = ifcfile.createIfcPropertySet(wall.GlobalId, owner_history, "Some Property Set Name ", None, property_values)
    ifcfile.createIfcRelDefinesByProperties(wall.GlobalId, owner_history, None, None, [wall], property_set)

ifcfile.write(ifc_file)  
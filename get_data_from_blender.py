import bpy
import csv
import os

outputFile = 'C:/Temp/0_IFCGuid_IFCMaterial.csv'
f = open(outputFile,'w')

for o in bpy.context.scene.objects:
    if o.type=='MESH':
    material = o.active_material.name
    global_id_index = o.BIMObjectProperties.attributes.find('GlobalId')
    guid = o.BIMObjectProperties.attributes[global_id_index].string_value
    print(guid)
    print(material)
    f.writelines(guid)
    f.writelines('\n')
    f.writelines(material)
    f.writelines('\n')
    f.close()
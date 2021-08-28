import csv
import bpy
import mathutils
from mathutils import Vector

def get_hea_data():
    
    hea_list = []

    with open("C:\\Algemeen\\07_prive\\02_Blender_Python_scripts\\hea.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        
        next(csv_reader, None) 
        
        for row in csv_reader:
            print (row)
            hea_list.append(row)
            
    return hea_list
          
          



def create_profile_HEA(profile_name, h,b,tw,tf):
    
    w = 1          
            
    cList = [       Vector((0,0,0)),
                    Vector((0,tf,0)),
                    Vector((b/2-tw,tf,0)),
                    Vector((b/2-tw,h-tf,0)),
                    Vector((0,h-tf,0)),    
                    Vector((0,h,0)), 
                    Vector((b,h,0)),
                    Vector((b,h-tf,0)),  
                    Vector((b/2+tw,h-tf,0)), 
                    Vector((b/2+tw,tf,0)),
                    Vector((b,tf,0)),
                    Vector((b,0,0)),
                    Vector((0,0,0))
                                       
                  ]          

    curvedata = bpy.data.curves.new(name='Curve', type='CURVE')
    curvedata.dimensions = '3D'

    objectdata = bpy.data.objects.new(profile_name, curvedata)
    objectdata.location = (0,0,0) 
   
    bpy.context.scene.collection.objects.link(objectdata)


    polyline = curvedata.splines.new('POLY')
    polyline.points.add(len(cList)-1)
    for num in range(len(cList)):
        x, y, z = cList[num]
        polyline.points[num].co = (x, y, z, w)
        
 
scale_factor = 1000
move_factor = 0

for i in get_hea_data():
    #print (i[0])      
    
    move_factor += 1
    #create_profile_HEA(profile_name='HEA'+str(i[0], h=96,b=100,tw=5,tf=8) 
    create_profile_HEA(profile_name=(  'HEA'+str(i[0])), 
                                        h=float(i[1])/scale_factor,
                                        b=float(i[2])/scale_factor,
                                        tw=float(i[3])/scale_factor,
                                        tf=float(i[4])/scale_factor)
                                        
                                        
                                        
    hea_profile = bpy.data.objects['HEA'+str(i[0])]
  
    vec = mathutils.Vector((move_factor, 0.0, 0.0))
    inv = hea_profile.matrix_world.copy()
    inv.invert()
 
    vec_rot = vec @ inv
    hea_profile.location = hea_profile.location + vec_rot
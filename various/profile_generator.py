import csv
import bpy
import mathutils
from mathutils import Vector
from math import sqrt 

def get_hea_data():
    
    hea_list = []

    with open("C:\\Algemeen\\07_prive\\02_Blender_Python_scripts\\hea.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        
        next(csv_reader, None) 
        
        for row in csv_reader:
            print (row)
            hea_list.append(row)
            
    return hea_list
          
r = 12         
c = sqrt(r**2+r**2)
m = (c-r)



coordinates = [
    ((-1, 0, 0), (-0.7, 0, 0), (-1, 0.5521, 0)),
    ((0, 1, 0), (-0.5521, 1, 0), (0, 0.7, 0)),
    ((0, 0, 0), (0, 0.3, 0), (-0.3, 0, 0))
]



def MakeCurveQuarter(objname, curvename, cList, ):    
    curvedata = bpy.data.curves.new(name=curvename, type='CURVE')    
    curvedata.dimensions = '2D'    
    
    objectdata = bpy.data.objects.new(objname, curvedata)    
    objectdata.location = (0,0,0)
    
   
    bpy.context.scene.collection.objects.link(objectdata)    
    
    polyline = curvedata.splines.new('BEZIER')    
    polyline.bezier_points.add(len(cList)-1)    

    for idx, (knot, h1, h2) in enumerate(cList):
        point = polyline.bezier_points[idx]
        point.co = knot
        point.handle_left = h1
        point.handle_right = h2
        point.handle_left_type = 'FREE'
        point.handle_right_type = 'FREE'

    polyline.use_cyclic_u = False    
    
MakeCurveQuarter("HOEK", "HOEK", coordinates)  



def create_profile_HEA(profile_name, h,b,tw,tf,r):
    
  
 
    #LINKERONDERHOEK
    linkeronderhoek = bpy.ops.curve.simple(align='WORLD', location=(b/2-tw-r,tf+r, 0), 
                                        rotation=(0, 0, -1.5708), 
                                        Simple_Type='Arc',
                                        Simple_radius=12,
                                        Simple_endangle=90,
                                        use_cyclic_u=False)
                                        
 
    #LINKERBOVENHOEK
    linkerbovenhoek = bpy.ops.curve.simple(align='WORLD',  location=(b/2-tw-r,h-tf, 0),
                                         rotation=(0, 0, -1.5708), 
                                         Simple_Type='Arc',
                                         Simple_radius=12,
                                         Simple_endangle=90,
                                         use_cyclic_u=False)
                                         
                                         
    rechterbovenhoek = bpy.ops.curve.simple(align='WORLD',  location=(b/2+tw,h-tf, 0),
                                         rotation=(0, 0, -1.5708*2), 
                                         Simple_Type='Arc',
                                         Simple_radius=12,
                                         Simple_endangle=90,
                                         use_cyclic_u=False)
                                         
    rechterbovenhoek = bpy.ops.curve.simple(align='WORLD',  location=(b/2+tw,tf+r, 0),
                                         rotation=(0, 0, -1.5708*3), 
                                         Simple_Type='Arc',
                                         Simple_radius=12,
                                         Simple_endangle=90,
                                         use_cyclic_u=False)
                                         
                                         


       
   
   
    
    w = 1     
    
    #r = 12         
    c = sqrt(r**2+r**2)
    m = (c-r)     
            
    cList = [       Vector((0,0,0)),
                    Vector((0,tf,0)),
                    
                    
                    #LINKERONDERHOEK FLENS LIJF
                    
                    Vector((b/2-tw-r,tf,0)),
                    #Vector((b/2-tw-m,tf+m,0)),
                    Vector((b/2-tw,tf+r,0)),
                    
     
                    #LINKERBOVENHOEK FLENS LIJF
                    Vector((b/2-tw,h-tf-r,0)),
                    Vector((b/2-tw-m,h-tf-m,0)),
                    Vector((b/2-tw-r,h-tf,0)),
                    
                    

                    Vector((0,h-tf,0)),    
                    Vector((0,h,0)), 
                    Vector((b,h,0)),
                    Vector((b,h-tf,0)),  
                    
               
                    #RECHTERBOVENHOEK FLENS LIJF
                    Vector((b/2+tw+r,h-tf,0)), 
                    Vector((b/2+tw+m,h-tf-m,0)), 
                    Vector((b/2+tw,h-tf-r,0)), 
                    
                    
                    #RECHTERONDERHOEK FLENS LIJF
                    Vector((b/2+tw,tf+r,0)),
                    Vector((b/2+tw+m,tf+m,0)),
                    Vector((b/2+tw+r,tf,0)),
                    
                    
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
        
#bpy.ops.curve.simple(align='WORLD', location=(33, 79.5147 , 0), rotation=(0, 0, 0), Simple_Type='Arc', use_cyclic_u=False)
        
#bpy.ops.curve.simple(align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), Simple_Type='Arc', Simple_endangle=90, use_cyclic_u=False)
     

#100;96;100;5;8;12;56;16.7;21.2;0.562;33.7 
#create_profile_HEA(profile_name='HEA100', h=96, b=100, tw=5, tf=8, r=12)       
 
 
def create_profiles_HEA():
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
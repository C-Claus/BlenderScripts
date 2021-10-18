import bpy    
from mathutils import Vector    


coordinates = [
    ((-1, 0, 0), (-0.7, 0, 0), (-1, 0.5521, 0)),
    ((0, 1, 0), (-0.5521, 1, 0), (0, 0.7, 0)),
    ((0, 0, 0), (0, 0.3, 0), (-0.3, 0, 0))
]

    
def MakeCurveQuarter(objname, curvename, cList, origin=(0,0,0)):    
    curvedata = bpy.data.curves.new(name=curvename, type='CURVE')    
    curvedata.dimensions = '2D'    
    
    objectdata = bpy.data.objects.new(objname, curvedata)    
    objectdata.location = origin
    
   
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

    polyline.use_cyclic_u = True    
    
MakeCurveQuarter("NameOfMyCurveObject", "NameOfMyCurve", coordinates)  
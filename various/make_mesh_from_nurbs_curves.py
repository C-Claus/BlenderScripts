
import bpy
from mathutils import Vector

surface_data = bpy.data.curves.new('wook', 'SURFACE')
surface_data.dimensions = '3D'

# 16 coordinates
points = [
    Vector((-1.5, -1.5, 0.0, 1.0)), Vector((-1.5, -0.5, 0.0, 1.0)),
    Vector((-1.5, 0.5, 0.0, 1.0)), Vector((-1.5, 1.5, 0.0, 1.0)),
    Vector((-0.5, -1.5, 0.0, 1.0)), Vector((-0.5, -0.5, 1.0, 1.0)),
    Vector((-0.5, 0.5, 1.0, 1.0)), Vector((-0.5, 1.5, 0.0, 1.0)),
    Vector((0.5, -1.5, 0.0, 1.0)), Vector((0.5, -0.5, 1.0, 1.0)),
    Vector((0.5, 0.5, 1.0, 1.0)), Vector((0.5, 1.5, 0.0, 1.0)),
    Vector((1.5, -1.5, 0.0, 1.0)), Vector((1.5, -0.5, 0.0, 1.0)),
    Vector((1.5, 0.5, 0.0, 1.0)), Vector((1.5, 1.5, 0.0, 1.0))
]

# set points per segments (U * V)
for i in range(0, 16, 4):
    spline = surface_data.splines.new(type='NURBS')
    spline.points.add(3)  # already has a default vector

    for p, new_co in zip(spline.points, points[i:i+4]):
        p.co = new_co

surface_object = bpy.data.objects.new('NURBS_OBJ', surface_data)
bpy.context.scene.collection.objects.link(surface_object)

splines = surface_object.data.splines
for s in splines:
    for p in s.points:
        p.select = True

bpy.context.view_layer.objects.active = surface_object
bpy.ops.object.mode_set(mode = 'EDIT') 
bpy.ops.curve.make_segment()

#bpy.context.scene.collection.objects.link(obj)
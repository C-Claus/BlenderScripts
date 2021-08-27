
import bpy
import mathutils

width = 1
height = 2

def set_path(width):
    
    print (width)
    
    bpy.data.objects['path'].dimensions[1] = width
    
set_path(width=width)



def create_window(width, height):
    
    
    #bovendorpel = bpy.data.objects['bovendorpel_114x67mm'].select_set(True)
    #onderdorpel = bpy.data.objects['onderdorpel_114x67mm'].select_set(True) 
    
    
    #bovendorpel.dimensions[0] = 0.7
    #bovendorpel.dimensions[1] = width
    
    #bpy.context.object.dimensions[0] = 0.7
    
    bpy.data.objects['bovendorpel_114x67mm'].dimensions[1] = width
    bpy.data.objects['onderdorpel_114x67mm'].dimensions[1] = width
    
    #bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    
    zijstijl = bpy.data.objects["zijstijl_144x67a"]
    vec = mathutils.Vector((0.0, int(width/2), 0.0))
    
    inv = zijstijl.matrix_world.copy()
    inv.invert()
    
    vec_rot = vec @ inv
    zijstijl.location = zijstijl.location + vec_rot
    
    print (zijstijl.location)
    
    
    
   
    
#create_window(width=width, height=height)
import bpy
import math
 
# mesh arrays
verts = []
faces = []
 
# mesh variables
numX = 10
numY = 10
 
# wave variables
freq = 1
amp = 1
scale = 1
 
#fill verts array
for i in range (0, numX):
    for j in range(0,numY):
 
        x = scale * i
        y = scale * j
        z = scale*((amp*math.cos(i*freq))+(amp*math.sin(j*freq)))
 
        vert = (x,y,z) 
        verts.append(vert)
 
#fill faces array
count = 0
for i in range (0, numY *(numX-1)):
    if count < numY-1:
        A = i
        B = i+1
        C = (i+numY)+1
        D = (i+numY)
 
        face = (A,B,C,D)
        faces.append(face)
        count = count + 1
    else:
        count = 0
 
#create mesh and object
mesh = bpy.data.meshes.new("wave")
object = bpy.data.objects.new("wave",mesh)
 
#set mesh location
object.location = bpy.context.scene.cursor.location
scene = bpy.context.scene
scene.collection.objects.link(object)
 
#create mesh from python data
mesh.from_pydata(verts,[],faces)
mesh.update(calc_edges=True)
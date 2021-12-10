import bpy
import bmesh
from mathutils import Vector

####################### START FROM EDITMODE

obj = bpy.context.object
me = obj.data
bm = bmesh.from_edit_mesh(me)

######################## SELECTION LISTS FROM VERTEX

Vset=[] # vertex path 

for f in bm.faces:
    if f.select == True:
        PROFILE = f  # FACE PROFILE     

for vert in bm.verts: # VERTEX PATH - VERTEX FACE
    if vert.select == True and not vert in PROFILE.verts:
        Vset.append(vert)
     
bpy.ops.mesh.select_all(action='DESELECT')

####################### DUPLICATE ALONG VERTEX PATH

for path_vert in Vset:
    
    nu_face = PROFILE.copy()
    nu_face.select=True

    VN = path_vert.normal; VN[2] = 0.0 
    VN.normalize()
    
    VP = path_vert.co
   
    for v in nu_face.verts:
           
        lx,lz = v.co.x,v.co.z # STORE VERTEX OFFSET ON ZX PLANE       
        v.co = (VP.x,VP.y,VP.z+lz) # MOVE PROFILE VERTS ON PATH VERT     
        v.co += lx * VN # SCALE VERTS ALONG XY NORMAL BY X OFFSET


###################### BRIDGE EM ALL      
Vset = [] 
for v in bm.verts:
    if v.select == True:
        Vset.append(v)   

bpy.ops.mesh.delete(type='ONLY_FACE')

for v in Vset: v.select = True

bpy.ops.mesh.select_mode(use_extend=True, use_expand=False, type='EDGE')      
bpy.ops.mesh.bridge_edge_loops()

bmesh.update_edit_mesh(me, True)   
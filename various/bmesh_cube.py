import bpy
import bmesh

bpyscene = bpy.context.scene
mesh_name = "Basic Cube" 
# Create an empty mesh and the object.
mesh = bpy.data.meshes.new(mesh_name)
basic_cube = bpy.data.objects.new(mesh_name, mesh)

# Add the object into the scene.
#bpyscene.objects.link(basic_cube)
bpy.context.collection.objects.link(basic_cube)
#new_collection.objects.link(basic_cube)



#bpyscene.objects.active = basic_cube
#basic_cube.select = True
obj = bpy.data.objects[mesh_name]
#obj = bpy.context.window.scene.objects[0]
#bpy.context.view_layer.objects.active = basic_cube
#obj.select_set(True) 


#odata = bpy.data.objects[mesh_name].data
#odata.edges[8].vertices[0] = 3
#odata.edges[8].vertices[1] = 5





# Construct the bmesh cube and assign it to the blender mesh.
bm = bmesh.new()
bmesh.ops.create_cube(bm, size=1.0)
bm.to_mesh(mesh)
bm.free()


#bm.to_mesh(me)
#bm.free()
#odata.update()
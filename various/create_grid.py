import bpy

# Settings
name = 'Gridtastic'
rows = 5
columns = 10
size = 1

# Utility functions
def vert(column, row):
    """ Create a single vert """

    return (column * size, row * size, 0)


def face(column, row):
    """ Create a single face """

    return (column* rows + row,
           (column + 1) * rows + row,
           (column + 1) * rows + 1 + row,
           column * rows + 1 + row)

# Looping to create the grid
verts = [vert(x, y) for x in range(columns) for y in range(rows)]
faces = [face(x, y) for x in range(columns - 1) for y in range(rows - 1)]

# Create Mesh Datablock
mesh = bpy.data.meshes.new(name)
mesh.from_pydata(verts, [], faces)

# Create Object and link to scene
obj = bpy.data.objects.new(name, mesh)
bpy.context.scene.collection.objects.link(obj)

# Select the object
bpy.context.view_layer.objects.active = obj
obj.select = True
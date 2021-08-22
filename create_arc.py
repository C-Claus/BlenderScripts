bl_info = {
    "name": "Circular Arc",
    "author": "batFINGER",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > Circular Arc",
    "description": "Adds a mesh circumcircle given base and height",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}


import bpy
import bmesh
from mathutils import Matrix
from math import asin
from bpy_extras.object_utils import AddObjectHelper

from bpy.props import (
    IntProperty,
    BoolProperty,
    FloatProperty,
)


class MESH_OT_primitive_arc_add(AddObjectHelper, bpy.types.Operator):
    """Add a simple arc mesh"""
    bl_idname = "mesh.primitive_arc_add"
    bl_label = "Add Circular Arc"
    bl_options = {'REGISTER', 'UNDO'}

    length: FloatProperty(
        name="length",
        description="Chord Length",
        min=0.01,
        max=100.0,
        default=2.0,
        unit='LENGTH',
    )
    height: FloatProperty(
        name="Height",
        description="Arc Height",
        min=0.01,
        max=100.0,
        unit='LENGTH',
        default=1.0,
    )
    segments: IntProperty(
        name="Arc Segments",
        description="Number of Segments",
        min=1,
        default=8,
    )

    def draw(self, context):
        '''Generic Draw'''
        layout = self.layout
        # annnotated on this class
        for prop in self.__class__.__annotations__.keys():
            layout.prop(self, prop)
        # annotated on AddObjectHelper
        for prop in AddObjectHelper.__annotations__.keys():
            layout.prop(self, prop)


    def execute(self, context):
        h = self.height
        a = self.length / 2
        r = (a * a + h * h) / (2 * h)
        if abs(a / r) > 1:
            # math domain error on arcsin
            return {'CANCELLED'}
        angle = 2 * asin(a / r)

        mesh = bpy.data.meshes.new("Arc")

        bm = bmesh.new()
        v = bm.verts.new((0, r, 0))
        bmesh.ops.rotate(
            bm, verts=[v], matrix=Matrix.Rotation(angle / 2, 3, 'Z'))
        bmesh.ops.spin(
            bm,
            geom=[v],
            axis=(0, 0, 1),
            steps=self.segments,
            angle=-angle,
        )

        for v in bm.verts:
            v.co.y -= r - h
            v.select = True
        bm.to_mesh(mesh)
        #mesh.update()

        # add the mesh as an object into the scene with this utility module
        from bpy_extras import object_utils
        object_utils.object_data_add(context, mesh, operator=self)

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(MESH_OT_primitive_arc_add.bl_idname, icon='MESH_CUBE')


def register():
    bpy.utils.register_class(MESH_OT_primitive_arc_add)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(MESH_OT_primitive_arc_add)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.mesh.primitive_arc_add()
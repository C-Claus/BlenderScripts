
import bpy


#bpy.ops.object.hide_view_clear()
#bpy.ops.object.select_all(action='DESELECT')
bpy.data.objects.foreach_set("hide_viewport", (True,) * len(bpy.ops.bim.select_ifc_class(ifc_class="IfcWindow")))
#

bpy.ops.object.hide_view_set(unselected=True)
#bpy.data.collections["Collection"].hide_viewport = True





#bpy.ops.object.hide_view_clear()


#bpy.ops.object.select_all(action='DESELECT')

#bpy.ops.bim.select_ifc_class(ifc_class="IfcBeam")

#bpy.ops.object.hide_view_set(unselected=True)






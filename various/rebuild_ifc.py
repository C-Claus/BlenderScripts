import bpy
from blenderbim.bim.ifc import IfcStore
from blenderbim.bim.handler import purge_module_data
from ifcopenshell.api.void.data import Data as VoidData
from ifcopenshell.api.context.data import Data as ContextData
from ifcopenshell.api.aggregate.data import Data as AggregateData
from ifcopenshell.api.geometry.data import Data as GeometryData


def get_body_context_id():
    if not ContextData.is_loaded:
        ContextData.load(IfcStore.get_file())
    for context in ContextData.contexts.values():
        for subcontext_id, subcontext in context["HasSubContexts"].items():
            if subcontext["ContextType"] == "Model" and subcontext["ContextIdentifier"] == "Body":
                return subcontext_id


def reset_file():
    for o in bpy.data.objects:
        if o.type in {'MESH', 'EMPTY'}:
            o.BIMObjectProperties.ifc_definition_id = 0
            if o.data:
                o.data.BIMMeshProperties.ifc_definition_id = 0
    for m in bpy.data.materials:
        m.BIMMaterialProperties.ifc_style_id = False
    bpy.context.scene.BIMProperties.ifc_file = ""
    IfcStore.purge()
    purge_module_data()


def assign_classes(objs):
    body_context_id = get_body_context_id()
    if not body_context_id:
        return
    for o in objs:
        if o.name.startswith("Ifc"):
            ifc_class = o.name.split("/")[0]
            o.name = "/".join(o.name.split("/")[1:])
            ctx = {"selected_objects": [o]}
            args = {
                "ifc_class": ifc_class,
                "context_id": body_context_id
            }
            bpy.ops.bim.assign_class(ctx, **args)


reset_file()
bpy.ops.bim.create_project()
assign_classes(bpy.data.objects)



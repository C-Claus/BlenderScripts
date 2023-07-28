
#user interface mutable versus immutable
import bpy
import blenderbim.tool as tool
#immutable
#>can’t change the object’s state after you’ve created it. 

#mutable
#>a mutable object allows you to modify its internal state after creation


class ReloadIfcFile(bpy.types.Operator, tool.Ifc.Operator):
    bl_idname = "bim.reload_ifc_file"
    bl_label = "Reload IFC File"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Reload an updated IFC file"
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    filter_glob: bpy.props.StringProperty(default="*.ifc", options={"HIDDEN"})

    def _execute(self, context):
        import ifcdiff

        old = tool.Ifc.get()
        new = ifcopenshell.open(self.filepath)

        ifc_diff = ifcdiff.IfcDiff(old, new, relationships=[])
        ifc_diff.diff()

        changed_elements = set([k for k, v in ifc_diff.change_register.items() if "geometry_changed" in v])

        for global_id in ifc_diff.deleted_elements | changed_elements:
            element = tool.Ifc.get().by_guid(global_id)
            obj = tool.Ifc.get_object(element)
            if obj:
                bpy.data.objects.remove(obj)

        # STEP IDs may change, but we assume the GlobalID to be constant
        obj_map = {}
        for obj in bpy.data.objects:
            element = tool.Ifc.get_entity(obj)
            if element and hasattr(element, "GlobalId"):
                obj_map[obj.name] = element.GlobalId

        delta_elements = [new.by_guid(global_id) for global_id in ifc_diff.added_elements | changed_elements]
        tool.Ifc.set(new)

        for obj in bpy.data.objects:
            global_id = obj_map.get(obj.name)
            if global_id:
                try:
                    tool.Ifc.link(new.by_guid(global_id), obj)
                except:
                    # Still prototyping, so things like types definitely won't work
                    print("Could not relink", obj)

        start = time.time()
        logger = logging.getLogger("ImportIFC")
        path_log = os.path.join(context.scene.BIMProperties.data_dir, "process.log")
        if not os.access(context.scene.BIMProperties.data_dir, os.W_OK):
            path_log = os.path.join(tempfile.mkdtemp(), "process.log")
        logging.basicConfig(
            filename=path_log,
            filemode="a",
            level=logging.DEBUG,
        )
        settings = import_ifc.IfcImportSettings.factory(context, self.filepath, logger)
        settings.has_filter = True
        settings.should_filter_spatial_elements = False
        settings.elements = delta_elements
        settings.logger.info("Starting import")
        ifc_importer = import_ifc.IfcImporter(settings)
        ifc_importer.execute()
        settings.logger.info("Import finished in {:.2f} seconds".format(time.time() - start))
        print("Import finished in {:.2f} seconds".format(time.time() - start))

        context.scene.BIMProperties.ifc_file = self.filepath
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}
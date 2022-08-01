import ifcopenshell

ifc_file = ifcopenshell.open("C:\\Algemeen\\07_prive\\BlenderScripts\\BlenderBIMLibrary\\IFC4 Demo Library.ifc")


print (ifc_file)

wall_types = ifc_file.by_type("IfcWallType")

for wall_type in wall_types:
    #print ((wall_type))
    #print ((wall_type.ApplicableOccurrence))
    #print ((wall_type.Decomposes))
    #print ((wall_type.Description))
    #print ((wall_type.ElementType))
    #print ((wall_type.GlobalId))
    #print ((wall_type.HasAssignments))
    if ((wall_type.HasAssociations)):
        for has_associations in wall_type.HasAssociations:
            #print (has_associations)
            if has_associations.is_a("IfcRelAssociatesMaterial"):
                #'Description', 'GlobalId', 'Name', 'OwnerHistory', 'RelatedObjects', 'RelatingMaterial',
                if has_associations.RelatingMaterial.is_a("IfcMaterialLayerSet"):
                    #'AssociatedTo', 'Description', 'HasExternalReferences', 'HasProperties', 'LayerSetName', 'MaterialLayers'
                    for material_layer in (has_associations.RelatingMaterial.MaterialLayers):
                        #'AssociatedTo', 'Category', 'Description', 'HasExternalReferences', 'HasProperties', 'IsVentilated', 'LayerThickness', 'Material', 'Name', 'Priority', 'ToMaterialLayerSet',
                        print (material_layer.Material)
                        print (material_layer.LayerThickness)


"""
['ApplicableOccurrence',
'Decomposes', 
'Description', 
'ElementType', 
'GlobalId',
'HasAssignments',
'HasAssociations', 
'HasContext',
'HasPropertySets',
'IsDecomposedBy',
'IsNestedBy', 
'Name',
'Nests',
'OwnerHistory', 
'PredefinedType',
'ReferencedBy',
'RepresentationMaps',
'Tag',
'Types',

"""


library = ifc_file.by_type("IfcProjectLibrary")

for i in library:

    print (i.Name)

    """
    ['Declares', 
    'Decomposes',
    'Description',
    'GlobalId', 
    'HasAssignments', 
    'HasAssociations',
    'HasContext', 
    'IsDecomposedBy',
    'IsDefinedBy',
    'IsNestedBy',
    'LongName', 
    'Name', 
    'Nests', 
    'ObjectType',
    'OwnerHistory',
    'Phase', 
    'RepresentationContexts'
    , 'UnitsInContext', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'attribute_name', 'attribute_type', 'get_info', 'get_info_2', 'id', 
    '   is_a', 'unwrap_value', 'walk', 'wrap_value']
    
    """
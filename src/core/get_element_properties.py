import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.attribute
import ifcopenshell.util.element
import ifcopenshell.util.resource


def get_element_properties(element:ifcopenshell.sqlite_entity):
    psets_and_qtos = ifcopenshell.util.element.get_psets(
        element = element,
        psets_only = True,
        should_inherit=True,
        verbose = True
        )
    attributes = element.get_info(
        include_identifier = True,
        recursive = False,
        scalar_only = True)
    # materials = ifcopenshell.util.element.get_material(element,True,False)
    # spatial_container = ifcopenshell.util.element.get_contained(element)
    # quantity_sets = ifcopenshell.util.element.get_quantities([element], True)
    # type_info = ifcopenshell.util.element.get_type(element)
    # predefined_type = ifcopenshell.util.element.get_predefined_type(element)



    details = {
        'id': int(element.id()) if element.id() is not None else None,
        'type': str(element.is_a()) if element.is_a() is not None else 'Unknown',
        'name': str(element.Name) if hasattr(element, 'Name') and element.Name is not None else None,
        'global_id': element.GlobalId,
        'psets': psets_and_qtos,
        "attributes": attributes,
    }



    return details
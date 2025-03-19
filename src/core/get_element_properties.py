import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.attribute
import ifcopenshell.util.element
import ifcopenshell.util.resource


def get_element_properties(element:ifcopenshell.sqlite_entity):
    psets_and_qtos = ifcopenshell.util.element.get_psets(element)
    attributes = element.get_info()
    materials = ifcopenshell.util.element.get_material(element,True,True)
    spatial_container = ifcopenshell.util.element.get_container(element)
    quantity_sets = ifcopenshell.util.element.get_quantities([element], verbose=True)
    # type_info = ifcopenshell.util.element.get_type(element)
    # predefined_type = ifcopenshell.util.element.get_predefined_type(element)


    psets = {
        'all': psets_and_qtos,
    }
    details = {
        'id': int(element.id()) if element.id() is not None else None,
        'type': str(element.is_a()) if element.is_a() is not None else 'Unknown',
        'name': str(element.Name) if hasattr(element, 'Name') and element.Name is not None else None,
        'global_id': element.GlobalId,
        'psets': psets
    }


    return details
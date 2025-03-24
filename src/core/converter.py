import multiprocessing

import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.attribute
import ifcopenshell.util.element
import ifcopenshell.util.resource


def load_ifc_model(ifc_path):
    try:
        print("IFC file loading...")
        ifc_model = ifcopenshell.open(ifc_path)
        print(f"IFC file loaded. Schema version: {ifc_model.schema}")
        return ifc_model
    except Exception as e:
        print(f"Error: Failed to load IFC file. {e}")
        return None
    
def get_geometry_settings():
    geo_settings = ifcopenshell.geom.settings()
    geo_settings.set("dimensionality", ifcopenshell.ifcopenshell_wrapper.SURFACES_AND_SOLIDS)
    geo_settings.set("unify-shapes", True)
    geo_settings.set("use-world-coords", True)
    geo_settings.set("apply-default-materials", True)
    geo_settings.set("no-normals", False)
    geo_settings.set("disable-opening-subtractions", False)
    geo_settings.set("weld-vertices", True)
    return geo_settings

def create_iterator(settings, ifc_model):
    return ifcopenshell.geom.iterator(settings, ifc_model, multiprocessing.cpu_count())

def get_element_details(element:ifcopenshell.sqlite_entity):
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
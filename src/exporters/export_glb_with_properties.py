from typing import List

import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.shape

from core.build_geometry_data_by_material import \
    build_geometry_data_by_material
from core.converter import get_geometry_settings
from core.get_element_properties import get_element_properties
from types_def.geometry import GeometryData
from types_def.ifc import IfcModel


def export_glb_with_properties(ifc_model:IfcModel):
  try:
    if not ifc_model:
        return False
    geo_settings = get_geometry_settings()
    
    elements = ifc_model.by_type("IfcProduct")
    
    processed = 0
    objects_with_geometry:List[GeometryData] = []
    properties = []
    for element in elements:
        if not element.Representation:
          print(f"Skip: {element.Name}")
          continue
          
        if element.is_a() in ["IfcOpeningElement", "IfcSpace"]:
            print(f"Skip: {element.Name} ({element.is_a()})")
            continue

        try:            
            shape = ifcopenshell.geom.create_shape(geo_settings, element)
            product_details = get_element_properties(element)
            detail = {
               "id":element.id(),
               "detail":product_details
            }
            properties.append(detail)

            if(len(shape.geometry.materials) > 1):
               for i, material in enumerate(shape.geometry.materials):                  
                  geometry_data:GeometryData = build_geometry_data_by_material(shape,element,material,i)
                  objects_with_geometry.append(geometry_data)
            else:
               geometry_data:GeometryData = {
                  "id":element.id(),
                  "vertices": shape.geometry.verts,
                  "indices": shape.geometry.faces,
                  "normals": shape.geometry.normals,
                  "material": shape.geometry.materials[0],
               }

               objects_with_geometry.append(geometry_data)
              
            processed += 1
            if processed % 100 == 0:
                print(f"progress: {processed}/{len(elements)}")
            
        except Exception as e:
            print(f"Warning: An error occurred while processing object {element.id()} ({element.is_a()}): {e}")
            continue

    
    print(f"Number of objects with geometry: {len(objects_with_geometry)}")
    return objects_with_geometry,properties



  except Exception as e:
    print(f"Error: Problem occurred during GLTF conversion. {e}")
    return False

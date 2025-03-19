from typing import Any, Dict, List

import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.shape
import numpy as np

from core.converter import get_geometry_settings, load_ifc_model


def export_glb_with_properties(ifc_path):
  try:
    ifc_model = load_ifc_model(ifc_path)

    if not ifc_model:
        return False
    geo_settings = get_geometry_settings()
    
    elements = ifc_model.by_type("IfcProduct")
    
    processed = 0
    objects_with_geometry: List[Dict[str, Any]] = []
    for element in elements:
        if not element.Representation:
          print(f"スキップ: {element.Name}")
          continue
        if element.is_a() in ["IfcOpeningElement", "IfcSpace", "IfcSite"]:
            print(f"スキップ: {element.Name} ({element.is_a()})")
            continue


        try:            
            shape = ifcopenshell.geom.create_shape(geo_settings, element)

            if(len(shape.geometry.materials) > 1):
               for i, material in enumerate(shape.geometry.materials):
                  mat_ids_array = np.array(shape.geometry.material_ids)
                  mat_ids_index = np.where(mat_ids_array == i)[0]
                  
                  faces = np.array(shape.geometry.faces, dtype=np.int32)
                  faces_2d = faces.reshape(-1, 3)
                  
                  selected_faces = faces_2d[mat_ids_index]
                  faces_tuple = tuple(int(x) for x in selected_faces.flatten())
                  
                  geometry_data = {
                     "id":element.id(),
                      "vertices": shape.geometry.verts, 
                      "indices": faces_tuple,
                      "normals": shape.geometry.normals,
                      "material": material,
                  }
                  objects_with_geometry.append(geometry_data)
            else:
               geometry_data = {
                  "id":element.id(),
                  "vertices": shape.geometry.verts,
                  "indices": shape.geometry.faces,
                  "normals": shape.geometry.normals,
                  "material": shape.geometry.materials[0],
               }

               objects_with_geometry.append(geometry_data)

            # product_details = get_element_details(element)
            
            processed += 1
            if processed % 100 == 0:
                print(f"進捗: {processed}/{len(elements)}")
            
        except Exception as e:
            print(f"警告: オブジェクト {element.id()} ({element.is_a()}) の処理中にエラーが発生しました: {e}")

    
    print(f"ジオメトリを持つオブジェクト数: {len(objects_with_geometry)}/{len(elements)}")
    return ifc_model, objects_with_geometry



  except Exception as e:
    print(f"エラー: GLTF変換中に問題が発生しました。{e}")
    return False

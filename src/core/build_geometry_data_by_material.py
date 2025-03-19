from typing import Union

import numpy as np
from ifcopenshell.entity_instance import entity_instance
from ifcopenshell.geom import ShapeElementType, ShapeType
from ifcopenshell.ifcopenshell_wrapper import style

from types_def.geometry import GeometryData

Shape = Union[ShapeType, ShapeElementType]

def build_geometry_data_by_material(shape:Shape,element:entity_instance,material:style,index:int):
    mat_ids_array = np.array(shape.geometry.material_ids)
    mat_ids_index = np.where(mat_ids_array == index)[0]
    
    faces = np.array(shape.geometry.faces, dtype=np.int32)
    faces_2d = faces.reshape(-1, 3)
    
    selected_faces = faces_2d[mat_ids_index]
    faces_tuple = tuple(int(x) for x in selected_faces.flatten())
    
    geometry_data:GeometryData = {
        "id":element.id(),
        "vertices": shape.geometry.verts, 
        "indices": faces_tuple,
        "normals": shape.geometry.normals,
        "material": material,
    }

    return geometry_data
import numpy as np
from pygltflib import BLEND, OPAQUE, Material, PbrMetallicRoughness

from types_def.geometry import GeometryData, PrepareGeometryData
from utils import extract_color_info


def prepare_geometry_data(objects_with_geometry:list[GeometryData]):
    pointsArray= []
    normalsArray = []
    facesArray = []
    userDataArray = []
    materialsArray = []
    meshId_array = []

    unique_materials = {}
    use_material_map = {}

    for i,obj_data in enumerate(objects_with_geometry):

        mesh_id = obj_data['id']
        meshId_array.append(mesh_id)

        vertices = np.array(obj_data['vertices'], dtype=np.float32).reshape(-1, 3)[:, [0, 2, 1]]
        vertices[:, 0] = -vertices[:, 0]
        pointsArray.append(vertices)

        faces = np.array(obj_data['indices'], dtype=np.uint32).reshape(-1, 3)
        facesArray.append(faces)

        material = obj_data['material']
        material_name = material.name

        use_material_map[i] = material_name

        if material_name not in unique_materials:
            base_color = extract_color_info(material)
            alphaMode = OPAQUE if base_color[-1] == 1 else BLEND
            new_material = Material(
                    pbrMetallicRoughness=PbrMetallicRoughness(
                        baseColorFactor = base_color,
                        metallicFactor=0.0,
                        roughnessFactor=1.0
                    ),
                    alphaMode=alphaMode,
                    alphaCutoff=None,
                    doubleSided=True,
                    name=material_name
                )
            material_index = len(materialsArray)
            unique_materials[material_name] = material_index
            materialsArray.append(new_material)
    
    return PrepareGeometryData(
        pointsArray, 
        normalsArray, 
        facesArray, 
        userDataArray, 
        materialsArray, 
        meshId_array, 
        use_material_map,
        unique_materials
        )
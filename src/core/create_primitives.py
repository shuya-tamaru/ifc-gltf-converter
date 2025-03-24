from ifcopenshell.ifcopenshell_wrapper import style
from pygltflib import Attributes, Primitive


def create_primitives( meshId_array:list[int],use_material_map:dict,unique_materials:dict):
    mesh_primitives = {}
    for i, (mesh_id) in enumerate(meshId_array):
        material_name = use_material_map[i]
        material_index = unique_materials[material_name]
        primitive = Primitive(
                attributes=Attributes(
                    POSITION=i * 2 + 1
                ),
                indices=i * 2,
                material = material_index
        )
        if mesh_id in mesh_primitives:
            mesh_primitives[mesh_id].append(primitive)
        else:
            mesh_primitives[mesh_id] = [primitive]
    
    return mesh_primitives
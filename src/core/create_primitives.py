from ifcopenshell.ifcopenshell_wrapper import style
from pygltflib import Attributes, Primitive


def create_primitives(materialsArray:list[style], meshId_array:list[int]):
    mesh_primitives = {}
    for i, (material, mesh_id) in enumerate(zip(materialsArray, meshId_array)):
        primitive = Primitive(
                attributes=Attributes(
                    POSITION=i * 2 + 1
                ),
                indices=i * 2,
                material = i
        )
        if mesh_id in mesh_primitives:
            mesh_primitives[mesh_id].append(primitive)
        else:
            mesh_primitives[mesh_id] = [primitive]
    
    return mesh_primitives
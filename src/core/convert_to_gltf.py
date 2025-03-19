from typing import Any, Dict, List

import numpy as np
from pygltflib import (ARRAY_BUFFER, BLEND, ELEMENT_ARRAY_BUFFER, FLOAT, GLTF2,
                       OPAQUE, SCALAR, UNSIGNED_INT, VEC3, Accessor,
                       Attributes, Buffer, BufferView, Material, Mesh, Node,
                       PbrMetallicRoughness, Primitive, Scene)

from utils import extract_color_info


def convert_to_gltf(objects_with_geometry:List[Dict[str, Any]]):
    
    # [[x, y, z], [x, y, z], ...]
    pointsArray= []
    # [[x, y, z], [x, y, z], ...]
    normalsArray = []
    # [[1, 2, 3], [2, 3, 4], ...]
    facesArray = []
    userDataArray = []
    materialsArray = []
    meshId_array = []
    material_indices = [] 
    # geometryData
    for obj_index, obj_data in enumerate(objects_with_geometry):

        mesh_id = obj_data['id']
        meshId_array.append(mesh_id)

        vertices = np.array(obj_data['vertices'], dtype=np.float32).reshape(-1, 3)[:, [0, 2, 1]]
        vertices[:, 0] = -vertices[:, 0]
        pointsArray.append(vertices)

        faces = np.array(obj_data['indices'], dtype=np.uint32).reshape(-1, 3)
        facesArray.append(faces)

        material = obj_data['material']
        base_color = extract_color_info(material)
        alphaMode = OPAQUE if base_color[-1] == 1 else BLEND
        material = Material(
                pbrMetallicRoughness=PbrMetallicRoughness(
                    baseColorFactor = base_color,
                    metallicFactor=0.0,
                    roughnessFactor=1.0
                ),
                alphaMode=alphaMode,
                alphaCutoff=None,
                doubleSided=True
            )
        materialsArray.append(material)
    

    binary_blob = bytearray()
    for points, faces in zip(pointsArray,  facesArray):

        points_binary_blob = points.tobytes()
        # normals_binary_blob = normals.tobytes()
        faces_binary_blob = faces.flatten().tobytes()

        binary_blob.extend(faces_binary_blob)
        binary_blob.extend(points_binary_blob)

    buffer = Buffer(byteLength=len(binary_blob))
    
    bufferViews = []
    byte_offset = 0
    accessors = []
    for i, (points, faces) in enumerate(zip(pointsArray, facesArray)):
        faces_byte_length = len(faces.flatten().tobytes())
        bufferViews.append(BufferView(
            buffer=0,
            byteOffset=byte_offset,
            byteLength=faces_byte_length,
            target=ELEMENT_ARRAY_BUFFER
        ))
        byte_offset += faces_byte_length

        points_byte_length = len(points.tobytes())
        bufferViews.append(BufferView(
            buffer=0,
            byteOffset=byte_offset,
            byteLength=points_byte_length,
            target=ARRAY_BUFFER
        ))
        byte_offset += points_byte_length

        accessors.extend([
            Accessor(
                bufferView=i * 2,
                componentType=UNSIGNED_INT,
                count=len(faces.flatten()),
                type=SCALAR,
                max=[np.max(faces).item()],
                min=[np.min(faces).item()],
            ),
            Accessor(
                bufferView=i * 2 + 1,
                componentType=FLOAT,
                count=len(points),
                type=VEC3,
                max=points.max(axis=0).tolist(),
                min=points.min(axis=0).tolist(),
            ),
        ])

    
    meshes = []
    nodes = []
    mesh_primitives = {}
    for i, (material, mesh_id) in enumerate(zip(materialsArray, meshId_array)):
        primitives = []
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
    
    for mesh_id, primitives in mesh_primitives.items():
        meshIndex = len(meshes)
        meshes.append(Mesh(
            primitives=primitives
        ))
        meshes[meshIndex].extras = {"id": mesh_id}
        nodes.append(Node(mesh=meshIndex))

    gltf = GLTF2(
        scene=0,
        scenes=[Scene(nodes=list(range(len(nodes))))],
        nodes=nodes,
        meshes=meshes,
        materials=materialsArray,
        accessors=accessors,
        bufferViews=bufferViews,
        buffers=[buffer]
    )

    gltf.set_binary_blob(bytes(binary_blob))
    return gltf


def save_glb(gltf:GLTF2, output_path):
    gltf.save(output_path)
    print(f"GLBファイルを保存しました: {output_path}")
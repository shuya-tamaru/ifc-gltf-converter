from typing import Any, Dict, List

from pygltflib import GLTF2, Scene

from core.build_gltf_buffer import build_gltf_buffer
from core.create_buffer_views_and_accessors import \
    create_buffer_views_and_accessors
from core.create_mesh_and_node import create_mesh_and_node
from core.create_primitives import create_primitives
from core.prepare_geometry_data import prepare_geometry_data


def gltf_converter_with_attributes(objects_with_geometry:List[Dict[str, Any]]):
    
    geo_data = prepare_geometry_data(objects_with_geometry)
    pointsArray = geo_data.points
    normalsArray = geo_data.normals
    facesArray = geo_data.faces
    userDataArray = geo_data.user_data
    materialsArray = geo_data.materials
    meshId_array = geo_data.mesh_ids

    binary_blob, buffer = build_gltf_buffer(pointsArray, facesArray)

    bufferViews, accessors =create_buffer_views_and_accessors(pointsArray, facesArray)
    
    mesh_primitives = create_primitives(materialsArray, meshId_array)
    meshes, nodes =create_mesh_and_node(mesh_primitives)
    

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
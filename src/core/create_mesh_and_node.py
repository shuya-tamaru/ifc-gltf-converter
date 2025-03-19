from pygltflib import Mesh, Node


def create_mesh_and_node (mesh_primitives:dict):
    meshes = []
    nodes = []
    for mesh_id, primitives in mesh_primitives.items():
        meshIndex = len(meshes)
        meshes.append(Mesh(
            primitives=primitives
        ))
        meshes[meshIndex].extras = {"id": mesh_id}
        nodes.append(Node(mesh=meshIndex))
    return meshes, nodes
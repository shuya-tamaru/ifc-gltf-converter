from pygltflib import Mesh, Node


def create_mesh_and_node (mesh_primitives:dict,properties:list):
    meshes = []
    nodes = []
    for mesh_id, primitives in mesh_primitives.items():
        matching_property = None
        for prop in properties:
            if str(prop["id"]) == str(mesh_id):
                matching_property = prop["detail"]
                break

        meshIndex = len(meshes)
        mesh = Mesh(primitives=primitives)
        mesh.extras = {
            "id": mesh_id
        }
        if matching_property:
            mesh.extras["properties"] = matching_property
        meshes.append(mesh)
        nodes.append(Node(mesh=meshIndex))
    return meshes, nodes
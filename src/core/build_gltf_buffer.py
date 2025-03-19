from pygltflib import Buffer

from types_def.geometry import NpFloatArray32, NpUnSignedInt32Array


def build_gltf_buffer(pointsArray:NpFloatArray32, facesArray:NpUnSignedInt32Array):
    binary_blob = bytearray()
    for points, faces in zip(pointsArray,  facesArray):

        points_binary_blob = points.tobytes()
        # normals_binary_blob = normals.tobytes()
        faces_binary_blob = faces.flatten().tobytes()

        binary_blob.extend(faces_binary_blob)
        binary_blob.extend(points_binary_blob)
    buffer = Buffer(byteLength=len(binary_blob))

    return binary_blob, buffer

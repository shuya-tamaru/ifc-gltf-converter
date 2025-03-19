import numpy as np
from pygltflib import (ARRAY_BUFFER, ELEMENT_ARRAY_BUFFER, FLOAT, SCALAR,
                       UNSIGNED_INT, VEC3, Accessor, BufferView)

from types_def.geometry import NpFloatArray32, NpUnSignedInt32Array


def create_buffer_views_and_accessors(pointsArray:NpFloatArray32, facesArray:NpUnSignedInt32Array):

    bufferViews:list[BufferView] = []
    byte_offset = 0
    accessors:list[Accessor] = []
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

    return bufferViews, accessors

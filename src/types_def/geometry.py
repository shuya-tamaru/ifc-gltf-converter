from dataclasses import dataclass
from typing import Any, TypedDict

import numpy as np
from ifcopenshell.ifcopenshell_wrapper import style
from numpy.typing import NDArray

NpFloatArray32 = NDArray[np.float32]
NpUnSignedInt32Array = NDArray[np.uint32]

class GeometryData(TypedDict):
    id: int
    vertices: tuple[float, ...]
    indices: tuple[int, ...]
    normals: tuple[float, ...]
    material: style

@dataclass
class PrepareGeometryData:
    points: list[NpFloatArray32]
    normals:list[NpFloatArray32]
    faces: list[NpUnSignedInt32Array]
    user_data: list[Any]
    materials: list[style]
    mesh_ids: list[int]

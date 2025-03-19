from typing import Union

import ifcopenshell
from ifcopenshell.ifcopenshell_wrapper import file

IfcModel = Union[ifcopenshell.file, file, None]

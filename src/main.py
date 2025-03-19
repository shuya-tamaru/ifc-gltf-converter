from core.gltf_converter_with_attributes import (
    gltf_converter_with_attributes, save_glb)
from core.load_ifc_model import load_ifc_model
from exporters.basic_glb import export_basic_glb
from exporters.export_glb_with_properties import export_glb_with_properties
from utils import getPaths_input_output


def main():
    ifc_path, output_path = getPaths_input_output()
    
    if ifc_path is None or output_path is None:
        return
    
    ifc_model = load_ifc_model(ifc_path)
    objects_with_geometry,properties = export_glb_with_properties(ifc_model)
    gltf = gltf_converter_with_attributes(objects_with_geometry,properties)
    save_glb(gltf, output_path)

if __name__ == "__main__":
    main()
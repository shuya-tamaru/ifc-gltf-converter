from core.gltf_converter_with_attributes import (
    gltf_converter_with_attributes, save_glb)
from exporters.basic_glb import export_basic_glb
from exporters.export_glb_with_properties import export_glb_with_properties
from utils import load_ifc


def main():
    ifc_path, output_path = load_ifc()
    
    if ifc_path is None or output_path is None:
        return
    
    ifc_model, objects_with_geometry = export_glb_with_properties(ifc_path)
    gltf = gltf_converter_with_attributes(objects_with_geometry)
    save_glb(gltf, output_path)

if __name__ == "__main__":
    main()
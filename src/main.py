from exporters.basic_glb import export_basic_glb
from utils import load_ifc


def main():
    ifc_path, output_path = load_ifc()
    
    if ifc_path is None or output_path is None:
        return
    
    export_basic_glb(ifc_path, output_path)

if __name__ == "__main__":
    main()
import ifcopenshell


def load_ifc_model(ifc_path):
    try:
        print("IFC file loading...")
        ifc_model = ifcopenshell.open(ifc_path)
        print(f"IFC file loaded. Schema version: {ifc_model.schema}")
        return ifc_model
    except Exception as e:
        print(f"Error: Failed to load IFC file. {e}")
        return None
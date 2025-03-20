import sys

from ifcopenshell.ifcopenshell_wrapper import style


def getPaths_input_output():
  if len(sys.argv) < 3:
        print("How to use: python src/main.py input_path.ifc output_path(.glb or .gltf) [export_type]")
        print("export_type: 'properties'(default) or 'model_only'")
        return None, None, None
  
  ifc_path = sys.argv[1]
  output_path = sys.argv[2]
  export_type = sys.argv[3] if len(sys.argv) > 3 else 'properties'
  
  return ifc_path, output_path, export_type

def extract_color_info(style:style):
  try:
    if hasattr(style, 'diffuse'):
        diffuse = style.diffuse
        color_values = [
            diffuse.r(),
            diffuse.g(),
            diffuse.b()
        ]
        opacity = 1.0
        if hasattr(style, 'transparency'):
            try:
                trans_value = float(style.transparency)
                
                if not (trans_value != trans_value):
                    opacity = max(0.0, min(1.0, 1.0 - trans_value))
                else:
                    opacity = 0.0
            except (ValueError, TypeError):
                opacity = 0.0
        
        return color_values + [opacity]
    
    return [1.0, 1.0, 1.0, 0.0]

  except Exception as e:
    print(f"Error: {e}")
    return [1.0, 1.0, 1.0, 0.0]
   
import sys

from ifcopenshell.ifcopenshell_wrapper import style


def getPaths_input_output():
  if len(sys.argv) < 3:
      print("使用方法: python main.py input_path.ifc output_path(.glb or .gltf)")
      return None, None
  
  ifc_path = sys.argv[1]
  output_path = sys.argv[2]
  
  return ifc_path, output_path

def extract_color_info(style:style):
  try:
    if hasattr(style, 'diffuse'):
        diffuse = style.diffuse
        color_values = [
            diffuse.r(),
            diffuse.g(),
            diffuse.b()
        ]
        transparency = 1.0
        if hasattr(style, 'transparency'):
            try:
                trans_value = float(style.transparency)
                
                if not (trans_value != trans_value):
                    transparency = max(0.0, min(1.0, 1.0 - trans_value))
            except (ValueError, TypeError):
                transparency = 1.0
        
        return color_values + [transparency]
    
    return [1.0, 1.0, 1.0, 1.0]

  except Exception as e:
    print(f"Error: {e}")
    return [1.0, 1.0, 1.0, 1.0]()
   
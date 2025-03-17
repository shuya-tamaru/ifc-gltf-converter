import sys


def load_ifc():
  if len(sys.argv) < 3:
      print("使用方法: python script.py input.ifc output.glb")
      return None, None
  
  ifc_path = sys.argv[1]
  output_path = sys.argv[2]
  
  return ifc_path, output_path
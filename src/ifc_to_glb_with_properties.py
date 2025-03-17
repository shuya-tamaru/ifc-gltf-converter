import multiprocessing
import sys
from collections import Counter

import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.shape


def main():
  if len(sys.argv) < 3:
      print("使用方法: python script.py input.ifc output.glb")
      return
  
  ifc_path = sys.argv[1]
  output_path = sys.argv[2]

if __name__ == "__main__":
    main()
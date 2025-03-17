import multiprocessing
import sys
from collections import Counter

import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.shape


def convert_ifc_to_glb(ifc_path, output_path):

  try:
    print("IFCファイルを読み込み中...")
    ifc_model = ifcopenshell.open(ifc_path)
    print(f"IFCファイルの読み込み完了。スキーマバージョン: {ifc_model.schema}")
    
    geo_settings = ifcopenshell.geom.settings()
    geo_settings.set("dimensionality", ifcopenshell.ifcopenshell_wrapper.CURVES_SURFACES_AND_SOLIDS)
    geo_settings.set("apply-default-materials", True)
    print("変換設定を適用しました")

    serialiser_settings = ifcopenshell.geom.serializer_settings()
    serialiser_settings.set("use-element-names", True)
    serialiser = ifcopenshell.geom.serializers.gltf(output_path,geo_settings,serialiser_settings)

    serialiser.setFile(ifc_model)
    serialiser.setUnitNameAndMagnitude("METER", 1.0)
    serialiser.writeHeader()
    
    iterator = ifcopenshell.geom.iterator(geo_settings, ifc_model, multiprocessing.cpu_count())
    
    print("変換を開始します...")
    processed = 0

    if iterator.initialize():
        while True:
            shape = iterator.get()
            serialiser.write(shape)
            processed += 1
            
            if processed % 100 == 0:
                print(f"{processed}個のオブジェクトを処理しました")
                
            if not iterator.next():
                break
            
    serialiser.finalize()
    print(f"変換完了: {processed}個のオブジェクトを処理しました")
    print(f"出力ファイル: {output_path}")



  except Exception as e:
    print(f"エラー: IFCファイルの読み込みに失敗しました。{e}")

def main():
  if len(sys.argv) < 3:
      print("使用方法: python script.py input.ifc output.glb")
      return
  
  ifc_path = sys.argv[1]
  output_path = sys.argv[2]

  convert_ifc_to_glb(ifc_path, output_path)



if __name__ == "__main__":
    main()

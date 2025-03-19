import ifcopenshell.geom

from core.converter import (create_iterator, get_geometry_settings,
                            load_ifc_model)


def export_basic_glb(ifc_path, output_path):
    try:
        ifc_model = load_ifc_model(ifc_path)

        if not ifc_model:
            return False
        
        geo_settings = get_geometry_settings()
        
        serialiser_settings = ifcopenshell.geom.serializer_settings()
        serialiser_settings.set("use-element-names", True)
        serialiser_settings.set("y-up", True)
        serialiser = ifcopenshell.geom.serializers.gltf(output_path, geo_settings, serialiser_settings)

        serialiser.setFile(ifc_model)
        serialiser.setUnitNameAndMagnitude("METER", 1.0)
        serialiser.writeHeader()

        iterator = create_iterator(geo_settings, ifc_model)
        
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
        return True

    except Exception as e:
        print(f"エラー: GLTF変換中に問題が発生しました。{e}")
        return False


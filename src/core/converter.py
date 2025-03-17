import multiprocessing

import ifcopenshell
import ifcopenshell.geom


def load_ifc_model(ifc_path):
    try:
        print("IFCファイルを読み込み中...")
        ifc_model = ifcopenshell.open(ifc_path)
        print(f"IFCファイルの読み込み完了。スキーマバージョン: {ifc_model.schema}")
        return ifc_model
    except Exception as e:
        print(f"エラー: IFCファイルの読み込みに失敗しました。{e}")
        return None
    
def get_geometry_settings():
    geo_settings = ifcopenshell.geom.settings()
    geo_settings.set("dimensionality", ifcopenshell.ifcopenshell_wrapper.CURVES_SURFACES_AND_SOLIDS)
    geo_settings.set("apply-default-materials", True)
    return geo_settings

def create_iterator(settings, ifc_model):
    return ifcopenshell.geom.iterator(settings, ifc_model, multiprocessing.cpu_count())
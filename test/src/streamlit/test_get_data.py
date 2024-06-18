"""Test de APPS/streamlit_revision_en_profundidad/importar_datos_api.py"""
import pytest

import pandas as pd
from pandas.testing import assert_frame_equal


def test_Obtener_maestro_skus():
    from APPS.streamlit_revision_en_profundidad.importar_datos_apis import Obtener_maestro_skus
    assert isinstance(Obtener_maestro_skus(), dict)
    # assert el dict tiene las claves 'df_data' y 'dict_skus_para_cuadro_sleccion'
    assert 'df_data' in Obtener_maestro_skus().keys()
    assert 'dict_skus_para_cuadro_sleccion' in Obtener_maestro_skus().keys()

@pytest.mark.parametrize("sku,frecuencia", [
    (672, 'W'),
])
def test_Obtener_datos_skus(mocker, sku, frecuencia)    :
    import json

    from APPS.streamlit_revision_en_profundidad.importar_datos_apis import _Obtener_datos_skus
    from APPS.utils.parametros_api import FrecuenciaTemporal
    from APPS.api_main.items.item_detalle_evolucion_venta import ItemDetalleEvolucionVenta
    from APPS.api_main.items.item_resumen_evolucion_venta import ItemResumenEvolucionVenta
    
       
    class Mock_Response:
        def json(self):
            with open('test/APPS/streamlit_revision_en_profundidad/data_para_tests/test_obtener_datos_sku_01.json', 'r') as f:
                return json.load(f)
        

    frecuencia_obj = FrecuenciaTemporal(frecuencia_temporal=frecuencia)
    # Mock de método requests en función Obtener_datos_skus de módulo importar_datos_apis
    mocker.patch('requests.get', return_value=Mock_Response())
    
    df_detalle, df_resumen = _Obtener_datos_skus(sku, frecuencia)

    assert isinstance(df_detalle, pd.DataFrame)
    assert isinstance(df_resumen, pd.DataFrame)
    
    # Test de campos retornados
    
    # El método Obtener_datos_skus reemplaza los nombres de campos en dataframe_resumen:
    #   - Cod_producto -> SKU
    # Reverso los cambios para testear contra los campos de ItemResumenEvolucionVenta
    df_resumen.rename(columns={'SKU': 'Cod_producto'}, inplace=True)
    assert set(df_resumen.columns) == set(ItemResumenEvolucionVenta.nombre_campos()), f"Columnas de dataframe resumen evolucion venta no coinciden con columnas de ItemResumenEvolucionVenta. Columnas obtenidas:{set(df_resumen.columns)}. Columnas esperadas {ItemResumenEvolucionVenta.nombre_campos()}"

    #  El método Obtener_datos_skus reemplaza los nombres de campos en dataframe_detalle:
    #   - Cod_producto -> SKU
    #   - frecuencia_obj.nombre -> Fecha
    # Reverso los cambios para testear contra los campos de ItemDetalleEvolucionVenta
    df_detalle.rename(columns={'SKU': 'Cod_producto', 'Fecha': frecuencia_obj.nombre}, inplace=True)

    assert set(df_detalle.columns) == set(ItemDetalleEvolucionVenta.nombre_campos(frecuencia=frecuencia_obj)), f"Columnas de dataframe detalle no coinciden con columnas de ItemDetalleEvolucionVenta. Columnas obtenidas:{set(df_detalle.columns)}. Columnas esperadas {ItemDetalleEvolucionVenta.nombre_campos(frecuencia=frecuencia_obj)}"
    
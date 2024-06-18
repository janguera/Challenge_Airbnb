# Test APPS/data/costos_contables.py
import pytest
import pandas as pd
from pydantic import ValidationError

# Utilitarios para testea
from .util_test import obtener_frecuencias_validas, obtener_data_frecuencia_temporal_no_soportada,obtener_data_dataframe_empty,obtener_data_y_check_campo_datetime


# Define la función obtener_data para ser usada en los tests
@pytest.fixture
def funcion_obtener_data():
    from APPS.api_data.modulos.costos_contables import obtener_data
    yield obtener_data

# # Test APPS/data/costos_contables.py - método obtener_data
@pytest.mark.parametrize('df_base, frecuencia, nombre_campo_date, fecha_inicio, fecha_final', [
    # Caso 1: frecuencia Mes
    (
        pd.DataFrame({
                'Mes': ['2022-01-01'],
                'Cod_producto': [1],
                'Costo_unitario_stock_contable': [100],
        }), 'MS', 'Mes', '2022-01-01', '2022-01-01'    
    ),
    (
        pd.DataFrame({
                'Mes': ['2022-01-01', '2022-02-01'],
                'Cod_producto': [1,2],
                'Costo_unitario_stock_contable': [100,200],
        }), 'MS', 'Mes', '2022-01-01', '2022-01-01'
    ),
    # Caso 2: sin especificar frecuencia
    (
        pd.DataFrame({
            'Semana': ['2022-01-01'],
            'Cod_producto': [1],
            'Costo_unitario_stock_contable': [100],
        }), None, 'Semana', '2022-01-01', '2022-01-01' 
    ),
    # # Caso 3: frecuencia 'D'
    # (pd.DataFrame({
    #         'Fecha': ['2022-01-01'],
    #         'Cod_producto': [1],
    #         'Costo_unitario_stock_contable': [100],
    # }), 'D', 'Fecha','2022-01-01', '2022-01-01' ),
    # Caso 4: frecuencia 'W'
    (pd.DataFrame({
            'Semana': ['2022-01-01'],
            'Cod_producto': [1],
            'Costo_unitario_stock_contable': [100],
    }), 'W', 'Semana', '2022-01-01', '2022-01-01' ),
    # Caso 5: frecuencia 'Q'
    (pd.DataFrame({
            'Quarter': ['2022-01-01'],
            'Cod_producto': [1],
            'Costo_unitario_stock_contable': [100],
    }), 'Q', 'Quarter','2022-01-01', '2022-01-01' ),
    # Caso 6: frecuencia 'Y'
    (pd.DataFrame({
            'Year': ['2022-01-01'],
            'Cod_producto': [1],
            'Costo_unitario_stock_contable': [100],
    }), 'Y', 'Year', '2022-01-01', '2022-01-01' ),

])
def test_obtener_data(funcion_obtener_data, df_base, frecuencia, nombre_campo_date, fecha_inicio, fecha_final):
    df = obtener_data_y_check_campo_datetime(
            function_obtener_data=funcion_obtener_data, 
            frecuencia=frecuencia, 
            nombre_campo_date=nombre_campo_date, 
            data_frame=df_base,
            fecha_inicio=fecha_inicio,
            fecha_final=fecha_final
        )

    


# Test APPS/data/costos_contables.py - método obtener_data - Caso: DataFrame vacío (i.e, no hay datos retornados por la query)
def test_obtener_dataframe_empty(funcion_obtener_data):
    obtener_data_dataframe_empty(function_obtener_data=funcion_obtener_data)

# Test APPS/data/costos_contables.py - método obtener_data - Caso: frecuencia temporal no soportada
@pytest.mark.parametrize('frecuencia_temporal, exception_error', [
    ('QQQ', ValidationError),
    ('D', AssertionError)
])
def test_obtener_data_frecuencia_temporal_no_soportada(funcion_obtener_data, frecuencia_temporal, exception_error):        
    obtener_data_frecuencia_temporal_no_soportada(function_obtener_data=funcion_obtener_data, frecuencia_temporal=frecuencia_temporal, exception_error=exception_error)



# Test APPS/data/costos_contables.py - método obtener_data - Caso: Se utiliza periodo ajustado de acuerdo a frecuencia
# Notas:
#   Chequea que la query contena las fechas de los períodos esperados ajustados de acuerdo a la frecuencia
#   No chequea que los datos obtenidos correspondan a la frecuencia solicitada
@pytest.mark.parametrize('frecuencia_temporal', [
    'W',
    'MS',
    'Q',
    'Y',
])
def test_obtener_data_frecuencias_validas(funcion_obtener_data,frecuencia_temporal):
    obtener_frecuencias_validas(function_obtener_data=funcion_obtener_data, frecuencia_temporal=frecuencia_temporal)
import requests
import json
import streamlit as st
import pandas as pd
import os

from pydantic import BaseSettings

class Settings(BaseSettings):
    middleware_host: str
    api_main_path: str = '/pricing-api-main'

    class Config:
        env_prefix = "API_PRICING_"
        case_sensitive = False
        env_file = ".env_api"




# if os.getcwd().split("/")[-1] == "pricing":
#     url = "0.0.0.0"    
# else:
#     url = "api"


host = Settings().middleware_host
host = host if host[-1] != "/" else host[:-1]
host = host + Settings().api_main_path



@st.cache(allow_output_mutation=True, show_spinner=False)
def Obtener_maestro_skus() -> pd.DataFrame:
    """
    Obtengo maestro de SKU que tengo información para revisar

    Retorno un dict con:
        - df: dataframe con los SKU que tengo información para revisar
        - dict_skus_para_cuadro_sleccion: diccionario con los SKU que tengo información para revisar
                        {'Cod_producto': 'Descriptor'   for .... }
    """    

    def dict_skus_para_cuadro_sleccion(maestro_skus: pd.DataFrame) -> dict:
        """Retorna diccionario con los SKU que tengo información para revisar
            { 'descriptor': 'Cod_producto'   for ....}
        """
        dict_maestro_skus = maestro_skus[['Descriptor']].to_dict('split')
        cod_producto = dict_maestro_skus['index']
        descriptor = [d[0] for d in dict_maestro_skus['data'] ]
        return { c:d for c,d in sorted(list(zip(cod_producto, descriptor)), key=lambda x: x[1]) }
    

    df_data = _Obtener_maestro_skus()
    return { 'df_data': df_data, 
              'dict_skus_para_cuadro_sleccion': dict_skus_para_cuadro_sleccion(df_data) 
            }

def _Obtener_maestro_skus() -> pd.DataFrame:
    """
    Obtengo un diccionario lista con los SKU que tengo información para revisar
    El dataframe retornado tiene el Cod_producto en el index

    """    
    __url = host+"/lista_productos"
    print(f'OBTENER_DATOS_MAESTRO_URL: #{__url}#')
    res = requests.get(url = __url)
    return pd.DataFrame.from_dict(data=res.json(), orient='tight')




@st.cache(show_spinner=False)
def Obtener_parametros() -> pd.DataFrame:
    """
    Obtengo los parametros de configuración de los SKU
    """
    res = requests.get(url = host+"/obtener_parametros")
    return pd.DataFrame(eval(res.text))

@st.cache(allow_output_mutation=True, show_spinner=False)
def Obtener_datos_skus(sku: int, frecuencia: str) -> pd.DataFrame:    
    """ Wrapper con cache para función _Obtener_datos_skus """
    return _Obtener_datos_skus(sku, frecuencia)

def _Obtener_datos_skus(sku: int, frecuencia: str) -> pd.DataFrame:    
    """
    Obtengo dataframed con los datos de los SKU que tengo información para revisar

    Retorno 2 dataframes:
        - df_evolucion_venta_detalle: con los datos de venta a nivel detalle
        - df_evolucion_venta_resumen: con los datos de venta a nivel resumen

    En los dataframes, los siguientes campos han sido renombrados:
        - Cod_producto -> SKU
        - <nombre campo frecuencia> -> Fecha
    """
    from APPS.utils.parametros_api import FrecuenciaTemporal
    inputs = {
                "SKU": sku, 
                "frecuencia": frecuencia,
                "analisis_temporal": "trimestre_anual",
            }
    res = requests.get(url = host+"/data_producto_en_profundidad", params = inputs)

    data = res.json()

    columna_temporal                    = FrecuenciaTemporal(frecuencia_temporal=frecuencia).nombre
    df_evolucion_venta_detalle          = pd.DataFrame.from_dict( data['evolucion_venta_detalle'], orient='tight').rename(columns={"Cod_producto": "SKU", columna_temporal: 'Fecha'})
    df_evolucion_venta_detalle['Fecha'] = pd.to_datetime(df_evolucion_venta_detalle['Fecha'])

    df_evolucion_venta_resumen  = pd.DataFrame.from_dict( data['evolucion_venta_resumen'], orient='tight').rename(columns={"Cod_producto": "SKU"})

    df_evolucion_venta_detalle['Cantidad_competencia']  = df_evolucion_venta_detalle['Cantidad_competencia_mercado'] - df_evolucion_venta_detalle['Cantidad_AH_mercado']
    df_evolucion_venta_detalle['Cantidad_AH']           = df_evolucion_venta_detalle['Cantidad_AH_mercado']
    df_evolucion_venta_detalle['Revenue_competencia']   = df_evolucion_venta_detalle['Revenue_competencia_mercado'] - df_evolucion_venta_detalle['Revenue_AH_mercado']
    df_evolucion_venta_detalle['Revenue_AH']            = df_evolucion_venta_detalle['Revenue_AH_mercado']
    
    return df_evolucion_venta_detalle, df_evolucion_venta_resumen

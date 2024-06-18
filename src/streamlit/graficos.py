import altair as alt
import pandas as pd

def grafico_revenue(df: pd.DataFrame) -> alt.Chart:
    return alt.Chart(df, title="Revenue").mark_line(
        point={
            "filled": False,
            "fill": "white"
        }
    ).transform_fold(
        fold=['Revenue', 'Revenue_sin_dcto', 'Revenue_con_dcto_solo_abf', 'Revenue_con_otros_dctos'], 
        as_=['Variable', 'Valor']
    ).encode(
        x='Fecha:T',
        y=alt.Y('max(Valor):Q', axis=alt.Axis(title='Valor', titleColor='#000000', format='$,.0f')),
        color='Variable:N',
        tooltip = [alt.Tooltip('max(Valor):Q', format = '$,.0f', title= 'Valor'),
                    alt.Tooltip('Fecha:T', title='Fecha'),
                ]            
    ).properties(
        width=1200,
        height=300
    )

def grafico_unidades(df: pd.DataFrame) -> alt.Chart:
    return alt.Chart(df, title="Unidades").mark_line(
        point={
            "filled": False,
            "fill": "white"
        }            
    ).transform_fold(
        fold=['Unidades_sin_dcto', 'Unidades_con_dcto_solo_abf', 'Unidades_con_otros_dctos', 'Unidades'], 
        as_=['Variable', 'Valor']
    ).encode(
        x='Fecha:T',
        y=alt.Y('max(Valor):Q', axis=alt.Axis(title='Unidades', titleColor='#000000', format=',.0f')),
        color='Variable:N',
        tooltip = [alt.Tooltip('max(Valor):Q', format = ',.0f', title= 'Valor'),
                    alt.Tooltip('Fecha:T', title='Fecha'),
                ]              
    ).properties(
        width=1200,
        height=300
    )

def grafico_precios_ahumada(df: pd.DataFrame) -> alt.Chart:
    return alt.Chart(df, title="Precios Ahumada").mark_line(
        point={
            "filled": False,
            "fill": "white"
        }            
    ).transform_fold(
        fold=['Precio_lleno', 'Precio_revenue_con_dcto_solo_abf', 'Precio_revenue_con_otros_dctos', 'Precio_revenue'], 
        as_=['Variable', 'Valor']
    ).encode(
        x='Fecha:T',
        y=alt.Y('max(Valor):Q', axis=alt.Axis(title='Valor', titleColor='#000000', format='$,.0f')),
        color='Variable:N',
        tooltip = [alt.Tooltip('max(Valor):Q', format = '$,.0f', title= 'Valor'),
                    alt.Tooltip('Fecha:T', title='Fecha'),
                ]            
    ).properties(
        width=1200,
        height=300
    )

def grafico_precio_lleno(df_precios_estandarizado: pd.DataFrame) -> alt.Chart:
    return alt.Chart(df_precios_estandarizado, title="Comparativa precio lleno").mark_line(
        point={
            "filled": False,
            "fill": "white"
        }            
    ).transform_fold(
        fold=['Precio_normal_FAhumada_promedio', 'Precio_normal_CruzVerde_promedio', 'Precio_normal_Salcobrand_promedio'], 
        as_=['Variable', 'Valor']
    ).encode(
        x='Fecha:T',
        y=alt.Y('max(Valor):Q', axis=alt.Axis(title='Valor', titleColor='#000000', format='$,.0f')),
        color=alt.Color('Variable:N', scale=alt.Scale(range=['#578259', '#e85f5f', '#52748d'])),
        tooltip = [alt.Tooltip('max(Valor):Q', format = '$,.0f', title= 'Valor'),
                    alt.Tooltip('Fecha:T', title='Fecha'),
                ] 
    ).properties(
        width=1200,
        height=300
    )

def grafico_precio_revenue(df_marketshare_estandarizado: pd.DataFrame) -> alt.Chart:
    return alt.Chart(df_marketshare_estandarizado, title="Comparativa precio revenue").mark_line(
        point={
            "filled": False,
            "fill": "white"
        }            
    ).transform_fold(
        fold=['precio_unitario_AH', 'precio_unitario_competencia'], 
        as_=['Variable', 'Valor']
    ).encode(
        x='Fecha:T',
        y = alt.Y('max(Valor):Q', axis=alt.Axis(title='Valor', titleColor='#000000', format='$,.0f')),
        color='Variable:N',
        tooltip = [alt.Tooltip('max(Valor):Q', format = '$,.0f', title= 'Valor'),
                    alt.Tooltip('Fecha:T', title='Fecha'),
                ] 
    ).properties(
        width=1200,
        height=300
    )

def grafico_margen(df: pd.DataFrame) -> alt.Chart:
    return alt.Chart(df, title="Margen").mark_line(
        point={
            "filled": False,
            "fill": "white"
        }            
    ).transform_fold(
        fold=['Margen_unitario_sin_dcto', 'Margen_unitario_con_dcto_solo_abf', 'Margen_unitario_con_otros_dctos', 'Margen_unitario'], 
        as_=['Variable', 'Valor']
    ).encode(
        x='Fecha:T',
        y=alt.Y('max(Valor):Q', axis=alt.Axis(title='Valor', titleColor='#000000', format='$,.0f')),
        color='Variable:N',
        tooltip = [alt.Tooltip('max(Valor):Q', format = '$,.0f', title= 'Valor'),
                    alt.Tooltip('Fecha:T', title='Fecha'),
                ]            
    ).properties(
        width=1200,
        height=300
    )

def grafico_costos(df: pd.DataFrame) -> alt.Chart:
    return alt.Chart(df, title="Costos").mark_line(
        point={
            "filled": False,
            "fill": "white"
        }            
    ).transform_fold(
        fold=['Costo_unitario_con_recupero', 'Costo_unitario_a_valor_de_ultima_compra', 'Recupero_unitario_neto', 'Recupero_unitario_cronico'], 
        as_=['Variable', 'Valor']
    ).encode(
        x='Fecha:T',
        y=alt.Y('max(Valor):Q', axis=alt.Axis(title='Valor', titleColor='#000000', format='$,.0f')),
        color='Variable:N',
        tooltip = [alt.Tooltip('max(Valor):Q', format = '$,.0f', title= 'Valor'),
                    alt.Tooltip('Fecha:T', title='Fecha'),
                ]            
    ).properties(
        width=1200,
        height=300
    )

def grafico_stock(df_stock_diario: pd.DataFrame) -> alt.Chart:
    return alt.Chart(df_stock_diario, title="Stock diario").mark_line(
        point={
            "filled": False,
            "fill": "white"
        }             
    ).transform_fold(
        fold=['Stock_minimo', 'Stock_maximo', 'Stock_promedio'], 
        as_=['Variable', 'Valor']
    ).encode(
        x='Fecha:T',
        y=alt.Y('max(Valor):Q', axis=alt.Axis(title='Unidades', titleColor='#000000', format=',.0f')),
        color='Variable:N',
        tooltip = [alt.Tooltip('max(Valor):Q', format = ',.0f', title= 'Valor'),
                    alt.Tooltip('Fecha:T', title='Fecha'),
                ] 
    ).properties(
        width=1200,
        height=300
    )

def grafico_uds_x_transaccion(df: pd.DataFrame) -> alt.Chart:
    return alt.Chart(df, title="Promedio unidades por transacción").mark_line(
        point={
            "filled": False,
            "fill": "white"
        }            
    ).transform_fold(
        fold=['Uds_x_transacc_unicas'], 
        as_=['Variable', 'Valor']
    ).encode(
        x='Fecha:T',
        y=alt.Y('max(Valor):Q', axis=alt.Axis(title='Cantidad', titleColor='#000000', format='.1f')),
        color='Variable:N',
        tooltip = [alt.Tooltip('max(Valor):Q', format = '.1f', title= 'Valor'),
                    alt.Tooltip('Fecha:T', title='Fecha'),
                ] 
    ).properties(
        width=1200,
        height=300
    )

def grafico_transacciones_diarias(df: pd.DataFrame) -> alt.Chart:
    return alt.Chart(df, title="Transacciones únicas promedio diarias").mark_line(
        point={
            "filled": False,
            "fill": "white"
        }            
    ).transform_fold(
        fold=['Transacciones_unicas_prom_diarias'], 
        as_=['Variable', 'Valor']
    ).encode(
        x='Fecha:T',
        y=alt.Y('max(Valor):Q', axis=alt.Axis(title='Cantidad', titleColor='#000000', format=',.0f')),
        color='Variable:N',
        tooltip = [alt.Tooltip('max(Valor):Q', format = ',.0f', title= 'Valor'),
                    alt.Tooltip('Fecha:T', title='Fecha'),
                ] 
    ).properties(
        width=1200,
        height=300
    )

def grafico_venta_perdida(df_venta_perdida_estandarizado: pd.DataFrame) -> alt.Chart:
    return alt.Chart(df_venta_perdida_estandarizado, title="Venta perdida").mark_line(
        point={
            "filled": False,
            "fill": "white"
        }             
    ).transform_fold(
        fold=['Revenue_perdido'], 
        as_=['Variable', 'Valor']
    ).encode(
        x='Fecha:T',
        y=alt.Y('max(Valor):Q', axis=alt.Axis(title='Valor', titleColor='#000000', format='$,.0f')),
        color='Variable:N',
        tooltip = [alt.Tooltip('max(Valor):Q', format = '$,.0f', title= 'Valor'),
                    alt.Tooltip('Fecha:T', title='Fecha'),
                ] 
    ).properties(
        width=1200,
        height=300
    )

def grafico_fillrate(df_fillrate: pd.DataFrame) -> alt.Chart:
    line = alt.Chart(df_fillrate, title="Fillrate").mark_bar(
            size=5,
            opacity=0.8
        ).transform_fold(
            fold=['Fillrate'], 
            as_=['Variable', 'Valor']
        ).encode(
            x='Fecha:T',
            y = alt.Y('max(Valor):Q',axis=alt.Axis(title='Fillrate', titleColor='#000000', format='%')),
            color='Variable:N',
            tooltip = [
                        alt.Tooltip('max(Valor):Q', format = '.2%', title= 'Valor'),
                        alt.Tooltip('Fecha:T', title='Fecha'),
                    ] 
        )
    bar = alt.Chart(df_fillrate, title="Fillrate").mark_tick(
            color='red',
            thickness=2,
            size=10 * 0.9,
        ).transform_fold(
            fold=['Cantidad_Solicitada'], 
            as_=['Variable', 'Valor']
        ).encode(
            x='Fecha:T',
            y = alt.Y('max(Valor):Q', axis=alt.Axis(title='Cantidad solicitada', titleColor='#000000')),
            # color = alt.Color('red'),
            tooltip = [
                        alt.Tooltip('max(Valor):Q', format = ',.0f', title= 'Valor'),
                        alt.Tooltip('Fecha:T', title='Fecha'),
                    ]
        )

    return alt.layer(line, bar).resolve_scale(
                y='independent'
            ).properties(
                width=1200,
                height=300
            ) 

def grafico_mercado_uds(df_marketshare_estandarizado: pd.DataFrame) -> alt.Chart:

    line = alt.Chart(df_marketshare_estandarizado, title="Evolución del mercado en unidades").mark_line(
        point={
            "filled": False,
            "fill": "white"
        }            
        ).transform_fold(
            fold=['Cantidad_AH', 'Cantidad_competencia'], 
            as_=['Variable', 'Valor']
        ).encode(
            x='Fecha:T',
            y = alt.Y('max(Valor):Q', axis=alt.Axis(title='Unidades', titleColor='#000000')),
            color='Variable:N',
            tooltip = [
                        alt.Tooltip('max(Valor):Q', format = '$,.0f', title= 'Valor'),
                        alt.Tooltip('Fecha:T', title='Fecha'),
                    ] 
        )
    bar = alt.Chart(df_marketshare_estandarizado, title="Evolución del mercado en unidades").mark_bar(
            size=15,
            opacity=0.2
        ).transform_fold(
            fold=['Pct_Ahumada_cantidad'], 
            as_=['Variable', 'Valor']
        ).encode(
            x='Fecha:T',
            y = alt.Y('max(Valor):Q',axis=alt.Axis(title='Participación de mercado', titleColor='#000000', format='%')),
            color = alt.value('#8f8f8f'),
            tooltip = [
                        alt.Tooltip('max(Valor):Q', format = '.2%', title= 'Valor'),
                        alt.Tooltip('Fecha:T', title='Fecha'),
                    ]
        )

    return alt.layer(line, bar).resolve_scale(
                y='independent'
            ).properties(
                width=1200,
                height=300
            ) 

def grafico_mercado_valor(df_marketshare_estandarizado: pd.DataFrame) -> alt.Chart:

    line = alt.Chart(df_marketshare_estandarizado, title="Evolución del mercado en valor").mark_line(
        point={
            "filled": False,
            "fill": "white"
        }            
        ).transform_fold(
            fold=['Revenue_AH', 'Revenue_competencia'], 
            as_=['Variable', 'Valor']
        ).encode(
            x='Fecha:T',
            y = alt.Y('max(Valor):Q', axis=alt.Axis(title='Valor', titleColor='#000000', format='$,.0f')),
            color='Variable:N',
            tooltip = [
                        alt.Tooltip('max(Valor):Q', format = '$,.0f', title= 'Valor'),
                        alt.Tooltip('Fecha:T', title='Fecha'),
                    ] 
        )
    bar = alt.Chart(df_marketshare_estandarizado, title="Evolución del mercado en valor").mark_bar(
            size=15,
            opacity=0.2
        ).transform_fold(
            fold=['Pct_Ahumada_revenue'], 
            as_=['Variable', 'Valor']
        ).encode(
            x='Fecha:T',
            y = alt.Y('max(Valor):Q',axis=alt.Axis(title='Participación de mercado', titleColor='#000000', format='%')),
            color=alt.value('#8f8f8f'),
            tooltip = [
                        alt.Tooltip('max(Valor):Q', format = '.2%', title= 'Valor'),
                        alt.Tooltip('Fecha:T', title='Fecha'),
                    ]
        )

    return alt.layer(line, bar).resolve_scale(
            y='independent'
        ).properties(
            width=1200,
            height=300
        )

# def grafico_comparativa_revenue_ahumada(df: pd.DataFrame) -> alt.Chart:
#     return alt.Chart(df, title="Comparativa revenue Ahumada vs. datos informes mercado").mark_line(
#         point={
#             "filled": False,
#             "fill": "white"
#         }             
#     ).transform_fold(
#         fold=['Revenue', 'Revenue_AH_IQVIA', 'Revenue_AH_NIELSEN'], 
#         as_=['Variable', 'Valor']
#     ).encode(
#         x='Fecha:T',
#         y=alt.Y('max(Valor):Q', axis=alt.Axis(title='Valor', titleColor='#000000', format='$,.0f')),
#         color='Variable:N',
#         tooltip = [alt.Tooltip('max(Valor):Q', format = '$,.0f', title= 'Valor'),
#                     alt.Tooltip('Fecha:T', title='Fecha'),
#                 ]            
#     ).properties(
#         width=1200,
#         height=300
#     )

# def grafico_comparativa_unidades_ahumada(df: pd.DataFrame) -> alt.Chart:
#     return alt.Chart(df, title="Comparativa unidades Ahumada vs. datos informes mercado").mark_line(
#         point={
#             "filled": False,
#             "fill": "white"
#         }             
#     ).transform_fold(
#         fold=['Unidades', 'Cantidad_AH_IQVIA', 'Cantidad_AH_NIELSEN'], 
#         as_=['Variable', 'Valor']
#     ).encode(
#         x='Fecha:T',
#         y=alt.Y('max(Valor):Q', axis=alt.Axis(title='Cantidad', titleColor='#000000', format=',.0f')),
#         color='Variable:N',
#         tooltip = [alt.Tooltip('max(Valor):Q', format = ',.0f', title= 'Valor'),
#                     alt.Tooltip('Fecha:T', title='Fecha'),
#                 ]            
#     ).properties(
#         width=1200,
#         height=300
#     )


# def grafico_comparativa_datos_mercado(df: pd.DataFrame) -> alt.Chart:
#     line_revenue = alt.Chart(df, title="Comparativa datos mercado IQVIA vs. Nielsen").mark_line(
#         point={
#             "filled": False,
#             "fill": "white"
#         }            
#         ).transform_fold(
#             fold=['Revenue_competencia_IQVIA', 'Revenue_competencia_NIELSEN'], 
#             as_=['Variable', 'Valor']
#         ).encode(
#             x='Fecha:T',
#             y = alt.Y('max(Valor):Q', axis=alt.Axis(title='Valor', titleColor='#000000', format='$,.0f')),
#             color='Variable:N',
#             tooltip = [
#                         alt.Tooltip('max(Valor):Q', format = '$,.0f', title= 'Valor'),
#                         alt.Tooltip('Fecha:T', title='Fecha'),
#                     ] 
#         )
#     line_uds = alt.Chart(df, title="Comparativa datos mercado IQVIA vs. Nielsen").mark_line(
#         point={
#             "filled": False,
#             "fill": "white"
#         }            
#         ).transform_fold(
#             fold=['Cantidad_competencia_IQVIA', 'Cantidad_competencia_NIELSEN'],
#             as_=['Variable', 'Valor']
#         ).encode(
#             x='Fecha:T',
#             y = alt.Y('max(Valor):Q',axis=alt.Axis(title='Unidades', titleColor='#000000', format=',.0f')),
#             color = 'Variable:N',
#             tooltip = [
#                         alt.Tooltip('max(Valor):Q', format = ',.0f', title= 'Valor'),
#                         alt.Tooltip('Fecha:T', title='Fecha'),
#                     ]
#         )

#     return alt.layer(line_revenue, line_uds).resolve_scale(
#                 y='independent'
#             ).properties(
#                 width=1200,
#                 height=300
#             ) 


# def grafico_comparativa_precio_unitario_ahumada(df: pd.DataFrame) -> alt.Chart:
#     return alt.Chart(df, title="Comparativa precio lleno Ahumada vs. precio revenue unitario informes mercado").mark_line(
#         point={
#             "filled": False,
#             "fill": "white"
#         }             
#     ).transform_fold(
#         fold=['Precio_normal_FAhumada', 'precio_unitario_ahumada_IQVIA', 'precio_unitario_ahumada_NIELSEN'], 
#         as_=['Variable', 'Valor']
#     ).encode(
#         x='Fecha:T',
#         y=alt.Y('max(Valor):Q', axis=alt.Axis(title='Valor', titleColor='#000000', format='$,.0f')),
#         color='Variable:N',
#         tooltip = [alt.Tooltip('max(Valor):Q', format = '$,.0f', title= 'Valor'),
#                     alt.Tooltip('Fecha:T', title='Fecha'),
#                 ]            
#     ).properties(
#         width=1200,
#         height=300
#     )


# def grafico_comparativa_precio_unitario_mercado(df: pd.DataFrame) -> alt.Chart:
#     return alt.Chart(df, title="Comparativa precio lleno mercado vs. precio revenue unitario mercado").mark_line(
#         point={
#             "filled": False,
#             "fill": "white"
#         }             
#     ).transform_fold(
#         fold=['Precio_normal_CruzVerde', 'Precio_normal_Salcobrand', 'precio_unitario_competencia_IQVIA', 'precio_unitario_competencia_NIELSEN'], 
#         as_=['Variable', 'Valor']
#     ).encode(
#         x='Fecha:T',
#         y=alt.Y('max(Valor):Q', axis=alt.Axis(title='Valor', titleColor='#000000', format='$,.0f')),
#         color='Variable:N',
#         tooltip = [alt.Tooltip('max(Valor):Q', format = '$,.0f', title= 'Valor'),
#                     alt.Tooltip('Fecha:T', title='Fecha'),
#                 ]            
#     ).properties(
#         width=1200,
#         height=300
#     )
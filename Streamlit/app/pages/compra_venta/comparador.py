import streamlit as st

import pandas as pd
from sklearn.preprocessing import MinMaxScaler, RobustScaler
import plotly.graph_objects as go

df = pd.read_csv("data/alquileres_completo_limpio.csv", low_memory=False)
df = df.dropna(subset=['precio'])
# Identificar y eliminar outliers
Q1 = df['precio'].quantile(0.05)
Q3 = df['precio'].quantile(0.95)
IQR = Q3 - Q1
filtro = (df['precio'] >= (Q1 - 1.5 * IQR)) & (df['precio'] <= (Q3 + 1.5 * IQR))
df = df[filtro]
df = df[df['precio'] >= 10]

def vista_detallada():
    st.sidebar.title("Navegación")
    if st.sidebar.button("Página Principal"):
        st.session_state.page = "primera_pagina"
    if st.sidebar.button("Vista de Gráficos"):
        st.session_state.page = "vista_graficos"

    st.title("Vista Detallada")
    st.write("En esta página podras buscar y comparar inmuebles de diferentes zonas de España.")
    st.write("Además contamos con una herramienta con la que podrás observar de forma visual las diferencias entre las principales caracteristicas que puede ofrecerte cada uno de ellos.")

    ##GRAFICO DE RADAR PARA COMPARAR INMUEBLES##
    columnas_importantes = ['identificador', 'superficie', 'superficie_construida', 'superficie_util', 'planta',
                            'baños', 'precio_m2', 'precio', 'habitaciones', 'ubicacion', 'href', 'nombre','CCAA']
    df_importante = df[columnas_importantes].copy()

    # Escala del precio
    scaler_price = RobustScaler()
    df_importante['precio_escalado'] = scaler_price.fit_transform(df_importante[['precio']])

    # Escala del resto de caracteristicas para normalizarlas
    scaler_others = MinMaxScaler()
    df_others_scaled = scaler_others.fit_transform(
        df_importante.drop(columns=['identificador', 'precio', 'precio_escalado', 'ubicacion', 'href', 'nombre', 'CCAA']))

    # Combinamos los datos escalados
    df_scaled = pd.DataFrame(df_others_scaled, columns=columnas_importantes[1:-5])
    df_scaled['precio'] = df_importante['precio_escalado']
    df_scaled['identificador'] = df_importante['identificador'].values

    # Título de la aplicación
    st.title('Comparativa de Inmuebles')

    # Filtro de CCAA
    ccaa_seleccionada = st.selectbox('Selecciona la CCAA', df['CCAA'].unique(), index=0)

    # Filtrar el DataFrame por la CCAA seleccionada
    df_ccaa_filtrado = df[df['CCAA'] == ccaa_seleccionada]

    # Filtro de ubicaciones
    ubicaciones = st.multiselect(
        'En qué ubicaciones quieres buscar',
        df_ccaa_filtrado['ubicacion'].unique(),
        placeholder='Selecciona una o varias ubicaciones'
    )

    # Filtrar el DataFrame por ubicaciones seleccionadas
    if ubicaciones:
        df_filtrado = df_ccaa_filtrado[df_ccaa_filtrado['ubicacion'].isin(ubicaciones)]
    else:
        df_filtrado = df_ccaa_filtrado

    # Eliminamos columnas completamente vacías
    df_filtrado = df_filtrado.dropna(axis=1, how='all')

    # Mostramos el DataFrame filtrado solo si no está vacío
    if not df_filtrado.empty:
        st.write('Datos filtrados por ubicación:')
        st.dataframe(df_filtrado)
    else:
        st.write('No hay datos disponibles para las ubicaciones seleccionadas.')

    # Pedimos que seleccione los identificadores de los inmuebles que se quieren comparar
    id1 = st.selectbox('Selecciona el primer identificador', df_filtrado['identificador'].unique())
    id2 = st.selectbox('Selecciona el segundo identificador', df_filtrado['identificador'].unique())

    # Filtramos los datos seleccionados
    piso1 = df_scaled[df_scaled['identificador'] == id1].drop(columns=['identificador'])
    piso2 = df_scaled[df_scaled['identificador'] == id2].drop(columns=['identificador'])

    # Creamos el gráfico de radar
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=piso1.iloc[0],
        theta=piso1.columns,
        fill='toself',
        name=f'{id1} - {df_filtrado[df_filtrado["identificador"] == id1]["ubicacion"].values[0]}'
    ))

    fig.add_trace(go.Scatterpolar(
        r=piso2.iloc[0],
        theta=piso2.columns,
        fill='toself',
        name=f'{id2} - {df_filtrado[df_filtrado["identificador"] == id2]["ubicacion"].values[0]}'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=False,
                range=[-2, 2]
            )
        ),
        showlegend=True
    )

    st.plotly_chart(fig)

    # Mostramos el DataFrame comparativo
    piso1_original = df[df['identificador'] == id1][columnas_importantes]
    piso2_original = df[df['identificador'] == id2][columnas_importantes]
    df_comparativo = pd.concat([piso1_original, piso2_original], ignore_index=True)

    # Reordenamos las columnas segun su importancia
    columnas_ordenadas = [
        'identificador', 'nombre', 'ubicacion', 'CCAA', 'precio', 'precio_m2',
        'superficie', 'superficie_construida', 'superficie_util', 'planta',
        'habitaciones', 'baños', 'href'
    ]
    df_comparativo = df_comparativo[columnas_ordenadas]

    st.write('Comparativa de características originales:')
    st.dataframe(df_comparativo)
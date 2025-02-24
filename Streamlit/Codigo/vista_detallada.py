import streamlit as st

import pandas as pd
from sklearn.preprocessing import MinMaxScaler, RobustScaler
import plotly.graph_objects as go

from cargar_datos import cargar_datos

df = cargar_datos()
nuevo_orden = [
    # 1. Identificación y Metadatos
    'identificador', 'nombre', 'href', 'agencia', 'timestamp',

    # 2. Ubicación y Descripción General
    'ubicacion', 'codigo_postal', 'tipo_de_casa', 'planta', 'orientacion',

    # 3. Precio y Costos Asociados
    'precio', 'precio_m2', 'gastos_de_comunidad',

    # 4. Tiempos y Actualizaciones (movido aquí)
    'antiguedad', 'actualizacion', 'telefono',

    # 5. Dimensiones y Distribución
    'superficie_util', 'superficie_construida', 'superficie_solar', 'superficie',
    'habitaciones', 'baños', 'comedor',

    # 6. Características del Inmueble
    'cocina_equipada', 'amueblado', 'lavadero', 'balcon', 'terraza',
    'trastero', 'garaje', 'piscina', 'chimenea', 'soleado',
    'exterior', 'interior', 'carpinteria_interior', 'carpinteria_exterior',
    'tipo_suelo', 'puerta_blindada', 'armarios_empotrados',

    # 7. Servicios e Infraestructura
    'luz', 'agua', 'gas', 'calefaccion', 'aire_acondicionado', 'sistema_de_seguridad',
    'ascensor', 'portero_automatico', 'se_aceptan_mascotas',
    'adaptado_a_personas_con_movilidad_reducida',
    'calle_asfaltada', 'calle_alumbrada', 'alcantarillado', 'urbanizado',

    # 8. Eficiencia Energética
    'consumo', 'emisiones', 'vidrios_dobles'
]

df = df[nuevo_orden]

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
                            'baños', 'precio_m2', 'precio', 'habitaciones', 'ubicacion', 'href', 'nombre']
    df_importante = df[columnas_importantes].copy()

    # Escala del precio
    scaler_price = RobustScaler()
    df_importante['precio_escalado'] = scaler_price.fit_transform(df_importante[['precio']])

    # Escala del resto de caracteristicas para normalizarlas
    scaler_others = MinMaxScaler()
    df_others_scaled = scaler_others.fit_transform(
        df_importante.drop(columns=['identificador', 'precio', 'precio_escalado', 'ubicacion', 'href', 'nombre']))

    # Combinamos los datos escalados
    df_scaled = pd.DataFrame(df_others_scaled, columns=columnas_importantes[1:-4])
    df_scaled['precio'] = df_importante['precio_escalado']
    df_scaled['identificador'] = df_importante['identificador'].values

    # Título de la aplicación
    st.title('Comparativa de Inmuebles')

    # Filtro de ubicaciones
    ubicaciones = st.multiselect('En qué ubicaciones quieres buscar',df['ubicacion'].unique(), placeholder= 'Selecciona una o varias ubicaciones')

    # Filtrar el DataFrame por ubicaciones seleccionadas
    if ubicaciones:
        df_filtrado = df[df['ubicacion'].isin(ubicaciones)]
    else:
        df_filtrado = df

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
        'identificador', 'nombre', 'ubicacion', 'precio', 'precio_m2',
        'superficie', 'superficie_construida', 'superficie_util', 'planta',
        'habitaciones', 'baños', 'href'
    ]
    df_comparativo = df_comparativo[columnas_ordenadas]

    st.write('Comparativa de características originales:')
    st.dataframe(df_comparativo)
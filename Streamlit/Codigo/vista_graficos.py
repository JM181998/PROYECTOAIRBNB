import streamlit as st
import matplotlib.pyplot as plt
from cargar_datos import cargar_datos

    #if st.button("⬅️ Volver"):
        #os._exit(0)
#revisar cargar datos
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

def vista_graficos():
    st.sidebar.title("Navegación")
    if st.sidebar.button("Página Principal"):
        st.session_state.page = "primera_pagina"
    if st.sidebar.button("Vista Detallada"):
        st.session_state.page = "vista_detallada"

    #st.title("Vista de Gráficos")
    #st.write("Aquí puedes aplicar filtros, ver el mapa y el dashboard.")
    # Añadir debajo el código para los filtros, mapa etc..

    #st.subheader("Distribución de precios")
    #fig, ax = plt.subplots(figsize=(4, 3))
    #ax.hist(df['precio'], bins=20, color='skyblue')
    #st.pyplot(fig)

    #st.subheader("Distribución de precios")
    #fig, ax = plt.subplots(figsize=(4, 3))
    #ax.hist(df['superficie'], bins=20, color='skyblue')
    #st.pyplot(fig)

    if 'antiguedad' in df.columns and 'precio' in df.columns:
        # Eliminar valores nulos
        df_filtered = df.dropna(subset=['antiguedad', 'precio'])

        # Contar la media de precio por categoría de antigüedad
        precio_promedio = df_filtered.groupby('antiguedad')['precio'].mean().sort_index()

        # Mostrar los datos en Streamlit
        st.write("### Precio Promedio por Antigüedad")
        st.dataframe(precio_promedio)

        # Graficar con Matplotlib
        fig, ax = plt.subplots(figsize=(12, 6))
        precio_promedio.plot(kind='bar', ax=ax)
        ax.set_title('Relación entre Precio Promedio y Antigüedad')
        ax.set_xlabel('Antigüedad')
        ax.set_ylabel('Precio Promedio')
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        plt.tight_layout()

        # Mostrar la gráfica en Streamlit
        st.pyplot(fig)
    else:
        st.error("Las columnas 'antiguedad' o 'precio' no existen en el DataFrame.")
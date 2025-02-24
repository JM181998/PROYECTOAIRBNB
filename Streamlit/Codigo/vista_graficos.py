import streamlit as st
import matplotlib.pyplot as plt
from cargar_datos import cargar_datos

    #if st.button("⬅️ Volver"):
        #os._exit(0)
#revisar cargar datos
df = cargar_datos()
df = df.dropna(subset=['precio'])

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
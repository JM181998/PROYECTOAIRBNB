import streamlit as st
import matplotlib.pyplot as plt

    #if st.button("⬅️ Volver"):
        #os._exit(0)
#revisar cargar datos
def vista_graficos():
    st.sidebar.title("Navegación")
    if st.sidebar.button("Página Principal"):
        st.session_state.page = "primera_pagina"
    if st.sidebar.button("Vista Detallada"):
        st.session_state.page = "vista_detallada"

    st.title("Vista de Gráficos")
    st.write("Aquí puedes aplicar filtros, ver el mapa y el dashboard.")
    # Añadir debajo el código para los filtros, mapa etc..

    st.subheader("Distribución de precios")
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.hist(df['precio'], bins=20, color='skyblue')
    st.pyplot(fig)

    st.subheader("Distribución de precios")
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.hist(df['superficie'], bins=20, color='skyblue')
    st.pyplot(fig)
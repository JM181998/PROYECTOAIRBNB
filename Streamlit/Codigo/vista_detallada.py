import streamlit as st


def vista_detallada():
    st.sidebar.title("Navegación")
    if st.sidebar.button("Página Principal"):
        st.session_state.page = "primera_pagina"
    if st.sidebar.button("Vista de Gráficos"):
        st.session_state.page = "vista_graficos"

    st.title("Vista Detallada")
    st.write("Busca y compara inmuebles.")
    # Añadir debajo el código para la búsqueda y comparación de inmuebles
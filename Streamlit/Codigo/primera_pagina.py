import streamlit as st

def primera_pagina():
    st.sidebar.title("Navegación")
    if st.sidebar.button("Vista de Presentación de Datos"):
        st.session_state.page = "vista_graficos"
    if st.sidebar.button("Vista Detallada"):
        st.session_state.page = "vista_detallada"

    st.title("Bienvenidos a nuestro página de analisis de inmuebles con pisos.com")
    st.write("Esta pagina permite visualizar los datos de diferentes inmuebles en toda España.")


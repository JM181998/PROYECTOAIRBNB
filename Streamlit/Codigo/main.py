import streamlit as st
from CargarDatos import cargar_datos
from grafica import mostrar_graficas

# Configuración de la app
st.set_page_config(
    page_title="Pisos.com",
    layout="wide"
)

# Cargar datos
df = cargar_datos()

# Mostrar gráficas
mostrar_graficas(df)

st.sidebar.title("Menú de navegación")
st.sidebar.page_link("pages/filtros.py", label="Filtros y Dashboard")
st.sidebar.page_link("pages/comparacion.py", label="Comparación de Inmuebles")
import streamlit as st
from cargar_datos import cargar_datos
from vista_graficos import vista_graficos
from primera_pagina import primera_pagina
from vista_detallada import vista_detallada

# Configuración de la app
st.set_page_config(
    page_title="Pisos.com",
    layout="wide"
)

# Cargar datos
df = cargar_datos()


#st.sidebar.title("Menú de navegación")
#st.sidebar.page_link("pages/filtros.py", label="Filtros y Dashboard")
#st.sidebar.page_link("pages/comparacion.py", label="Comparación de Inmuebles")

if 'page' not in st.session_state:
    st.session_state.page = 'primera_pagina'

if st.session_state.page == 'primera_pagina':
    primera_pagina()
elif st.session_state.page == 'vista_graficos':
    vista_graficos()
elif st.session_state.page == 'vista_detallada':
    vista_detallada()
import streamlit as st
from PIL import Image

def main():
    st.set_page_config(page_title="Análisis de Datos de Pisos.com", layout="wide")

    # Sidebar
    st.sidebar.title("Navegación")
    page = st.sidebar.selectbox("Selecciona una página",
                                ["Página Principal", "Exploratory Data Analysis", "Comparador de pisos", "Clustering",
                                 "Clasificación", "Regresión", "Base de Datos", "About Us"])

    # Página Principal
    if page == "Página Principal":
        # Añadir imagen de titulo
        #image = Image.open('app/images/logo.png')
        #st.image(image, caption='Análisis de Datos de Pisos.com', use_container_width=True)

        st.title("Análisis de Datos de Pisos.com")

        st.markdown("""
            ## Bienvenido a la App de Análisis de Datos de Pisos.com
            Esta aplicación está diseñada para proporcionar un análisis exhaustivo de los datos de compra, venta y alquiler de propiedades en la página Pisos.com. A continuación, se presenta una breve descripción de las secciones disponibles en la app:

            ### Secciones de la App
            - **Exploratory Data Analysis**: Visualizaciones y análisis exploratorio de los datos.
            - **Comparador de pisos**: Herramienta que nos permite comparar dos inmuebles de forma interactiva.
            - **Clustering**: Modelos de clustering que agrupan las propiedades según sus características.
            - **Clasificación**: Modelos de clasificación que asignan una propiedad a un grupo definido por el modelo de clustering.
            - **Regresión**: Modelos de regresión que calculan el posible valor de una propiedad.
            - **Base de Datos**: Descripción de la arquitectura de la base de datos utilizada en el proyecto.
            - **About Us**: Información sobre los integrantes del proyecto, con enlaces a LinkedIn y Github.

            ### Cómo Navegar
            Utiliza el menú de la izquierda para navegar entre las diferentes secciones de la app. Cada sección contiene visualizaciones interactivas y explicaciones detalladas para ayudarte a entender mejor los datos y los modelos utilizados.

            ### Objetivo del Proyecto
            El objetivo de este proyecto es proporcionar una herramienta interactiva y fácil de usar para analizar los datos de propiedades en Pisos.com, ayudando a los usuarios a tomar decisiones informadas sobre compra, venta y alquiler de propiedades.

            ¡Esperamos que disfrutes explorando los datos y modelos en esta app!
            """)

    # Exploratory Data Analysis
    elif page == "Exploratory Data Analysis":
        st.title("Exploratory Data Analysis")
        st.markdown("Aquí se mostrarán las visualizaciones y funcionalidades de las gráficas propuestas en el SPRINT I.")

    # Comparador de pisos
    elif page == "Comparador de pisos":
        st.title("Comparador de pisos")
        st.markdown("Aquí se mostrará una herramienta de comparación entre dos inmuebles de forma interactiva.")

    # Clustering
    elif page == "Clustering":
        st.title("Clustering")
        st.markdown("Aquí se expondrán los modelos de clustering que agrupan las acciones según sus características.")

    # Clasificación
    elif page == "Clasificación":
        st.title("Clasificación")
        st.markdown("Aquí se expondrán los modelos de clasificación que clasifican un piso a un grupo definido por el modelo de clustering.")

    # Regresión
    elif page == "Regresión":
        st.title("Regresión")
        st.markdown("Aquí se expondrán los modelos de regresión que calculan el posible valor de un piso/casa.")

    # Base de Datos
    elif page == "Base de Datos":
        st.title("Base de Datos")
        st.markdown("Aquí se mostrará la arquitectura de la base de datos implementada en el proyecto, explicando la utilidad de cada tabla y el significado de cada columna.")

    # About Us
    elif page == "About Us":
        st.title("About Us")
        st.markdown("Información de los integrantes del proyecto, enlaces a LinkedIn y Github.")

if __name__ == "__main__":
    main()
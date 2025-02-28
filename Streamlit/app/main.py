import streamlit as st
from PIL import Image
from pages import home, eda, comparador, clustering, classification, regression, database, about_us


def main():
    st.set_page_config(page_title="Análisis de Datos de Pisos.com", layout="wide")

    # Sidebar
    st.sidebar.title("Navegación")
    page = st.sidebar.selectbox("Selecciona una página",
                                ["Página Principal", "Exploratory Data Analysis", "Comparador de pisos", "Clustering",
                                 "Clasificación", "Regresión", "Base de Datos", "About Us"])

    # Página Principal
    if page == "Página Principal":
        home.main()

    # Exploratory Data Analysis
    elif page == "Exploratory Data Analysis":
        eda.main()

    # Comparador de pisos
    elif page == "Comparador de pisos":
        comparador.main()

    # Clustering
    elif page == "Clustering":
        clustering.main()

    # Clasificación
    elif page == "Clasificación":
        classification.main()

    # Regresión
    elif page == "Regresión":
        regression.main()

    # Base de Datos
    elif page == "Base de Datos":
        database.main()

    # About Us
    elif page == "About Us":
        about_us.main()


if __name__ == "__main__":
    main()
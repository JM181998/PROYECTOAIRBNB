import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
import folium
import geopandas as gpd
import json

def eda_page():
    st.title("Vista de Gráficos")
    st.write("Aquí puedes ver la presentación de los datos obtenidos y como se relacionan entre sí.")
    #MAPA COROPLÉTICO
    def mapa_coropletico(file_path):
        st.markdown("## Mapa Coroplético de Pisos/Casas en alquiler por Provincia")
        # Cargamos el archivo GeoJSON de las provincias de España
        geojson_path = "data/spanish_provinces.geojson"
        with open(geojson_path, 'r') as f:
            geojson_data = json.load(f)
        gdf_spain = gpd.GeoDataFrame.from_features(geojson_data["features"])
        # Cargamos el archivo CSV
        df = pd.read_csv(file_path, low_memory=False)
        # Agrupamos por provincia y contamos el número de pisos/casas
        df_grouped = df.groupby('provincia').size().reset_index(name='counts')
        # Creamos un diccionario de mapeo para asegurarnos de que coincidan los nombres de las provincias en ambos archivos
        mapping = {
            'A Coruña': 'A Coruña',
            'Alava': 'Araba',
            'Albacete': 'Albacete',
            'Alicante': 'Alacant',
            'Almeria': 'Almería',
            'Asturias': 'Asturias',
            'Avila': 'Ávila',
            'Badajoz': 'Badajoz',
            'Barcelona': 'Barcelona',
            'Burgos': 'Burgos',
            'Caceres': 'Cáceres',
            'Cadiz': 'Cádiz',
            'Cantabria': 'Cantabria',
            'Castellon': 'Castelló',
            'Ciudad Real': 'Ciudad Real',
            'Cordoba': 'Córdoba',
            'Cuenca': 'Cuenca',
            'Girona': 'Girona',
            'Granada': 'Granada',
            'Guadalajara': 'Guadalajara',
            'Guipuzcoa': 'Gipuzcoa',
            'Huelva': 'Huelva',
            'Huesca': 'Huesca',
            'Islas Baleares': 'Illes Balears',
            'Jaen': 'Jaén',
            'La Rioja': 'La Rioja',
            'Las Palmas': 'Las Palmas',
            'Leon': 'León',
            'Lleida': 'Lleida',
            'Lugo': 'Lugo',
            'Madrid': 'Madrid',
            'Malaga': 'Málaga',
            'Melilla': 'Melilla',
            'Murcia': 'Murcia',
            'Navarra': 'Navarra',
            'Ourense': 'Ourense',
            'Palencia': 'Palencia',
            'Pontevedra': 'Pontevedra',
            'Salamanca': 'Salamanca',
            'Santa Cruz de Tenerife': 'Santa Cruz de Tenerife',
            'Segovia': 'Segovia',
            'Sevilla': 'Sevilla',
            'Soria': 'Soria',
            'Tarragona': 'Tarragona',
            'Teruel': 'Teruel',
            'Toledo': 'Toledo',
            'Valencia': 'València',
            'Valladolid': 'Valladolid',
            'Vizcaya': 'Bizkaia',
            'Zamora': 'Zamora',
            'Zaragoza': 'Zaragoza'
        }
        # Normalizar los nombres de las provincias en ambos DataFrames y aplicar el mapeo
        gdf_spain['provincia_normalized'] = gdf_spain['provincia'].map(mapping)
        df_grouped['provincia_normalized'] = df_grouped['provincia'].map(mapping)
        # Unimos los datos con el GeoDataFrame
        gdf_spain = gdf_spain.merge(df_grouped, left_on='provincia_normalized', right_on='provincia_normalized', how='left')
        # Creamos el mapa coroplético con Folium
        m = folium.Map(location=[40.416775, -3.703790], zoom_start=6)

        folium.Choropleth(
            geo_data=geojson_data,
            name='choropleth',
            data=df_grouped,
            columns=['provincia_normalized', 'counts'],
            key_on='feature.properties.provincia',
            fill_color='Oranges',
            fill_opacity=0.9,
            line_opacity=0.2,
            legend_name='Cantidad de pisos/casas en alquiler por provincia'
        ).add_to(m)

        folium.LayerControl().add_to(m)
        # Renderizamos el mapa directamente en Streamlit
        st.components.v1.html(m._repr_html_(), height=600)
    mapa_coropletico("data/compras_completo_limpio.csv")

    #ANALISIS DE OULIERS EN PRECIO
    def analizar_outliers_precio(file_path):
        st.markdown("## Análisis de outliers en columna precio de los alquileres")
        # Cargamos el archivo CSV
        df = pd.read_csv(file_path, low_memory=False)
        # Transformamos la columna precio a su valor logarítmico
        df['log_precio'] = np.log(df['precio'])
        # Calculamos el Z-Score e identificamos outliers
        df['z_score'] = (df['log_precio'] - df['log_precio'].mean()) / df['log_precio'].std()
        df['outlier'] = df['z_score'].apply(lambda x: 'Outlier' if np.abs(x) > 3 else 'Normal')
        # Creamos el histograma con Plotly
        fig = px.histogram(df, x='log_precio', color='outlier', title='Histograma de Precios Logarítmicos con Outliers',
                           color_discrete_map={'Outlier': 'red', 'Normal': 'green'})
        fig.update_layout(
            xaxis_title='Precio Logarítmico',
            yaxis_title='Frecuencia'
        )
        st.plotly_chart(fig)
    analizar_outliers_precio("data/compras_completo_limpio.csv")


if __name__ == "__main__":
    eda_page()
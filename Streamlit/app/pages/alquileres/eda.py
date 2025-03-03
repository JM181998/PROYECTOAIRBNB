import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
import folium
import geopandas as gpd
import json

#df = pd.read_csv("data/alquileres_completo_limpio.csv", low_memory=False)
#df = df.dropna(subset=['precio'])
## Identificar y eliminar outliers
#Q1 = df['precio'].quantile(0.05)
#Q3 = df['precio'].quantile(0.95)
#IQR = Q3 - Q1
#filtro = (df['precio'] >= (Q1 - 1.5 * IQR)) & (df['precio'] <= (Q3 + 1.5 * IQR))
#df = df[filtro]
#df = df[df['precio'] >= 10]

# Eliminar filas donde el valor de la columna agencia sea "Agencia no disponible"
#df = df[df['agencia'] != "Agencia no disponible"]

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
    mapa_coropletico("data/alquileres_completo_limpio.csv")

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
    analizar_outliers_precio("data/alquileres_completo_limpio.csv")

    ##FRAN
    def scatter_segmentado(df, x, y, segmentar_por):
        ubicaciones = df[segmentar_por].unique()
        fig, ax = plt.subplots(figsize=(10, 6))

        for ubicacion in ubicaciones:
            subset = df[df[segmentar_por] == ubicacion]
            ax.scatter(subset[x], subset[y], label=ubicacion, alpha=0.7)

        ax.set_title(f'Relación entre {y} y {x} segmentado por {segmentar_por}')
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.legend(title=segmentar_por, bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()

        # Mostrar gráfico en Streamlit
        st.pyplot(fig)

    scatter_segmentado(df, 'superficie_construida', 'precio', 'comunidad_autonoma')

    st.write("### Conclusiones del análisis de precio vs. superficie construida por comunidad autonoma")
    st.write("Concentración en rangos bajos: La mayoría de las propiedades tienen superficies menores a 200 m² y precios inferiores a 10,000€")
    st.write("Valores atípicos: Existen algunas propiedades con precios muy elevados (hasta 80,000€) y grandes superficies (+600 m²)")
    st.write("Tendencia positiva: En general, el precio tiende a aumentar con la superficie construida, aunque con gran dispersión")
    st.write("Diferencias entre comunidadautonoma: Regiones como Madrid, Cataluña e Islas Baleares presentan precios más elevados en comparación con otras comunidades.")
    st.write("Mercado heterogéneo: Aunque la relación precio-superficie es clara, otros factores como ubicación")

    ##ENRIQUE
    if 'antiguedad' in df.columns and 'precio' in df.columns:
        # Eliminar valores nulos
        df_filtered = df.dropna(subset=['antiguedad', 'precio'])

        # Contar la media de precio por categoría de antigüedad
        precio_promedio = df_filtered.groupby('antiguedad')['precio'].mean()

        # Orden deseado de las columnas
        columnas_ordenadas = [
            "Menos de 5 años", "Entre 5 y 10 años", "Entre 10 y 20 años",
            "Entre 20 y 30 años", "Entre 30 y 50 años", "Más de 50 años"
        ]

        # Reindexar el DataFrame para que siga el orden deseado
        precio_promedio = precio_promedio.reindex(columnas_ordenadas)

        # Mostrar los datos en Streamlit
        ##st.write("### Precio Promedio por Antigüedad")
        #st.dataframe(precio_promedio)

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

    st.write("### Conclusiones sobre la relacion precio/antigüedad ")
    st.write("En mi opinion respondiendo a la pregunta de punto 4 no existe una relacion clara entre precio y antiguedad, ademas que los años van en ragons de 10 o 20 años, pero parece ser que va la relacion del precio va mas en su ubicacion o tamaño de todos modos cuando nos reunamos lo miramos todos")


    ##JUANMA
    st.write("### Analisis de las agencias en el mercado de alquileres")



    st.write("¿Qué agencia tiene en los pisos mas caros y los mas baratos?")
    # Agrupar por agencia y calcular precios mínimos y máximos
    precios_por_agencia = df.groupby('agencia')['precio']
    precio_min_agencia = precios_por_agencia.min()
    precio_max_agencia = precios_por_agencia.max()

    # Identificar la agencia más barata y la más cara
    agencia_mas_barata = precio_min_agencia.idxmin()
    agencia_mas_cara = precio_max_agencia.idxmax()

    # Calcular el precio medio total
    precio_medio_total = df['precio'].mean()

    # Mostrar resultados en Streamlit
    st.write(f"Agencia con el precio más barato: {agencia_mas_barata} con un precio de {precio_min_agencia.min()}")
    st.write(f"Agencia con el precio más caro: {agencia_mas_cara} con un precio de {precio_max_agencia.max()}")
    st.write(f"Precio medio total de todos los pisos: {precio_medio_total}")

    # Filtrar las 10 agencias con los precios más bajos y las 10 con los precios más altos
    top_10_baratas = precio_min_agencia.nsmallest(10)
    top_10_caras = precio_max_agencia.nlargest(10)

    # Crear un DataFrame con las agencias filtradas
    # Crear un DataFrame con las agencias filtradas para precios más bajos
    precios_baratos_filtrados = pd.DataFrame({
        'Precio Mínimo': top_10_baratas
    })

    # Crear un DataFrame con las agencias filtradas para precios más altos
    precios_caros_filtrados = pd.DataFrame({
        'Precio Máximo': top_10_caras
    })

    # Crear gráfico de barras para precios más bajos
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    precios_baratos_filtrados.plot(kind='bar', ax=ax1)

    # Personalizar gráfico
    plt.title('Top 10 Precios más baratos por Agencia')
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.2, top=0.85)

    # Mostrar gráfico en Streamlit
    st.pyplot(fig1)

    # Crear gráfico de barras para precios más altos
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    precios_caros_filtrados.plot(kind='bar', ax=ax2)

    # Personalizar gráfico
    plt.title('Top 10 Precios más caros por Agencia')
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.2, top=0.85)

    # Mostrar gráfico en Streamlit
    st.pyplot(fig2)

    st.write("Agencias y cantidad de inmuebles")

    # Filtrar agencias con más de 50 inmuebles
    inmuebles_por_agencia = df.groupby('agencia').filter(lambda x: x['identificador'].nunique() > 50)
    inmuebles_df = inmuebles_por_agencia.groupby('agencia')['identificador'].nunique().reset_index()
    inmuebles_df.columns = ['agencia', 'cantidad_inmuebles']
    inmuebles_df = inmuebles_df.sort_values(by='cantidad_inmuebles', ascending=False)


    # Crear gráfico de barras
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=inmuebles_df, x='agencia', y='cantidad_inmuebles', ax=ax)
    ax.set_title('Cantidad de Inmuebles por Agencia (Ordenado de Mayor a Menor)')
    ax.set_ylabel('Cantidad de Inmuebles')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    plt.tight_layout()

    # Mostrar gráfico en Streamlit
    st.pyplot(fig)


if __name__ == "__main__":
    eda_page()
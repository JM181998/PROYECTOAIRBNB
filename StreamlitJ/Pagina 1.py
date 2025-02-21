import streamlit as st

import numpy as np
import pandas as pd
import requests

def main():
    # Title
    st.title("ANALISIS INMOBILIARIO CON PISOS.COM")

    # Text
    st.text("Bienvenidos a nuestra página de análisis inmobiliario con Pisos.com.")
    st.text("Esta página será la muestra de nuestro PFB")
    name = "Jorge Gazulla"

    # # Header
    st.header("Header1")

    # # Subheader
    st.subheader("Subheader1")

    # # Markdown
    st.markdown("# This is markdown.")

    # # Display Colored Text/Boostraps Alert
    #st.success("success")
    #st.warning("warning")
    #st.info("info")
    #st.error("error")
    ##st.exception("exception.")

    # .write()
    st.write("Normal Text.")
    st.write("## This is a markdown text")
    #st.write(1 + 2)

    # # Help
    #st.help(range)

    # Display Data
    df = pd.read_csv(filepath_or_buffer="sources/alquileres_scrap_completo.csv")
    df = df.iloc[:, 1:]

    # Dinamic Data
    st.dataframe(df)
    #st.write(df)

    # Static Table
    #st.table(df)

    # Adding Color
    #st.dataframe(df.select_dtypes(include=np.number).style.highlight_max(axis = 0))

    # Display JSON
    #endpoint = "https://api.frankfurter.app/latest"
    #response = requests.get(url=endpoint)
    #st.json(response.json())

    # # Display Code
    # code = """
    # def func():
    #     return x**2
    # """
    # st.code(body = code, language = "python")

    pass


if __name__ == "__main__":
    main()

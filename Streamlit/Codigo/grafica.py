import streamlit as st
import matplotlib.pyplot as plt

def mostrar_graficas(df):
    st.subheader("Distribución de precios")
    fig, ax = plt.subplots()
    ax.hist(df['precio'], bins=20, color='skyblue')
    st.pyplot(fig)
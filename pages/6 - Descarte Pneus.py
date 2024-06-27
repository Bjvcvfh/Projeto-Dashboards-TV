import streamlit as st
import pandas as pd
import locale
import plotly.express as px

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

st.set_page_config(
    layout="wide",
    page_title="Compras de Pneu"
)

df = pd.read_csv("consultas/descarte_pneu.csv", sep=';', encoding='utf-8-sig')

#Altera o campo para data
df['Data Desc'] = pd.to_datetime(df['Data Desc'], format='%d/%m/%Y')
df['Ano'] = df['Data Desc'].dt.year
df['Qtd'] = 1

#Filtros de ano
filtro_2023 = df[df['Ano'] == 2023]
filtro_2024 = df[df['Ano'] == 2024] 

#Grafico descartes 2023
st.markdown("<h2 style='text-align: center; color: black;'>Descarte de Pneus 2023</h2>", unsafe_allow_html=True)
fig = px.pie(filtro_2023, values='Qtd', names='TAMANHO')
st.plotly_chart(fig)

#Grafico modelos 2023
st.markdown("<h2 style='text-align: center; color: black;'>Descrição de Descartes 2023</h2>", unsafe_allow_html=True)
fig = px.histogram(filtro_2023, x='Qtd', y='MOTIVO', text_auto='.0f')
fig.update_layout(yaxis={'categoryorder':'total ascending'})
fig.update_traces(textangle=0)
st.plotly_chart(fig)

#Grafico descartes 2024
st.markdown("<h2 style='text-align: center; color: black;'>Descarte de Pneus 2024</h2>", unsafe_allow_html=True)
fig = px.pie(filtro_2024, values='Qtd', names='TAMANHO')
st.plotly_chart(fig)

#Grafico modelos 2024
st.markdown("<h2 style='text-align: center; color: black;'>Descrição de Descartes 2024</h2>", unsafe_allow_html=True)
fig = px.histogram(filtro_2024, x='Qtd', y='MOTIVO', text_auto='.0f')
fig.update_layout(yaxis={'categoryorder':'total ascending'})
fig.update_traces(textangle=0)
st.plotly_chart(fig)

import streamlit as st
import pandas as pd
import locale
import plotly.express as px

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

st.set_page_config(
    layout="wide",
    page_title="Compras de Pneu"
)

df = pd.read_csv("consultas/compra_pneu.csv", sep=';', encoding='latin-1')
df2 = pd.read_csv("consultas/posicao_pneu.csv", sep =';', encoding='latin-1')

#Altera o campo para data
df['DT Digitacao'] = pd.to_datetime(df['DT Digitacao'], format='%d/%m/%Y')
df['Ano'] = df['DT Digitacao'].dt.year

# Convertendo a coluna 'Codigo Pneu' para strings e removendo os zeros à esquerda
df2['Codigo Pneu'] = df2['Codigo Pneu'].astype(str).str.lstrip('0')
df2['Qtd'] = 1

#Mapeamento dos nomes das posições dos pneus
map = {
        '1D': '1° EIXO LADO DIREITO',
        '1EDE': 'PRIMEIRO EIXO DIREITO EXTERNO',
        '1EDI': 'PRIMEIRO EIXO DIREITO INTERNO',
        '1EEE': 'PRIMEIRO EIXO ESQUERDO EXTERNO',
        '1EEI':	'PRIMEIRO EIXO ESQUERDO INTERNO',
        '2DD':	'SEGUNDO EIXO DIANTEIRO DIREITO',
        '2DE':	'SEGUNDO EIXO DIANTEIRO ESQUERDO',
        '2EDE':	'SEGUNDO EIXO DIREITO EXTERNO',
        '2EDI':	'SEGUNDO EIXO DIREITO INTERNO',
        '2EEE':	'SEGUNDO EIXO ESQUERDO EXTERNO',
        '2EEI':	'SEGUNDO EIXO ESQUERDO INTERNO',
        '3EDE':	'TERCEIRO EIXO DIREITO EXTERNO',
        '3EDI':	'TERCEIRO EIXO DIREITO INTERNO',
        '3EEE':	'TERCEIRO EIXO ESQUERDO EXTERNO',
        '3EEI':	'TERCEIRO EIXO ESQUERDO INTERNO',
        '4EDE':	'QUARTO EIXO DIREITO EXTERNO',
        '4EDI':	'QUARTO EIXO DIREITO INTERNO',
        '4EEE':	'QUARTO EIXO ESQUERDO EXTERNO',
        '4EEI':	'QUARTO EIXO ESQUERDO INTERNO',
        'DD':	'DIANTEIRO DIREITO',
        'DDE':	'DIANTEIRO DIREITO EXTERNO',
        'DDI':	'DIANTEIRO DIREITO INTERNO',
        'DE':	'DIANTEIRO ESQUERDO',
        'DEE':	'DIANTEIRO ESQUERDO EXTERNO',
        'DEI':	'DIANTEIRO ESQUERDO INTERNO',
        'TD':	'TRASEIRO DIREITO',
        'TDE':	'TRACAO DIREITA EXTERNA',
        'TDI':	'TRACAO DIREITA INTERNA',
        'TE':	'TRASEIRO ESQUERDO',
        'TEE':	'TRACAO ESQUERDA EXTERNA',
        'TEI':	'TRACAO ESQUERDA INTERNA',
        'TK001': 'TERCEIRO EIXO LIVRE',
        'TKDE':	'TRUCK  DIREITO EXTERNO',
        'TKDI':	'TRUCK DIREITO INTERNO',
        'TKEE':	'TRUCK ESQUERDO EXTERNO',
        'TKEI':	'TRUCK ESQUERDO INTERNO'    
}

#Trocando pelo dicionario
df2['Posicao Pneu'] = df2['Posicao Pneu'].replace(map)
#Selecionando os dados que quero
df2_filtrada = df2[df2['Codigo Pneu'] > '9607'][['Codigo Pneu' , 'Placa Veicul', 'Posicao Pneu']]
df2_filtrada2024 = df2[df2['Codigo Pneu'] > '9607'][['Codigo Pneu' , 'Placa Veicul', 'Posicao Pneu', 'Qtd']]

#Filtros de ano
filtro_2023 = df[df['Ano'] == 2023]
filtro_2024 = df[df['Ano'] == 2024] 

#Grafico modelos 2023
st.markdown("<h2 style='text-align: center; color: black;'>Porcentagem de Compras 2023</h2>", unsafe_allow_html=True)
fig = px.pie(filtro_2023, values='Quantidade', names='Descr Prod')
st.plotly_chart(fig)

#Grafico de pneus por placa 2023

#Grafico modelos 2023
st.markdown("<h2 style='text-align: center; color: black;'>Total de Compras 2023</h2>", unsafe_allow_html=True)
fig = px.histogram(filtro_2023, x='Vlr.Total', y='Descr Prod', text_auto='.2s')
fig.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig)

#Grafico modelos 2024
st.markdown("<h2 style='text-align: center; color: black;'>Porcentagem de Compras 2024</h2>", unsafe_allow_html=True)
fig = px.pie(filtro_2024, values='Quantidade', names='Descr Prod')
st.plotly_chart(fig)

#Grafico de pneus por placa 2024
st.markdown("<h2 style='text-align: center; color: black;'>Aplicação dos Pneus 2024</h2>", unsafe_allow_html=True)
fig = px.histogram(df2_filtrada2024, x='Placa Veicul', y='Qtd', text_auto='.0f')
fig.update_layout(xaxis={'categoryorder':'total descending'})
st.plotly_chart(fig)

df2_filtrada

#Grafico modelos 2024
st.markdown("<h2 style='text-align: center; color: black;'>Total de Compras 2024</h2>", unsafe_allow_html=True)
fig = px.histogram(filtro_2024, x='Vlr.Total', y='Descr Prod', text_auto='.2s')
fig.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig)

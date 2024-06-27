import streamlit as st
import pandas as pd
import locale
import altair as alt
import plotly.express as px

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

st.set_page_config(
    layout="wide",
    page_title="App Meu Checklist"
)

df = pd.read_csv("consultas/checklist.txt", sep=',')
df1 = pd.read_csv("consultas/checklist1.txt", sep=',')

# Gráfico de barras uso por motorista
grafico_motorista = alt.Chart(df1).mark_bar().encode(
    x=alt.X('Motorista:N', axis=alt.Axis(title='Motorista'.upper())),
    y=alt.Y('Quantidade:Q', axis=alt.Axis(title='Quantidade total'.upper()), scale=alt.Scale(domain=[0, 30])),
        ).interactive()

# Adiciona rótulos de dados com o total de cada motorista
rótulos_motorista = alt.Chart(df1).mark_text(
    align='center',
    baseline='middle',
    dx=0,
    dy=-7,  # Ajuste para posicionar o texto acima das barras
    fontSize=14  # Define o tamanho da fonte do rótulo
).encode(
    x=alt.X('Motorista:N'),
    y=alt.Y('Quantidade:Q'),
    text=alt.Text('Quantidade:Q', format='.0f')  # Formata o texto para exibir números inteiros
)

st.markdown("<h2 style='text-align: center; color: black;'>Usos do App Meu Checklist</h2>", unsafe_allow_html=True)
fig = px.pie(df, values='Quantidade', names='Tipo')
st.plotly_chart(fig)

# Junta o gráfico de barras e o rótulo
grafico_final_motorista = (grafico_motorista + rótulos_motorista).properties(width=600, height=400)

# Junta o gráfico de barras e o rótulo
st.markdown("<h2 style='text-align: center; color: black;'>Quantidade por Motorista</h2>", unsafe_allow_html=True)

#Mostra o gráfico
st.altair_chart(grafico_final_motorista, use_container_width=True)
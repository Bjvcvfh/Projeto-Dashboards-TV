import streamlit as st
import altair as alt
import locale
import pandas as pd
import plotly.express as px

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

st.set_page_config(
    layout="wide",
    page_title="Consumo Lavagem"
)

df = pd.read_csv("consultas/stl.csv", encoding='latin-1', sep=';')

#Altera o campo para data
df['Data Inicio'] = pd.to_datetime(df['Data Inicio'], format='%d/%m/%Y')
df['Ano'] = df['Data Inicio'].dt.year
df['Mes'] = df['Data Inicio'].dt.month

#Filtra o tipo real
filtro = df[df['Tipo'] == 'REAL']
filtro = filtro[filtro['Tipo Insumo'] == "Produto"]
filtro_2023 = filtro[filtro['Ano'] == 2023]
filtro_2024 = filtro[filtro['Ano'] == 2024]

#Faz aparecer somente 1 valor de cada tipo
produtos = filtro['Nome Insumo'].unique()

#Faz a selecbox com os produtos que foram filtrados
produto = st.selectbox('Nome Produto', produtos)
df_filtered = filtro[df['Nome Insumo'] == produto]

# Calcula o total de cada mês
total_por_mes = df_filtered.groupby(['Ano', 'Mes'])['Quantidade'].sum().reset_index(name='Total')
total_por_mes_2023 = total_por_mes[total_por_mes['Ano'] == 2023]
total_por_mes_2024 = total_por_mes[total_por_mes['Ano'] == 2024]

# Filtra os dados apenas para o ano de 2023
df_filtered_2023 = df_filtered[df_filtered['Ano'] == 2023]

# Filtra os dados apenas para o ano de 2024
df_filtered_2024 = df_filtered[df_filtered['Ano'] == 2024]

# Gráfico de barras mensal 2023
grafico_2023 = alt.Chart(df_filtered_2023).mark_bar().encode(
    x=alt.X('Mes:N', axis=alt.Axis(title='Mês'.upper())),
    y=alt.Y('Quantidade:Q', axis=alt.Axis(title='Quantidade'.upper()), scale=alt.Scale(domain=[0, 700])),
            ).interactive()

# Adiciona rótulos de dados com o total de cada mês 2023
rótulos_2023 = alt.Chart(total_por_mes_2023).mark_text(
    align='center',
    baseline='middle',
    dx=0,
    dy=-7,  # Ajuste para posicionar o texto acima das barras
    fontSize=14  # Define o tamanho da fonte do rótulo
).encode(   
    x=alt.X('Mes:N', axis=alt.Axis(title='Mês'.upper())),
    y=alt.Y('Total:Q'),
    text=alt.Text('Total:Q', format='.0f')  # Formata o texto para exibir números inteiros
)

# Gráfico de barras mensal 2024
grafico_2024 = alt.Chart(df_filtered_2024).mark_bar().encode(
    x=alt.X('Mes:N', axis=alt.Axis(title='Mês'.upper())),
    y=alt.Y('Quantidade:Q', axis=alt.Axis(title='Quantidade'.upper()), scale=alt.Scale(domain=[0, 700])),
            ).interactive()

# Adiciona rótulos de dados com o total de cada mês 2024
rótulos_2024 = alt.Chart(total_por_mes_2024).mark_text(
    align='center',
    baseline='middle',
    dx=0,
    dy=-7,  # Ajuste para posicionar o texto acima das barras
    fontSize=14  # Define o tamanho da fonte do rótulo
).encode(
    x=alt.X('Mes:N', axis=alt.Axis(title='Mês'.upper())),
    y=alt.Y('Total:Q'),
    text=alt.Text('Total:Q', format='.0f')  # Formata o texto para exibir números inteiros
)

# Junta o gráfico de barras e o rótulo mensal 2024
grafico_final_2023 = (grafico_2023 + rótulos_2023).properties(width=600, height=400)
grafico_final_2024 = (grafico_2024 + rótulos_2024).properties(width=600, height=400)

# Coluna 1
col1, col2 = st.columns(2)

# Título mensal alinhado com o gráfico mensal
with col1:
    st.markdown("<h2 style='text-align: center; color: black;'>Quantidade de Consumo Mensal 2023</h2>", unsafe_allow_html=True)
    col1.altair_chart(grafico_final_2023, use_container_width=True)
    
with col2:
    st.markdown("<h2 style='text-align: center; color: black;'>Quantidade de Consumo Mensal 2024</h2>", unsafe_allow_html=True)
    col2.altair_chart(grafico_final_2024, use_container_width=True)



st.markdown("<h2 style='text-align: center; color: black;'>Porcentagem de Consumo 2023</h2>", unsafe_allow_html=True)
fig = px.pie(filtro_2023, values='Quantidade', names='Nome Insumo')
st.plotly_chart(fig)
    
st.markdown("<h2 style='text-align: center; color: black;'>Porcentagem de Consumo 2024</h2>", unsafe_allow_html=True)
fig = px.pie(filtro_2024, values='Quantidade', names='Nome Insumo')
st.plotly_chart(fig)
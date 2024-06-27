import streamlit as st
import pandas as pd 
import locale
import altair as alt
import plotly.express as px

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

st.set_page_config(
    layout="wide",
    page_title="SD1 Lavadores"
)

df = pd.read_csv("consultas/sd1.csv", encoding='latin-1', sep=';')

#altera o nome da coluna Vlr.Total
df.rename(columns={'Vlr.Total': 'Totais'}, inplace=True)

#Altera o campo para data
df['DT Digitacao'] = pd.to_datetime(df['DT Digitacao'])
df['Ano'] = df['DT Digitacao'].dt.year
df['Mes'] = df['DT Digitacao'].dt.month

#Conta quantas vezes 'Descr Prod' aparece no csv
produtos = df['Descr Prod'].unique()

#Cria a selectbox de acordo com os nomes existentes
produto = st.selectbox('Nome Produto', produtos)
df_filtered = df[df['Descr Prod'] == produto]

#Filtro para porcentagem
filtro_2023 = df[df['Ano'] == 2023]
filtro_2024 = df[df['Ano'] == 2024]

# Calcula o total de cada mês
total_por_mes = df_filtered.groupby(['Ano', 'Mes'])['Quantidade'].sum().reset_index(name='Total')
total_por_mes_2023 = total_por_mes[total_por_mes['Ano'] == 2023]
total_por_mes_2024 = total_por_mes[total_por_mes['Ano'] == 2024]

# Calcula o custo de cada mês
total_custo = df_filtered.groupby(['Ano', 'Mes'])['Totais'].sum().reset_index(name='ValorTotal')
total_custo_2023 = total_custo[total_custo['Ano'] == 2023]
total_custo_2024 = total_custo[total_custo['Ano'] == 2024]

# Calcula o total de cada ano
total_por_ano = df_filtered.groupby(['Ano'])['Quantidade'].sum().reset_index(name='TotalAno')

# Calcula o custo total de cada ano
total_custo_ano = df_filtered.groupby(['Ano'])['Totais'].sum().reset_index(name='ValorTotalAno')

# Filtra os dados apenas para o ano de 2023
df_filtered_2023 = df_filtered[df_filtered['Ano'] == 2023]

# Filtra os dados apenas para o ano de 2024
df_filtered_2024 = df_filtered[df_filtered['Ano'] == 2024]

# Gráfico de barras mensal 2023
grafico_2023 = alt.Chart(df_filtered_2023).mark_bar(color='green').encode(
    x=alt.X('Mes:N', axis=alt.Axis(title='Mês'.upper())),
    y=alt.Y('Quantidade:Q', axis=alt.Axis(title='Quantidade'.upper()), scale=alt.Scale(domain=[0, 1200])),
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

# Gráfico de barras custo mensal 2023
grafico_custo_2023 = alt.Chart(df_filtered_2023).mark_bar(color='green').encode(
    x=alt.X('Mes:N', axis=alt.Axis(title='Mês'.upper())),
    y=alt.Y('Totais:Q', axis=alt.Axis(title='Custo'.upper()), scale=alt.Scale(domain=[0, 30000])),
            ).interactive()

# Adiciona rótulos de dados com o custo total de cada mês 2023
custo_2023 = alt.Chart(total_custo_2023).mark_text(
    align='center',
    baseline='middle',
    dx=0,
    dy=-7,  # Ajuste para posicionar o texto acima das barras
    fontSize=14  # Define o tamanho da fonte do rótulo
).encode(
    x=alt.X('Mes:N', axis=alt.Axis(title='Mês'.upper())),
    y=alt.Y('ValorTotal:Q'),
    text=alt.Text('ValorTotal:Q', format='$,.2f')  # Formata o texto para exibir moeda
)

# Gráfico de barras mensal 2024
grafico_2024 = alt.Chart(df_filtered_2024).mark_bar(color='green').encode(
    x=alt.X('Mes:N', axis=alt.Axis(title='Mês'.upper())),
    y=alt.Y('Quantidade:Q', axis=alt.Axis(title='Quantidade'.upper()), scale=alt.Scale(domain=[0, 1000])),
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

# Gráfico de barras custo mensal 2024
grafico_custo_2024 = alt.Chart(df_filtered_2024).mark_bar(color='green').encode(
    x=alt.X('Mes:N', axis=alt.Axis(title='Mês'.upper())),
    y=alt.Y('Totais:Q', axis=alt.Axis(title='Custo'.upper()), scale=alt.Scale(domain=[0, 30000])),
            ).interactive()

# Adiciona rótulos de dados com o custo total de cada mês 2024
custo_2024 = alt.Chart(total_custo_2024).mark_text(
    align='center',
    baseline='middle',
    dx=0,
    dy=-7,  # Ajuste para posicionar o texto acima das barras
    fontSize=14  # Define o tamanho da fonte do rótulo
).encode(
    x=alt.X('Mes:N', axis=alt.Axis(title='Mês'.upper())),
    y=alt.Y('ValorTotal:Q'),
    text=alt.Text('ValorTotal:Q', format='$,.2f')  # Formata o texto para exibir moeda
)

# Gráfico de barras anual
grafico_anual = alt.Chart(df_filtered).mark_bar(color='green').encode(
    x=alt.X('Ano:N', axis=alt.Axis(title='Ano'.upper())),
    y=alt.Y('Quantidade:Q', axis=alt.Axis(title='Quantidade'.upper()), scale=alt.Scale(domain=[0, 8000])),
            ).interactive()

# Adiciona rótulos de dados com o total de cada ano
rótulos_anual = alt.Chart(total_por_ano).mark_text(
    align='center',
    baseline='middle',
    dx=0,
    dy=-7,  # Ajuste para posicionar o texto acima das barras
    fontSize=14  # Define o tamanho da fonte do rótulo
).encode(
    x=alt.X('Ano:N', axis=alt.Axis(title='Ano'.upper())),
    y=alt.Y('TotalAno:Q'),
    text=alt.Text('TotalAno:Q', format='.0f')  # Formata o texto para exibir números inteiros
)

# Gráfico de barras custo anual
grafico_custo_anual = alt.Chart(df_filtered).mark_bar(color='green').encode(
    x=alt.X('Ano:N', axis=alt.Axis(title='Ano'.upper())),
    y=alt.Y('Totais:Q', axis=alt.Axis(title='Custo'.upper()), scale=alt.Scale(domain=[0, 70000])),
            ).interactive()

# Adiciona rótulos de dados com o custo total de cada ano
custo_anual = alt.Chart(total_custo_ano).mark_text(
    align='center',
    baseline='middle',
    dx=0,
    dy=-7,  # Ajuste para posicionar o texto acima das barras
    fontSize=14  # Define o tamanho da fonte do rótulo
).encode(
    x=alt.X('Ano:N', axis=alt.Axis(title='Ano'.upper())),
    y=alt.Y('ValorTotalAno:Q'),
    text=alt.Text('ValorTotalAno:Q', format='$,.2f')  # Formata o texto para exibir números inteiros
)

# Junta o gráfico de barras e o rótulo mensal 2024
grafico_final_2023 = (grafico_2023 + rótulos_2023).properties(width=600, height=400)
grafico_final_2024 = (grafico_2024 + rótulos_2024).properties(width=600, height=400)
grafico_final_custo2023 = (grafico_custo_2023 + custo_2023).properties(width=600, height=400)
grafico_final_custo2024 = (grafico_custo_2024 + custo_2024).properties(width=600, height=400)

# Coluna 1
col1, col2 = st.columns(2)

# Título mensal alinhado com o gráfico mensal
with col1:
    st.markdown("<h2 style='text-align: center; color: black;'>Quantidade de Compra Mensal 2023</h2>", unsafe_allow_html=True)
    col1.altair_chart(grafico_final_2023, use_container_width=True)
    
with col2:
    st.markdown("<h2 style='text-align: center; color: black;'>Quantidade de Compra Mensal 2024</h2>", unsafe_allow_html=True)
    col2.altair_chart(grafico_final_2024, use_container_width=True)

# Coluna 2
col3, col4 = st.columns(2) 

# Título mensal alinhado com o gráfico mensal de custos
with col3:
    st.markdown("<h2 style='text-align: center; color: black;'>Custo de Compra Mensal 2023</h2>", unsafe_allow_html=True)
    col3.altair_chart(grafico_final_custo2023, use_container_width=True)
    
with col4:
    st.markdown("<h2 style='text-align: center; color: black;'>Custo de Compra Mensal 2024</h2>", unsafe_allow_html=True)
    col4.altair_chart(grafico_final_custo2024, use_container_width=True)

grafico_final_anual = (grafico_anual + rótulos_anual).properties(width=600, height=400)
grafico_final_custoanual = (grafico_custo_anual + custo_anual).properties(width=600, height=400)

# Coluna 3
col5, col6 = st.columns(2)

# Título mensal alinhado com o gráfico mensal de quantidade e custos
with col5:
    st.markdown("<h2 style='text-align: center; color: black;'>Quantidade de Compra Anual</h2>", unsafe_allow_html=True)
    col5.altair_chart(grafico_final_anual, use_container_width=True)
    
with col6:
    st.markdown("<h2 style='text-align: center; color: black;'>Custo de Compra Anual</h2>", unsafe_allow_html=True)
    col6.altair_chart(grafico_final_custoanual, use_container_width=True)
    
st.markdown("<h2 style='text-align: center; color: black;'>Porcentagem do Valor das Compras 2023</h2>", unsafe_allow_html=True)
fig = px.pie(filtro_2023, values='Totais', names='Descr Prod')
st.plotly_chart(fig)
    
st.markdown("<h2 style='text-align: center; color: black;'>Porcentagem do Valor das Compras 2024</h2>", unsafe_allow_html=True)
fig = px.pie(filtro_2024, values='Totais', names='Descr Prod')
st.plotly_chart(fig)


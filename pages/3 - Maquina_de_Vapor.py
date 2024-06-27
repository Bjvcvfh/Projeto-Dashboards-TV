import streamlit as st
import pandas as pd
import locale
import altair as alt

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

st.set_page_config(
    layout="wide",
    page_title="Consumo Maquina de Vapor"
)

df = pd.read_csv("consultas/maqvap.txt", sep=',')

#Altera o campo para data
df['Data'] = pd.to_datetime(df['Data'])

df['Ano'] = df['Data'].dt.year
df['Mes'] = df['Data'].dt.month

# Calcula o total de cada mês
total_por_mes = df.groupby(['Ano', 'Mes'])['Custo'].sum().reset_index(name='Total')
total_por_mes_2023 = total_por_mes[total_por_mes['Ano'] == 2023]
total_por_mes_2024 = total_por_mes[total_por_mes['Ano'] == 2024]

# Calcula o total de cada ano
total_por_ano = df.groupby(['Ano'])['Custo'].sum().reset_index(name='TotalAno')

# Filtra os dados apenas para o ano de 2023
df_filtered_2023 = df[df['Ano'] == 2023]

# Filtra os dados apenas para o ano de 2024
df_filtered_2024 = df[df['Ano'] == 2024]

# Gráfico de barras mensal 2023
grafico_2023 = alt.Chart(df_filtered_2023).mark_line().encode(
    x=alt.X('Mes:N', axis=alt.Axis(title='Mês'.upper())),
    y=alt.Y('Custo:Q', axis=alt.Axis(title='Custo Total por Mês'.upper()), scale=alt.Scale(domain=[0, 30000])),
        ).interactive()

# Adiciona rótulos de dados com o total de cada mês
rótulos_2023 = alt.Chart(total_por_mes_2023).mark_text(
    align='center',
    baseline='middle',
    dx=0,
    dy=-7,  # Ajuste para posicionar o texto acima das barras
    fontSize=14  # Define o tamanho da fonte do rótulo
).encode(
    x=alt.X('Mes:N'),
    y=alt.Y('Total:Q'),
    text=alt.Text('Total:Q', format='$,.2f')  # Formata o texto para exibir moeda
)

# Gráfico de barras mensal 2024
grafico_2024 = alt.Chart(df_filtered_2024).mark_line().encode(
    x=alt.X('Mes:N', axis=alt.Axis(title='Mês'.upper())),
    y=alt.Y('Custo:Q', axis=alt.Axis(title='Custo Total por Mês'.upper()), scale=alt.Scale(domain=[0, 30000])),
        ).interactive()

# Adiciona rótulos de dados com o total de cada mês
rótulos_2024 = alt.Chart(total_por_mes_2024).mark_text(
    align='center',
    baseline='middle',
    dx=0,
    dy=-7,  # Ajuste para posicionar o texto acima das barras
    fontSize=14  # Define o tamanho da fonte do rótulo
).encode(
    x=alt.X('Mes:N'),
    y=alt.Y('Total:Q'),
    text=alt.Text('Total:Q', format='$,.2f')  # Formata o texto para exibir moeda
)

# Gráfico de barras anual
grafico_anual = alt.Chart(df).mark_bar().encode(
    x=alt.X('Ano:N', axis=alt.Axis(title='Ano'.upper())),
    y=alt.Y('Custo:Q', axis=alt.Axis(title='Custo Total por Ano'.upper()), scale=alt.Scale(domain=[0, 250000])),
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
    text=alt.Text('TotalAno:Q', format='$,.2f')  # Formata o texto para exibir moeda
)

# Junta o gráfico de barras e o rótulo mensal
grafico_final_2023 = (grafico_2023 + rótulos_2023).properties(width=600, height=400)
grafico_final_2024 = (grafico_2024 + rótulos_2024).properties(width=600, height=400)

# Coluna 1
col1, col2 = st.columns(2)

# Título mensal alinhado com o gráfico mensal
with col1:
    st.markdown("<h2 style='text-align: center; color: black;'>Custo Maquina de Vapor Mensal 2023</h2>", unsafe_allow_html=True)
    col1.altair_chart(grafico_final_2023, use_container_width=True)

with col2:
    st.markdown("<h2 style='text-align: center; color: black;'>Custo Maquina de Vapor Mensal 2024</h2>", unsafe_allow_html=True)
    col2.altair_chart(grafico_final_2024, use_container_width=True)

# Título anual centralizado
st.markdown("<h2 style='text-align: center; color: black;'>Custo Maquina de Vapor Anual</h2>", unsafe_allow_html=True)

# Junta o gráfico de barras e o rótulo anual
grafico_final_anual = (grafico_anual + rótulos_anual).properties(width=600, height=400)
st.altair_chart(grafico_final_anual, use_container_width=True)
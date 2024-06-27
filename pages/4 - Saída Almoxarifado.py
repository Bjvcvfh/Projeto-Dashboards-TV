import streamlit as st
import pandas as pd
import locale
import plotly.express as px

# Configuração da localidade
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

# Configuração da página
st.set_page_config(
    layout="wide",
    page_title="Peças Almoxarifado"
)

# Leitura do arquivo CSV
df = pd.read_csv("consultas/stl_geral.csv", sep=';', encoding='latin-1')

# Alterar o campo para data
df['Data Inicio'] = pd.to_datetime(df['Data Inicio'], format='%d/%m/%Y')

# Aplicação dos filtros
filtro = df[df['Tipo'] == 'REAL']
filtro = filtro[filtro['Tipo Insumo'] == "Produto"]
filtro = filtro[filtro['Nota Fiscal'] == ".   ."]
filtro = filtro[~filtro['Nome Insumo'].str.contains("PARAFUSO")]
filtro = filtro[~filtro['Nome Insumo'].str.contains("PORCA")]
filtro = filtro[~filtro['Nome Insumo'].str.contains("ARRUELA")]
filtro = filtro[~filtro['Nome Insumo'].str.contains("PARAF")]
filtro = filtro[~filtro['Nome Insumo'].str.contains("REBITE")]
filtro = filtro[~filtro['Nome Insumo'].str.contains("SOLUPAN")]
filtro = filtro[~filtro['Nome Insumo'].str.contains("POLLY PINK")]
filtro = filtro[~filtro['Nome Insumo'].str.contains("960SM")]
filtro = filtro[~filtro['Nome Insumo'].str.contains("ANEL")]
filtro = filtro[~filtro['Nome Insumo'].str.contains("ABRACADEIRA")]
filtro = filtro[~filtro['Nome Insumo'].str.contains("ATPRIME")]
filtro = filtro[~filtro['Nome Insumo'].str.contains("CREPE")]
filtro = filtro[~filtro['Nome Insumo'].str.contains("OLEO")]
filtro = filtro[~filtro['Nome Insumo'].str.contains("DETERGENTE")]
filtro = filtro[~filtro['Nome Insumo'].str.contains("ACELERADOR")]
filtro = filtro[~filtro['Nome Insumo'].str.contains("THINNER")]
filtro = filtro[~filtro['Nome Insumo'].str.contains("ANILHA")]
filtro = filtro[~filtro['Nome Insumo'].str.contains("PNEU")]
filtro = filtro[~filtro['Nome Insumo'].str.contains("FLUIDO P/")]
filtro = filtro[~filtro['Nome Insumo'].str.contains("ADITIVO")]
filtro = filtro[~filtro['Nome Insumo'].str.contains("FLUIDO P/")]
filtro = filtro[~filtro['Nome Insumo'].str.contains("ADEPOXI")]
filtro = filtro[~filtro['Codigo'].str.contains("PN")]
filtro = filtro[~filtro['Codigo'].str.contains("GG")]
filtro = filtro[~filtro['Codigo'].str.contains("MS")]
filtro = filtro[~filtro['Codigo'].str.contains("SV")]
filtro = filtro[~filtro['Codigo'].str.contains("LV")]
filtro = filtro[~filtro['Codigo'].str.contains("ET")]


# Extração de mês e ano
filtro['Mes'] = filtro['Data Inicio'].dt.month
filtro['Ano'] = filtro['Data Inicio'].dt.year
filtro['Ano'] = filtro['Ano'].astype(str)

# Adicionando o seletor de meses
meses_disponiveis = sorted(filtro['Data Inicio'].dt.strftime('%Y-%m').unique())
mes_selecionado = st.selectbox('Selecione o mês', meses_disponiveis)

# Filtrar o DataFrame pelo mês selecionado
df_filtered_month = filtro[filtro['Data Inicio'].dt.strftime('%Y-%m') == mes_selecionado]
df_filtered_month = df_filtered_month.sort_values(by='Quantidade')  # Ordenar por quantidade

# Agrupar pelos meses e anos e somar a quantidade de serviços por produto
df_grouped = df_filtered_month.groupby(['Nome Insumo', 'Mes', 'Ano'])['Quantidade'].sum().reset_index()

# Calcular a soma total por produto
soma_total_produto = df_grouped.groupby('Nome Insumo')['Quantidade'].sum().reset_index()
soma_total_produto = soma_total_produto.rename(columns={'Quantidade': 'Total Quantidade'})

# Adicionar a soma total ao DataFrame agrupado
df_grouped = df_grouped.merge(soma_total_produto, on='Nome Insumo')
df_grouped = df_grouped.sort_values(by='Quantidade', ascending=False)

# Formatar os meses e anos como uma única string
df_grouped['Data Inicio'] = df_grouped.apply(lambda row: f"{row['Mes']}/{row['Ano']}", axis=1)

colunas_para_exibir = ['Nome Insumo', 'Total Quantidade', 'Data Inicio']

st.markdown("<h2 style='text-align: center; color: black;'>Quantidade de Produtos por Mês</h2>", unsafe_allow_html=True)
st.dataframe(df_grouped[colunas_para_exibir])

# Exibir o DataFrame agrupado com opções interativas
selected_row = st.table(df_grouped[colunas_para_exibir]).selectbox('Selecione um item para ver o histórico:', df_grouped['Nome Insumo'])

# Filtrar o DataFrame pelo produto selecionado
filtro_produto_selecionado = filtro[filtro['Nome Insumo'] == selected_row]

# Agrupar pelo mês e somar as quantidades
soma_mensal_produto = filtro_produto_selecionado.groupby(['Ano', 'Mes'])['Quantidade'].sum().reset_index()

# Ordenar corretamente pela coluna de mês/ano
soma_mensal_produto['Data Inicial'] = soma_mensal_produto.apply(lambda row: f"{row['Mes']:02d}/{row['Ano']}", axis=1)
soma_mensal_produto = soma_mensal_produto.sort_values(by=['Ano', 'Mes'])

# Plotar o gráfico
fig = px.line(soma_mensal_produto, x='Data Inicial', y='Quantidade', markers=True, text="Quantidade", labels={'Quantidade': 'Quantidade Total', 'Data Inicial': 'Mês'}, title=f"Soma Mensal de {selected_row}")
fig.update_traces(textposition="top center",
                  textfont=dict(
        family="Arial",
        size=11,
        color="black"
    ))
st.plotly_chart(fig)
# %%
import streamlit as st
import pandas as pd


st.set_page_config(layout="wide", page_title="Produção", page_icon="📃")

st.title(f"Controle da Produção - EDDI CASA")


@st.cache_data
def load_data():
    # dataset = "datasets/CONTROLE DA PRODUCAO E M.O. - 2024.csv"
    dataset = "datasets/Controle da produção - 2025.csv"
    df = pd.read_csv(dataset)
    df = df.applymap(lambda x: x.title() if isinstance(x, str) else x)
    columns = df.columns
    colunas_formatadas = [coluna.title() for coluna in columns]
    df.columns = colunas_formatadas
    return df


df = load_data()
df["Data"] = pd.to_datetime(df["Data"])
df = df.set_index(df["Data"])
# df = df.drop(columns="Unnamed: 0")

st.session_state["df"] = df

# anos = df["Ano"].unique()
# ano = st.sidebar.selectbox(
#     "Ano",
#     anos,
#     placeholder="Selecione o ano",
# )

ano = 2025
# df_filtrador_ano = df[df["Ano"] == ano]

meses = df["Mes"].unique()
mes = st.sidebar.selectbox("Mes", meses, placeholder="Selecione o mês")
df_filtrado_mes = df[df["Mes"] == mes]

st.header(f"{mes} {ano}")

col1, col2, col3 = st.columns(3)

total_mes = df_filtrado_mes["Total"].sum()
total_mes_formatado = f"R$ {total_mes:,.2f}"
col1.metric(
    label="Total Produção",
    value=f"{total_mes_formatado.replace('.', '-').replace(',','.').replace('-', ',')}",
)

total_interno = df_filtrado_mes["Producao Interna"].sum()
total_interno_formatado = f"R$ {total_interno:,.2f}"
col2.metric(
    label="Produção Interna",
    value=f"{total_interno_formatado.replace('.', '-').replace(',','.').replace('-', ',')}",
)

total_mo = df_filtrado_mes["Producao Mao De Obra"].sum()
total_mo_formatado = f"R$ {total_mo:,.2f}"
col3.metric(
    label="Produção Mão de Obra",
    value=f"{total_mo_formatado.replace('.', '-').replace(',','.').replace('-', ',')}",
)


fechamento_2025 = {
    "Meses": ["Janeiro", "Fevereiro", "Março", "Abril", "Maio"],
    "Bonus": [12792.94, 15373.07, 15003.14, 18430.40, 18199.67],
    "Fechamento": [135727.50, 131557.98, 127245.84, 136547.75, 142877.91],
}
df_fechamento = pd.DataFrame(fechamento_2025)

col4, col5, col6 = st.columns(3)
df_fechamento_filtrado = df_fechamento[df_fechamento["Meses"] == mes]
valor_fechamento = float(df_fechamento_filtrado["Fechamento"])
valor_fechamento_formatado = f"R$ {valor_fechamento:,.2f}"
col4.metric(
    label="Total Gasto",
    value=f"{valor_fechamento_formatado.replace('.', '-').replace(',','.').replace('-', ',')}",
)
valor_bonus = float(df_fechamento_filtrado["Bonus"])
valor_bonus_formatado = f"R$ {valor_bonus:,.2f}"
col5.metric(
    label="Bônus",
    value=f"{valor_bonus_formatado.replace('.', '-').replace(',','.').replace('-', ',')}",
)

resultado = total_mes - valor_fechamento
resultado_formatado = f"R$ {resultado:,.2f}"

st.metric(
    label="Resultado",
    value=f"{resultado_formatado.replace('.','/').replace(',','.').replace('/',',')}",
)

# st.bar_chart(df_filtrado_mes["Total"], x_label="Data", y_label="Total")


# selected = st.checkbox("Ver tabela")
# if selected:
#     df_filtrado_mes

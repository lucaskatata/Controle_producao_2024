# %%
import streamlit as st
import pandas as pd
from openai import OpenAI

st.set_page_config(layout="wide", page_title="Produção", page_icon="📃")

st.title(f"Controle da Produção - EDDI CASA")

client = OpenAI(
    api_key="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"
)


@st.cache_data
def load_data():
    # dataset = "datasets/CONTROLE DA PRODUCAO E M.O. - 2024.csv"
    dataset = "datasets/Controle da produção.csv"
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

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": f"{df}",
            "role": "user",
            "content": f"Você tem acesso ao Dataframe?? {df}",
        }
    ],
)

output_chat = response.choices[0].message.content

st.markdown(output_chat)

anos = df["Ano"].unique()
ano = st.sidebar.selectbox(
    "Ano",
    anos,
    placeholder="Selecione o ano",
)
df_filtrador_ano = df[df["Ano"] == ano]

meses = df_filtrador_ano["Mes"].unique()
mes = st.sidebar.selectbox("Mes", meses, placeholder="Selecione o mês")
df_filtrado_mes = df_filtrador_ano[df_filtrador_ano["Mes"] == mes]

st.header(f"{mes} {ano}")

col1, col2, col3 = st.columns(3)

total_mes = df_filtrado_mes["Total"].sum()
total_mes_formatado = f"R$ {total_mes:,.2f}"
col1.metric(
    label="Total",
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

selected = st.checkbox("Ver tabela")
if selected:
    df_filtrado_mes

st.bar_chart(df_filtrado_mes["Total"], x_label="Data", y_label="Total")

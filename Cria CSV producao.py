# %%
import pandas as pd
from pathlib import Path


def retorna_mes(caminho_pasta):
    meses = {
        "01": "Janeiro",
        "02": "Fevereiro",
        "03": "Março",
        "04": "Abril",
        "05": "Maio",
        "06": "Junho",
        "07": "Julho",
        "08": "Agosto",
        "09": "Setembro",
        "10": "Outubro",
        "11": "Novembro",
        "12": "Dezembro",
    }
    pasta = Path(caminho_pasta)
    mes = pasta.name.split(" - ")[0]
    mes = meses.get(mes)
    return mes


def df_diario_producao_interna(arquivo):
    df_final = pd.DataFrame()
    lista_df = []
    df = pd.read_excel(arquivo, sheet_name="CAPA", usecols="B:E", nrows=12, skiprows=5)
    df["PROCESSO"] = df["PROCESSO"].str.split("-").str[-1].str.title()
    df = df.round(2)
    df["PROCESSO"] = df["PROCESSO"].str.strip()

    colunas = df.columns.str.title().str.strip()
    df = (
        df.drop(columns=colunas[2:])
        .rename(
            columns={"VALOR": f'{arquivo.stem.replace("-","/")}', "PROCESSO": "Data"}
        )
        .set_index("Data")
        .T
    )
    df["Producao Interna"] = df.sum(axis=1)
    colunas = df.columns
    nova_ordem_colunas = [colunas[-1]]
    colunas = colunas[:-1]
    for c in colunas:
        nova_ordem_colunas.append(c)
    df = df[nova_ordem_colunas]
    return df


def criar_df_producao_interna(caminho_pasta, df_diario_producao_interna):
    lista_df = []
    df_final = pd.DataFrame()
    for arquivo in caminho_pasta.iterdir():
        df = df_diario_producao_interna(arquivo)
        lista_df.append(df)
        df_final = pd.concat(lista_df)

    df_final.index.name = "Data"
    return df_final


def df_diario_mao_de_obra(arquivo):
    df_final = pd.DataFrame()
    lista_df = []
    df = pd.read_excel(arquivo, sheet_name="CAPA", usecols="B:E", nrows=12, skiprows=5)
    df["PROCESSO"] = df["PROCESSO"].str.split("-").str[-1].str.title()
    df = df.round(2)
    df["PROCESSO"] = df["PROCESSO"].str.strip()

    colunas = df.columns.str.title().str.strip()
    df = (
        df.drop(columns=colunas[2:])
        .rename(
            columns={"VALOR": f'{arquivo.stem.replace("-","/")}', "PROCESSO": "Data"}
        )
        .set_index("Data")
        .T
    )
    df["Producao Mao de Obra"] = df.sum(axis=1)
    colunas = df.columns
    nova_ordem_colunas = [colunas[-1]]
    colunas = colunas[:-1]
    for c in colunas:
        nova_ordem_colunas.append(c)
    df = df[nova_ordem_colunas]
    return df


def criar_df_mao_de_obra(caminho_pasta, df_diario_mao_de_obra):
    lista_df = []
    df_final = pd.DataFrame()
    for arquivo in caminho_pasta.iterdir():
        df = df_diario_mao_de_obra(arquivo)
        lista_df.append(df)
        df_final = pd.concat(lista_df)
    df_final.index = df_final.index.str.replace(" M.O", "")
    df_mo = df_final.drop(
        columns=[
            "Corte",
            "Corte Voil",
            "Bainha Continua",
            "Barrado",
            "Emenda",
            "Overloque",
            "Paleteira",
            "Acabamento",
            "Furo",
            "Ilhos",
            "Dobra",
            "Embalagem",
        ],
        axis=1,
    )
    df_mo.index = df_mo.index.astype(str).str.extract(r"(\d{2}/\d{2}/\d{4})")[0]
    df_mo.index.name = "Data"
    return df_mo


def merge(df_producao_interna, df_mao_de_obra, caminho_pasta):
    df = pd.merge(df_producao_interna, df_mao_de_obra, on="Data", how="outer").fillna(0)
    df["Total"] = df["Producao Interna"] + df["Producao Mao de Obra"]
    df = df[
        [
            "Total",
            "Producao Interna",
            "Producao Mao de Obra",
            "Corte",
            "Corte Voil",
            "Bainha Continua",
            "Barrado",
            "Emenda",
            "Overloque",
            "Paleteira",
            "Acabamento",
            "Furo",
            "Ilhos",
            "Dobra",
            "Embalagem",
        ]
    ]
    df["Mes"] = retorna_mes(caminho_pasta)
    return df


def concatena_meses(pasta):
    lista_df = []

    for c in pasta.iterdir():
        df = pd.read_csv(c)
        lista_df.append(df)

    df = pd.concat(lista_df)

    df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y")
    df = df.sort_values(by="Data").reset_index(drop=True)
    return df


diretorio_arquivo = Path(input("Pasta do mês para incluir: ").replace('"', ""))

for c in diretorio_arquivo.iterdir():
    if c.is_dir():
        if c.name.split("-")[1] == "2025":
            df_producao_interna = criar_df_producao_interna(
                c, df_diario_producao_interna
            )
        else:
            df_mao_de_obra = criar_df_mao_de_obra(c, df_diario_mao_de_obra)

df = merge(df_producao_interna, df_mao_de_obra, diretorio_arquivo)

pasta_destino = Path(r"D:\Trabalho - Eddi\Controle de Produção - 2025\Mensal")


df.to_csv(
    pasta_destino / f"Controle da produção - {retorna_mes(diretorio_arquivo)} 2025.csv",
    decimal=".",
    float_format="%.2f",
)

df_final = concatena_meses(pasta_destino)
df_final['Ano'] = df_final['Data'].dt.year
# %%
df_final.to_csv(
    Path(r"D:\Trabalho - Eddi\Controle de Produção - 2025")
    / f"Controle da produção - 2025.csv",
    decimal=".",
    float_format="%.2f",
)
# %%

df_final.to_csv(
    Path(r"D:\Lucas\GitHub\Controle_producao_2024\datasets")
    / f"Controle da produção - 2025.csv",
    decimal=".",
    float_format="%.2f",
)

# %%
df.to_excel(
    pasta_destino
    / f"Controle da produção - {retorna_mes(diretorio_arquivo)} 2025.xlsx",
    index=False,
)
# %%
df_final
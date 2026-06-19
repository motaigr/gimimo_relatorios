import streamlit as st
import pandas as pd
import glob

# --- Dados de vendas ---
arquivos = glob.glob("clientes/*.csv")
arquivos = [a for a in arquivos if "22-34-11" not in a]

lista_dfs = []
for arquivo in arquivos:
    df_temp = pd.read_csv(arquivo, sep=";")
    df_temp["Total"] = df_temp["Total"].astype(str).str.replace(",", ".").astype(float)
    lista_dfs.append(df_temp)

df_vendas = pd.concat(lista_dfs, ignore_index=True)

# --- Dashboard ---
st.title("Dashboard Gimimo")

col1, col2, col3 = st.columns(3)
col1.metric("Faturamento Total", f"R$ {df_vendas['Total'].sum():.2f}")
col2.metric("Total de Pedidos", len(df_vendas))
col3.metric("Ticket Médio", f"R$ {df_vendas['Total'].mean():.2f}")

import matplotlib.pyplot as plt

st.subheader("Evolução do Faturamento Mensal")

arquivos_fat = glob.glob("evolucao/*.csv")
lista_fat = []
for arquivo in arquivos_fat:
    df_temp = pd.read_csv(arquivo, sep=";")
    df_temp["Período"] = pd.to_datetime(df_temp["Período"], format="%d/%m/%Y")
    df_temp["Valor"] = df_temp["Valor"].astype(str).str.replace(",", ".").astype(float)
    df_temp["Mês"] = df_temp["Período"].dt.to_period("M")
    lista_fat.append(df_temp)

df_fat = pd.concat(lista_fat, ignore_index=True)
df_fat = df_fat.groupby("Mês", as_index=False).agg({"Valor": "sum"})

fig, ax = plt.subplots()
ax.plot(df_fat["Mês"].astype(str), df_fat["Valor"], marker="o")
ax.set_xlabel("Mês")
ax.set_ylabel("Valor (R$)")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

arquivos_prod = glob.glob("produtos/*.csv")
lista_prod = []
for arquivo in arquivos_prod:
    df_temp = pd.read_csv(arquivo, sep=";")
    df_temp["Valor Total"] = df_temp["Valor Total"].astype(str).str.replace(",", ".").astype(float)
    lista_prod.append(df_temp)

df_prod = pd.concat(lista_prod, ignore_index=True)
df_prod["Produto"] = df_prod["Produto"].str.split("|").str[0].str.strip()
df_prod = df_prod.groupby("Produto", as_index=False).agg({"Valor Total": "sum"})
df_prod = df_prod.sort_values("Valor Total", ascending=False)

st.subheader("Top 10 Produtos por Receita")
fig_prod, ax_prod = plt.subplots()
ax_prod.barh(df_prod.head(10)["Produto"], df_prod.head(10)["Valor Total"])
ax_prod.set_xlabel("Valor Total (R$)")
ax_prod.set_ylabel("Produto")
plt.tight_layout()
plt.gca().invert_yaxis()
st.pyplot(fig_prod)

arquivos_quant = glob.glob("produtos/*.csv")
lista_quant = []
for arquivo in arquivos_quant:
    df_temp = pd.read_csv(arquivo, sep=";")
    df_temp["Quantidade"] = df_temp["Quantidade"].astype(int)
    df_temp["Produto"] = df_temp["Produto"].str.split("|").str[0].str.strip()
    lista_quant.append(df_temp)

df_quant = pd.concat(lista_quant, ignore_index=True)
df_quant = df_quant.groupby("Produto", as_index=False).agg({"Quantidade": "sum"})
df_quant = df_quant.sort_values("Quantidade", ascending=False)
st.subheader("Top 10 Produtos por Quantidade Vendida")
fig_quant, ax_quant = plt.subplots()
ax_quant.barh(df_quant.head(10)["Produto"], df_quant.head(10)["Quantidade"])
ax_quant.set_xlabel("Quantidade")
ax_quant.set_ylabel("Produto")
plt.tight_layout()
plt.gca().invert_yaxis()
st.pyplot(fig_quant)

arquivos_cli = glob.glob("clientes/*.csv")
lista_cli = []
for arquivo in arquivos_cli:
    df_temp = pd.read_csv(arquivo, sep=";")
    df_temp["Total"] = df_temp["Total"].astype(str).str.replace(",", ".").astype(float)
    df_temp["Nome"] = df_temp["Cliente"].str.split(" - ").str[0]
    lista_cli.append(df_temp)

df_cli = pd.concat(lista_cli, ignore_index=True)
df_cli = df_cli.groupby("Nome", as_index=False).agg({"Total": "sum"})
df_cli = df_cli.sort_values("Total", ascending=False)
st.subheader("Top 10 Clientes por Faturamento")

fig_cli, ax_cli = plt.subplots()
ax_cli.barh(df_cli.head(10)["Nome"], df_cli.head(10)["Total"])
ax_cli.set_xlabel("Total (R$)")
ax_cli.set_ylabel("Cliente")
plt.tight_layout()
plt.gca().invert_yaxis()
st.pyplot(fig_cli)
import streamlit as st
import pandas as pd
import glob
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Gimimo — Análise de Vendas",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        .stApp { background-color: #0E1117; }
        .block-container { padding-top: 1.5rem; }
        [data-testid="stMetric"] {
            background-color: #1E1E2E;
            border-radius: 10px;
            padding: 15px;
            border: 1px solid #3A3A5C;
        }
        [data-testid="stMetricLabel"] { color: #AAAACC !important; font-size: 14px; }
        [data-testid="stMetricValue"] { color: #FFFFFF !important; font-size: 28px; }
            h1, h2, h3 { color: #FFFFFF !important; }
    </style>
""", unsafe_allow_html=True)

# ── Carregamento de dados ──────────────────────────────────────────────────────

@st.cache_data
def carregar_vendas():
    arquivos = glob.glob("clientes/*.csv")
    arquivos = [a for a in arquivos if "22-34-11" not in a]
    dfs = []
    for arquivo in arquivos:
        df = pd.read_csv(arquivo, sep=";")
        df["Total"] = df["Total"].astype(str).str.replace(",", ".").astype(float)
        df["Nome"] = df["Cliente"].str.split(" - ").str[0]
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

@st.cache_data
def carregar_faturamento():
    arquivos = glob.glob("evolucao/*.csv")
    dfs = []
    for arquivo in arquivos:
        df = pd.read_csv(arquivo, sep=";")
        df["Período"] = pd.to_datetime(df["Período"], format="%d/%m/%Y")
        df["Valor"] = df["Valor"].astype(str).str.replace(",", ".").astype(float)
        df["Mês"] = df["Período"].dt.to_period("M")
        dfs.append(df)
    df = pd.concat(dfs, ignore_index=True)
    return df.groupby("Mês", as_index=False).agg({"Valor": "sum"})

@st.cache_data
def carregar_produtos():
    arquivos = glob.glob("produtos/*.csv")
    dfs = []
    for arquivo in arquivos:
        df = pd.read_csv(arquivo, sep=";")
        df["Valor Total"] = df["Valor Total"].astype(str).str.replace(",", ".").astype(float)
        df["Quantidade"] = df["Quantidade"].astype(int)
        df["Produto"] = df["Produto"].str.split("|").str[0].str.strip()
        dfs.append(df)
    df = pd.concat(dfs, ignore_index=True)
    return df.groupby("Produto", as_index=False).agg({"Quantidade": "sum", "Valor Total": "sum"})

df_vendas = carregar_vendas()
df_fat = carregar_faturamento()
df_prod = carregar_produtos()

# ── Categorização ──────────────────────────────────────────────────────────────

def categorizar(nome):
    if "Absorvente" in nome or "Sachê" in nome or "Sach" in nome:
        return "Armazenamento"
    return "Bótons"

df_prod["Categoria"] = df_prod["Produto"].apply(categorizar)
df_categorias = df_prod.groupby("Categoria", as_index=False).agg({"Quantidade": "sum"})
df_prod["Produto"] = df_prod["Produto"].str[:40]

df_cli = df_vendas.groupby("Nome", as_index=False).agg({"Total": "sum"})
df_cli = df_cli.sort_values("Total", ascending=False)

df_prod_receita = df_prod.sort_values("Valor Total", ascending=False)
df_prod_quant = df_prod.sort_values("Quantidade", ascending=False)

# ── Layout ─────────────────────────────────────────────────────────────────────

st.title("Gimimo — Análise de Vendas")

# Métricas
col1, col2, col3 = st.columns(3)
col1.metric("💰 Faturamento Total", f"R$ {df_vendas['Total'].sum():,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
col2.metric("🛒 Total de Pedidos", len(df_vendas))
col3.metric("🎯 Ticket Médio", f"R$ {df_vendas['Total'].mean():,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.divider()

# Linha 1 — Faturamento mensal + Rosca
col_fat, col_rosca = st.columns([2, 1])

with col_fat:
    st.subheader("Evolução do Faturamento Mensal")
    fig_fat = px.line(
        df_fat,
        x=df_fat["Mês"].astype(str),
        y="Valor",
        markers=True,
        template="plotly_dark",
        labels={"x": "Mês", "Valor": "Valor (R$)"}
    )
    fig_fat.update_layout(
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117"
)
    st.plotly_chart(fig_fat, use_container_width=True)

with col_rosca:
    st.subheader("Vendas por Categoria")
    fig_rosca = go.Figure(go.Pie(
        labels=df_categorias["Categoria"],
        values=df_categorias["Quantidade"],
        hole=0.5,
        marker_colors=["#E87C4C", "#4C9BE8"]
    ))
    fig_rosca.update_layout(
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    font_color="white",
    legend=dict(font=dict(color="white"))
)
    st.plotly_chart(fig_rosca, use_container_width=True)

st.divider()

# Linha 2 — Top produtos por receita + por quantidade
col_rec, col_quant = st.columns(2)

with col_rec:
    st.subheader("Top 10 Produtos por Receita")
    top_rec = df_prod_receita.head(10).sort_values("Valor Total")
    fig_rec = px.bar(
        top_rec,
        x="Valor Total",
        y="Produto",
        orientation="h",
        template="plotly_dark",
        labels={"Valor Total": "Receita (R$)", "Produto": ""},
        color="Valor Total",
        color_continuous_scale="Blues"
    )
    fig_rec.update_layout(paper_bgcolor="#0E1117", plot_bgcolor="#0E1117")
    st.plotly_chart(fig_rec, use_container_width=True)

with col_quant:
    st.subheader("Top 10 Produtos por Quantidade")
    top_quant = df_prod_quant.head(10).sort_values("Quantidade")
    fig_quant = px.bar(
        top_quant,
        x="Quantidade",
        y="Produto",
        orientation="h",
        template="plotly_dark",
        labels={"Quantidade": "Unidades Vendidas", "Produto": ""},
        color="Quantidade",
        color_continuous_scale="Blues"
    )
    fig_quant.update_layout(paper_bgcolor="#0E1117", plot_bgcolor="#0E1117")
    st.plotly_chart(fig_quant, use_container_width=True)

st.divider()

# Linha 3 — Top clientes
st.subheader("Top 10 Clientes por Faturamento")
top_cli = df_cli.head(10).sort_values("Total")
fig_cli = px.bar(
    top_cli,
    x="Total",
    y="Nome",
    orientation="h",
    template="plotly_dark",
    labels={"Total": "Total (R$)", "Nome": ""},
    color="Total",
    color_continuous_scale="Blues"
)
fig_cli.update_layout(paper_bgcolor="#0E1117", plot_bgcolor="#0E1117")
st.plotly_chart(fig_cli, use_container_width=True)
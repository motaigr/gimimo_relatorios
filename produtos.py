import csv
import glob
import pandas as pd
import matplotlib.pyplot as plt

arquivos = glob.glob("produtos/*.csv")

lista_dfs = []
for arquivo in arquivos:
    df_temp = pd.read_csv(arquivo, sep=";")
    df_temp["Valor Total"] = df_temp["Valor Total"].astype(str).str.replace(",", ".").astype(float)
    lista_dfs.append(df_temp)

df_final = pd.concat(lista_dfs, ignore_index=True)
df_final["Produto"] = df_final["Produto"].str.split("|").str[0].str.strip()
df_final = df_final.groupby("Produto", as_index=False).agg({"Quantidade": "sum", "Valor Total": "sum"})
df_final = df_final.sort_values("Valor Total", ascending=False)

print(df_final.head(5))
print(df_final.columns.tolist())
print(df_final)

plt.barh(df_final["Produto"], df_final["Valor Total"])
plt.xlabel("Produto")
plt.ylabel("Valor Total")
plt.title("Receita por Produto (R$)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.gca().invert_yaxis()
plt.show()

#df_final.to_excel("result_receita.xlsx", index=False)

df_quantidade = df_final.sort_values("Quantidade", ascending=False)
plt.barh(df_quantidade["Produto"], df_quantidade["Quantidade"])
plt.xlabel("Produto")
plt.ylabel("Quantidade")
plt.title("Quantidade Vendida por Produto")
plt.xticks(rotation=45)
plt.tight_layout()
plt.gca().invert_yaxis()
plt.show()

#df_quantidade.to_excel("result_quantidade.xlsx", index=False)


def categorizar(nome):
    if "Absorvente" in nome or "Sachê" in nome:
        return "Armazenamento"
    else:
        return "Bótons"
    
df_final["Categoria"] = df_final["Produto"].apply(categorizar)
df_categorias = df_final.groupby("Categoria").agg({"Quantidade": "sum", "Valor Total": "sum"})
print(df_categorias)

fig, ax = plt.subplots()
ax.pie(
    df_categorias["Quantidade"],
    labels=df_categorias.index,
    autopct="%1.1f%%",
    wedgeprops={"width": 0.5}
)
ax.set_title("Vendas por Categoria (Quantidade)")
plt.show()
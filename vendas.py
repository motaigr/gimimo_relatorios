import pandas as pd
import glob
import matplotlib.pyplot as plt

arquivos = glob.glob("clientes/*.csv")
arquivos.remove("relatorio-de-vendas_10-06-2026-22-34-11.csv")


lista_dfs = []

for arquivo in arquivos:
    df_temp = pd.read_csv(arquivo, sep=";")
    df_temp["Valor"] = df_temp["Valor"].astype(str).str.replace(",", ".").astype(float)
    df_temp["Frete"] = df_temp["Frete"].astype(str).str.replace(",", ".").astype(float)
    df_temp["Total"] = df_temp["Total"].astype(str).str.replace(",", ".").astype(float)
    lista_dfs.append(df_temp)

df_total = pd.concat(lista_dfs, ignore_index=True)
df_total["Nome"] = df_total["Cliente"].str.split(" - ").str[0]
df_total["cpf"] = df_total["Cliente"].str.split(" - ").str[1]

df_total = df_total.groupby(["Nome", "cpf"], as_index=False).agg({"Valor": "sum", "Frete": "sum", "Total": "sum"})
df_total["Total"].sum()
pedidos = len(df_total)
ticket_medio = df_total["Total"].mean()


top10 = df_total.sort_values("Total", ascending=False).head(10)

plt.figure(figsize=(10, 6))
plt.barh(top10["Nome"], top10["Total"])
plt.xlabel("Total (R$)")
plt.title("Top 10 Clientes por Valor Total")
plt.tight_layout()
plt.gca().invert_yaxis()
plt.show()

#print(df_total[["Nome", "cpf"]].head(5))
print(df_total.sort_values("Total", ascending=False).head(10))
#print(df_total.dtypes)
print(df_total["Total"].sum())
print(f"Ticket médio: {ticket_medio:.2f}")
print(f"Total de pedidos: {pedidos}")


df_total.to_excel("resultado.xlsx", index=False)


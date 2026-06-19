import glob
import pandas as pd
import matplotlib.pyplot as plt

arquivos = glob.glob("evolucao/*.csv")

lista_dfs = []

for arquivo in arquivos:
    df_temp = pd.read_csv(arquivo, sep=";")
    df_temp["Período"] = pd.to_datetime(df_temp["Período"], format="%d/%m/%Y")
    df_temp["Valor"] = df_temp["Valor"].astype(str).str.replace(",", ".").astype(float)
    df_temp["Mês"] = df_temp["Período"].dt.to_period("M")
    lista_dfs.append(df_temp)
df_total = pd.concat(lista_dfs, ignore_index=True)
df_total = df_total.groupby("Mês", as_index=False).agg({"Valor": "sum"})
    
print(df_total.head(10))
print(df_total.dtypes)
print(df_total.shape)

plt.plot(df_total["Mês"].astype(str), df_total["Valor"])
plt.xlabel("Mês")
plt.ylabel("Valor")
plt.title("Evolução do Faturamento")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

df_total.to_excel("result_faturamento.xlsx", index=False)
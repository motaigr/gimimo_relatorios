import csv
import glob
import pandas as pd

arquivos = glob.glob("produtos/*.csv")

lista_dfs = []
for arquivo in arquivos:
    df_temp = pd.read_csv(arquivo, sep=";")
    df_temp["Valor"] = df_temp["Valor"].astype(str).str.replace(",", ".").astype(float)
    lista_dfs.append(df_temp)

df_final = pd.concat(lista_dfs, ignore_index=True)

print(df_final.head(5))
print(df_final.columns.tolist())
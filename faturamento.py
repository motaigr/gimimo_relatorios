import csv
import glob
import pandas as pd

arquivos = glob.glob("evolucao/*.csv")

lista_dfs = []

for arquivo in arquivos:
    df_temp = pd.read_csv(arquivo, sep=";")
    df_temp["Período"] = pd.to_datetime(df_temp["Período"], format="%d/%m/%Y")
    df_temp["Valor"] = df_temp["Valor"].astype(str).str.replace(",", ".").astype(float)
    lista_dfs.append(df_temp)
df_total = pd.concat(lista_dfs, ignore_index=True)
    
print(df_total.head(10))
print(df_total.dtypes)
print(df_total.shape)
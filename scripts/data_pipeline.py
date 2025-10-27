import pandas as pd
import boto3
from io import StringIO
import sys
import os


if len(sys.argv) < 2:
    print("Please provide the S3 bucket name as an argument on python command line")
    sys.exit(1)

bucket_name = sys.argv[1]

s3 = boto3.client("s3")

#raw data
arquivo_entrada = "data/dados_pacientes.csv"
arquivo_saida_tratado = "data/dados_pacientes_tratado.csv"
arquivo_saida_cliente = "data/dados_pacientes_cliente.csv"

df = pd.read_csv(arquivo_entrada)



#Data cleaning
if "weight" in df.columns:
    df.loc[(df["weight"] < 30) | (df["weight"] > 200), "weight"] = None
if "height" in df.columns:
    df.loc[(df["height"] < 100) | (df["height"] > 220), "height"] = None

# Converter colunas de tempo
colunas_tempo = ["casestart", "caseend", "anestart", "aneend", "opstart", "opend"]
for col in colunas_tempo:
    if col in df.columns:
        df[col] = pd.to_timedelta(df[col], unit="s")

# Duracoes em horas
if {"casestart", "caseend"}.issubset(df.columns):
    df["duracao_caso_horas"] = (df["caseend"] - df["casestart"]).dt.total_seconds() / 3600
if {"anestart", "aneend"}.issubset(df.columns):
    df["duracao_anestesia_horas"] = (df["aneend"] - df["anestart"]).dt.total_seconds() / 3600


df.to_csv(arquivo_saida_tratado, index=False, encoding="utf-8-sig")
print(f"✅ Arquivo tratado salvo localmente como: {arquivo_saida_tratado}")


#/client
df_cliente = df.copy()
if "patient_id" in df_cliente.columns:
    df_cliente = df_cliente.drop(columns=["patient_id"])

df_cliente.to_csv(arquivo_saida_cliente, index=False, encoding="utf-8-sig")

#Upload to S3
def upload_to_s3(file_path, s3_key):
    with open(file_path, "rb") as data:
        s3.upload_fileobj(data, bucket_name, s3_key)
    print(f"☁️  Uploaded to s3://{bucket_name}/{s3_key}")

# Upload
upload_to_s3(arquivo_entrada, f"raw/{arquivo_entrada}")
upload_to_s3(arquivo_saida_tratado, f"trusted/{arquivo_saida_tratado}")
upload_to_s3(arquivo_saida_cliente, f"client/{arquivo_saida_cliente}")

print("Pipeline de dados concluído")

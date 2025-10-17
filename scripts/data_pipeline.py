import boto3, pandas as pd, os

# Cria o diretório output
os.makedirs("./output/", exist_ok=True)

bucket = "lab-sprint5-arqnuvem-rafael-scheneider"
s3 = boto3.client("s3")
local = "data/sales.csv"

# RAW
s3.upload_file(local, bucket, "raw/sales.csv")

# TRUSTED
df = pd.read_csv(local).dropna()
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

# Salva dentro de ./output/
trusted_path = "./output/trusted_sales.csv"
df.to_csv(trusted_path, index=False)
s3.upload_file(trusted_path, bucket, "trusted/sales.csv")

# CLIENT
client = df[['order_id','amount']]
client_path = "./output/client_sales.csv"
client.to_csv(client_path, index=False)
s3.upload_file(client_path, bucket, "client/sales.csv")

print("Pipeline executado com sucesso!")

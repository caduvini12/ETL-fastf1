import pandas as pd 
df = pd.read_parquet('s3://fastf1-datalake-caduvini/gold/year=2025/place=monaco/quali=Q/dados_gold_monaco_2025.parquet')
media_velocidade = df[df["Volta_Precisa"]].groupby("Piloto")["Velocidade"].mean()
print(media_velocidade)



print(df['Tempo_Volta'])
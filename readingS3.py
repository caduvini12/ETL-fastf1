import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_parquet('s3://fastf1-datalake-caduvini/gold/year=2025/place=monaco/quali=Q/dados_gold_monaco_2025.parquet')

# Filtra só as voltas válidas e só os dois pilotos que você quer comparar
df_preciso = df[df["Volta_Precisa"]]
df_filtrado = df_preciso[df_preciso["Piloto"].isin(["NOR", "VER"])]

plt.figure(figsize=(12, 6))
sns.set_theme(style="darkgrid")

sns.lineplot(
    data=df_filtrado,
    x="Numero_Volta",   # progressão real da sessão, não a duração da volta
    y="Velocidade",
    hue="Piloto",
    linewidth=2.5,
    marker="o"
)

plt.title('Comparativo de Velocidade: NOR vs VER - Qualifying Mônaco 2025', fontsize=14, fontweight='bold')
plt.xlabel('Número da Volta', fontsize=12)
plt.ylabel('Velocidade Máxima (km/h)', fontsize=12)
plt.legend(title="Piloto")
plt.tight_layout()

plt.savefig('comparativo_nor_ver.png', dpi=150, bbox_inches='tight')
plt.show()
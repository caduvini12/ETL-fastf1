import pandas as pd
from pathlib import Path

def transformGold(year,place,quali):
    caminho = Path(__file__).parent / "silver" / "telemetry"/f'year={year}'/f'place={place}'/f'quali={quali}'
    caminho2 = Path(__file__).parent / "silver" / "Data_Laps"/f'year={year}'/f'place={place}'/f'quali={quali}'
    arquivo2 = caminho2 /f'dados_voltas_{place}_{year}.parquet'
    arquivo = caminho /f'dados_silver_{place}_{year}.parquet'
    dados2 = pd.read_parquet(arquivo2)
    dados = pd.read_parquet(arquivo)
    dadosTransform = dados.groupby(['Piloto','Numero_Volta'])["Velocidade"].max()
    new_dadosTransform= dadosTransform.reset_index()
    merge_df = pd.merge(new_dadosTransform,dados2, on=['Piloto','Numero_Volta'], how='inner')
    print(merge_df)

transformGold(2025,'monaco','Q')
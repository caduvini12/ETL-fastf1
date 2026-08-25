import pandas as pd
from pathlib import Path

def transformGold(year,place,quali):
    caminho = Path(__file__).parent/ "silver" /f'year={year}'/f'place={place}'/f'quali={quali}'
    arquivo = caminho /f'dados_silver_{place}_{year}.parquet'
    dados = pd.read_parquet(arquivo)
    dadosTransform = dados.groupby('Piloto')['Velocidade'].mean()
    print(dadosTransform)

transformGold(2025,'monaco','Q')
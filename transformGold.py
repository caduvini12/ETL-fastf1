import pandas as pd
from pathlib import Path

def readDataSilver(year,place,quali):
    caminho1 = Path(__file__).parent / "silver" / "telemetry" / f'year={year}'/f'place={place}'/f'quali={quali}'
    caminho2 = Path(__file__).parent / "silver" / "Data_Laps" / f'year={year}'/f'place={place}'/f'quali={quali}'
    arquivo = caminho1 / f'dados_silver_{place}_{year}.parquet'
    arquivo2 = caminho2 / f'dados_voltas_{place}_{year}.parquet'
    arquivo1 = pd.read_parquet(arquivo,engine ='fastparquet')
    arquivo2 = pd.read_parquet(arquivo2,engine = 'fastparquet')
    return arquivo1,arquivo2

def transformGold(arquivo1,arquivo2):
    dadosTransform = arquivo1.groupby(['Piloto','Numero_Volta'])["Velocidade"].max()
    new_dadosTransform= dadosTransform.reset_index()
    merge_df = pd.merge(new_dadosTransform,arquivo2, on=['Piloto','Numero_Volta'], how='inner')
    return merge_df

def savingGold(year,place,quali):
    caminho3 = Path(__file__).parent / "gold" /  f'year={year}'/f'place={place}'/f'quali={quali}'
    caminho3.mkdir(parents=True,exist_ok=True)
    arquivo1, arquivo2 = readDataSilver(year,place,quali)
    dados = transformGold(arquivo1,arquivo2)
    arquivo = caminho3 /f'dados_gold_{place}_{year}.parquet'
    dados.to_parquet(arquivo,index=False)


savingGold(2025,'monaco','Q')


from pathlib import Path
import pandas as pd

def readDatabase(year, place,quali):
 caminho = Path(__file__).parent / "bronze" /f'year={year}'/f'place={place}'/f'quali={quali}'
 arquivo = caminho / f'dados_fastf1_{place}_{year}.parquet'
 df = pd.read_parquet(arquivo,engine ='fastparquet')

 return df
def transformData(df):

    # Arredondamento dos valores
    df['RPM'] = df['RPM'].round(1)
    df['Speed'] = df['Speed'].round(2)
    df['Throttle'] = df['Throttle'].round(2)
    df['Distance'] = df['Distance'].round(2)
    df['RelativeDistance'] = df['RelativeDistance'].round(4)
    df['X'] = df['X'].round(2)
    df['Y'] = df['Y'].round(2)
    df['Z'] = df['Z'].round(2)

    # Conversão do tempo
    df['Tempo_Sessao_Segundos'] = (
        df['SessionTime'] / 1_000_000_000
    ).round(3)

    df['Tempo_Sessao_Minutos'] = (
        df['Tempo_Sessao_Segundos'] / 60
    ).round(1)

    # Renomeando todas as colunas
    df.rename(columns={
        'Date': 'Data',
        'Time': 'Tempo',
        'Speed': 'Velocidade',
        'nGear': 'Marcha',
        'Throttle': 'Acelerador',
        'Brake': 'Freio',
        'DRS': 'DRS',
        'Distance': 'Distancia',
        'RelativeDistance': 'Distancia_Relativa',
        'Status': 'Status',
        'X': 'Posicao_X',
        'Y': 'Posicao_Y',
        'Z': 'Posicao_Z',
        'Driver': 'Piloto',
        'LapNumber': 'Numero_Volta',
        'SessionTime': 'Tempo_Sessao'
    }, inplace=True)

    # Remove colunas antigas que não são mais necessárias
    df.drop(
        columns=[
            'Tempo',
            'Tempo_Sessao'
        ],
        inplace=True,
        errors='ignore'
    )

    return df
def savingData_Silver(year,place,quali):
   try:
    caminho = Path(__file__).parent / "silver" /f'year={year}'/f'place={place}'/f'quali={quali}'
    caminho.mkdir(parents=True,exist_ok=True)
    dados = readDatabase(year, place, quali)
    dataTransfrom = transformData(dados)
    arquivo = caminho / f'dados_silver_{place}_{year}.parquet'
    dataTransfrom.to_parquet(arquivo,index = False)
   except ValueError:
      print('Erro ao tentar salvar')

savingData_Silver(2025, 'monaco','Q')
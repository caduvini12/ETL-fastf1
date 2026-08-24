from pathlib import Path
import pandas as pd

def readDatabase(year, place,quali):
 arquivo = Path(__file__).parent / "silver" /f'year={year}'/f'place={place}'/f'quali={quali}'
 caminho_final1 = arquivo / f'dados_fastf1_{place}_{year}.parquet'
 df = pd.read_parquet(caminho_final1,engine ='fastparquet')

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
    arquivo = Path(__file__).parent / "silver" /f'year={year}'/f'place={place}'/f'quali={quali}'
    arquivo.mkdir(parents=True,exist_ok=True)
    dados = readDatabase(year, place, quali)
    dataTransfrom = transformData(dados)
    caminhofinal = arquivo / f'dados_fastf1_{place}_{year}.parquet'
    dataTransfrom.to_parquet(caminhofinal,index = False)
   except ValueError:
      print('Erro ao tentar salvar')

savingData_Silver(2025, 'monaco','Q')
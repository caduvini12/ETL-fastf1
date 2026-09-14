from pathlib import Path
import pandas as pd

def readDatabase(year, place,quali):

 caminho = Path(__file__).parent / "bronze" / "telemetry" /f"year={year}" /f"place={place}" /f"quali={quali}"
 caminho2 = Path(__file__).parent / "bronze" / "Data_Laps" /f"year={year}" /f"place={place}" /f"quali={quali}"
 arquivo = caminho / f'dados_telemetry_bronze_{place}_{year}.parquet'
 arquivo2 = caminho2 / f'dados_voltas_bronze_{place}_{year}.parquet'
 df = pd.read_parquet(arquivo,engine ='fastparquet')
 df2 = pd.read_parquet(arquivo2,engine = 'fastparquet')

 return df,df2

def transformDataLaps(df2):
    #filtrando linhas por corridas verdadeiras
    df2[df2['IsAccurate'] == True]

    # Conversão dos tempos de nanossegundos para segundos
    colunas_tempo = [
        'LapTime',
        'PitOutTime',
        'PitInTime',
        'Sector1Time',
        'Sector2Time',
        'Sector3Time',
        'LapStartTime'
    ]

    for coluna in colunas_tempo:
        if coluna in df2.columns:
            df2[coluna] = (
                df2[coluna] / 1_000_000
            ).round(3)

    # Renomeando as colunas
    df2.rename(columns={
        'Time': 'Tempo',
        'Driver': 'Piloto',
        'DriverNumber': 'Numero_Piloto',
        'LapTime': 'Tempo_Volta',
        'LapNumber': 'Numero_Volta',
        'Stint': 'Stint',
        'PitOutTime': 'Tempo_Saida_Pit',
        'PitInTime': 'Tempo_Entrada_Pit',
        'Sector1Time': 'Tempo_Setor_1',
        'Sector2Time': 'Tempo_Setor_2',
        'Sector3Time': 'Tempo_Setor_3',
        'SpeedI1': 'Velocidade_Setor_1',
        'SpeedI2': 'Velocidade_Setor_2',
        'SpeedFL': 'Velocidade_Final',
        'SpeedST': 'Velocidade_Reta',
        'IsPersonalBest': 'Melhor_Volta',
        'Compound': 'Composto',
        'TyreLife': 'Vida_Pneu',
        'FreshTyre': 'Pneu_Novo',
        'Team': 'Equipe',
        'LapStartTime': 'Inicio_Volta',
        'LapStartDate': 'Data_Inicio_Volta',
        'TrackStatus': 'Status_Pista',
        'IsAccurate': 'Volta_Precisa'
    }, inplace=True)

    # Removendo colunas que não são necessárias
    df2.drop(
        columns=[
            'Position',
            'Deleted',
            'DeletedReason',
            'FastF1Generated'
        ],
        inplace=True,
        errors='ignore'
    )

    return df2


def transformDataTelemetry(df):
    
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
def savingData_Silver(stage,year,place,quali):
   try:
    caminho = Path(__file__).parent / f"{stage}"/ "telemetry" /f'year={year}'/f'place={place}'/f'quali={quali}'
    caminho2 = Path(__file__).parent / f"{stage}" / "Data_Laps" /f"year={year}" /f"place={place}" /f"quali={quali}"
    caminho.mkdir(parents=True,exist_ok=True)
    caminho2.mkdir(parents=True,exist_ok=True)
    dados,dados1 = readDatabase(year, place, quali)
    dataTransform = transformDataTelemetry(dados)
    dataTransformlaps = transformDataLaps(dados1)
    arquivo = caminho / f'dados_telemetry_{stage}_{place}_{year}.parquet'
    arquivo2 = caminho2 / f'dados_voltas_{stage}_{place}_{year}.parquet'
    dataTransformlaps.to_parquet(arquivo2,index=False)
    dataTransform.to_parquet(arquivo,index = False)
   except ValueError:
      print('Erro ao tentar salvar')

savingData_Silver('silver',2025, 'monaco','Q')
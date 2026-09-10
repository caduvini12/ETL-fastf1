from pathlib import Path
import pandas as pd

def readDatabaseBronze(year, place,quali):

 caminho = Path(__file__).parent / "bronze" / "telemetry" /f"year={year}" /f"place={place}" /f"quali={quali}"
 caminho2 = Path(__file__).parent / "bronze" / "Data_Laps" /f"year={year}" /f"place={place}" /f"quali={quali}"
 arquivo = caminho / f'dados_fastf1_{place}_{year}.parquet'
 arquivo2 = caminho2 / f'dados_voltas_{place}_{year}.parquet'
 df = pd.read_parquet(arquivo,engine ='fastparquet')
 df2 = pd.read_parquet(arquivo2,engine = 'fastparquet')

 return df,df2

def transformDataVoltas(df2):
  df2 = df2[df2['IsAccurate']]

  df2['LapTime'] = (
  df2['LapTime'] / 1_000_000_000).round(3)

  df2['Sector1Time'] =( df2['Sector1Time'] / 1_000_000_000).round(3)

  df2['Sector2Time'] =( df2['Sector2Time'] / 1_000_000_000).round(3)

  df2['Sector3Time'] =( df2['Sector3Time'] / 1_000_000_000).round(3)

  df2.rename(columns={
        'Time': 'Tempo',
        'Driver': 'Piloto',                
        'DriverNumber': 'Numero_Piloto',
        'LapTime': 'Tempo_Volta',
        'LapNumber': 'Numero_Volta',
        'Stint': 'Turno_Pneu',
        'Sector1Time': 'Tempo_Setor_1',
        'Sector2Time': 'Tempo_Setor_2',
        'Sector3Time': 'Tempo_Setor_3',
        'FreshTyre': 'Pneu_Novo',
        'Team': 'Equipe',
        'LapStartTime': 'Tempo_Inicio_Volta',
        'LapStartDate': 'Data_Inicio_Volta',
        'TrackStatus': 'Status_Pista',
        'IsAccurate': 'Volta_Precisa'
        },inplace=True)
                        
  df2.drop(columns=[
  'PitInTime', 
  'PitOutTime',
  'DeletedReason',
  'Deleted', 
  'Position',
  'FastF1Generated'
   ],
   inplace =True,
   errors = 'ignore') 
       # Adicionado inplace=True para aplicar as mudanças diretamente

  return df2

def transformDataTelemetria(df):

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
    caminho = Path(__file__).parent / "silver" /"telemetry" /f'year={year}'/f'place={place}'/f'quali={quali}'
    caminho2 = Path(__file__).parent / "silver" / "Data_Laps" /f"year={year}" /f"place={place}" /f"quali={quali}" 
    caminho.mkdir(parents=True,exist_ok=True)
    caminho2.mkdir(parents=True,exist_ok=True)
    telemetry, Laps = readDatabaseBronze(year, place, quali)
    dataTransform = transformDataTelemetria(telemetry)
    dataTransform2 = transformDataVoltas(Laps)
    arquivo = caminho / f'dados_silver_{place}_{year}.parquet'
    arquivo2 = caminho2 / f'dados_voltas_{place}_{year}.parquet'
    dataTransform.to_parquet(arquivo,index = False)
    dataTransform2.to_parquet(arquivo2,index = False)
   except FileNotFoundError:
      print('Erro ao tentar salvar dados da telemtria')



savingData_Silver(2025, 'monaco','Q')
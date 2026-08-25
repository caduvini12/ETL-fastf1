import fastf1
import pandas as pd
from pathlib import Path

def extractData (year, place, quali):
 caminho = Path(__file__).parent / "bronze" / "telemetry" /f"year={year}" /f"place={place}" /f"quali={quali}"
 caminho.mkdir(parents=True, exist_ok=True)  
 caminho2 = Path(__file__).parent / "bronze" / "Data_Laps" /f"year={year}" /f"place={place}" /f"quali={quali}"
 caminho2.mkdir(parents=True, exist_ok=True)
 session = fastf1.get_session(year, place, quali)
 session.load()
 DataLaps_list = []
 telemetry_list = []
 failad_laps = []
 for x, y in session.laps.iterlaps():
  try:
   #dados de telemetria
   telemetry = y.get_telemetry()
   telemetry['Driver'] = y.Driver
   telemetry['LapNumber'] = y.LapNumber

   #dados de voltas
   dataLaps = y.to_frame().T
   dataLaps['Driver'] = y.Driver
   dataLaps['LapNumber'] = y.LapNumber

   # salvando nas listas
   DataLaps_list.append(dataLaps)
   telemetry_list.append(telemetry)
  except ValueError:
   driver_error = y.Driver
   lap_error = y.LapNumber
   error = {"driver": driver_error, "lap": lap_error}
   failad_laps.append(error)
 
   
  
 if telemetry_list:
  df = pd.concat(telemetry_list, ignore_index = True)
  arquivo = caminho / f'dados_fastf1_{place}_{year}.parquet'
  df.to_parquet(arquivo, index=False)
  df2 = pd.DataFrame(failad_laps)
  arquivo2 = caminho2 / f'voltas_sem_dados_{place}_{year}.csv'
  df2.to_csv(arquivo2, index=False)

  df3 = pd.concat(DataLaps_list, ignore_index= True)
  arquivo3 = caminho2 / f'dados_voltas_{place}_{year}.parquet'
  df3.to_parquet(arquivo3, index=False)

  return df,df3,failad_laps

extractData(2025, 'monaco', 'Q')
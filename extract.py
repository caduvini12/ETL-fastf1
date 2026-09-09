import fastf1
import pandas as pd
from pathlib import Path

def extractData (year, place, quali):
 DataLaps_list = []
 telemetry_list = []
 failad_laps = []
 
 caminho = Path(__file__).parent / "bronze" / "telemetry" /f"year={year}" /f"place={place}" /f"quali={quali}"
 caminho.mkdir(parents=True, exist_ok=True)  
 caminho2 = Path(__file__).parent / "bronze" / "Data_Laps" /f"year={year}" /f"place={place}" /f"quali={quali}"
 caminho2.mkdir(parents=True, exist_ok=True)
 session = fastf1.get_session(year, place, quali)
 session.load()
 DataLaps_list = session.laps
 

 
 for x, y in session.laps.iterlaps():
  try:
   #dados de telemetria
   telemetry = y.get_telemetry()
   telemetry['Driver'] = y.Driver
   telemetry['LapNumber'] = y.LapNumber
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
  arquivo2 = caminho / f'voltas_sem_dados_{place}_{year}.csv'
  df2.to_csv(arquivo2, index=False)

  
  arquivo3 = caminho2 / f'dados_voltas_{place}_{year}.parquet'
  DataLaps_list.to_parquet(arquivo3, index=False)

  return df,failad_laps

extractData(2025, 'monaco', 'Q')
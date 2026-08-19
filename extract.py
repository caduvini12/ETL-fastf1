import fastf1
import pandas as pd
from pathlib import Path

def extractData (year, place, quali):
 arquivo = Path(__file__).parent / "bronze" /f"year={year}" /f"place={place}" /f"quali={quali}"
 arquivo.mkdir(parents=True, exist_ok=True)  
 session = fastf1.get_session(year, place, quali)
 session.load()

 telemetry_list = []
 failad_laps = []
 for x, y in session.laps.iterlaps():
  try:
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
  caminho_final1 = arquivo / f'dados_fastf1_{place}_{year}.parquet'
  df.to_parquet(caminho_final1, index=False)
  df2 = pd.DataFrame(failad_laps)
  caminho_final2 = arquivo / f'voltas_sem_dados_{place}_{year}.csv'
  df2.to_csv(caminho_final2, index=False)
  return df, failad_laps

extractData(2026, 'monaco', 'Q')
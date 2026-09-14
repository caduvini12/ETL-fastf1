import boto3
from pathlib import Path

def savingS3_Bronze(year,place,quali):
  caminho = Path(__file__).parent / "bronze" / "telemetry" /f"year={year}" /f"place={place}" /f"quali={quali}"
  caminho2 = Path(__file__).parent / "bronze" / "Data_Laps" /f"year={year}" /f"place={place}" /f"quali={quali}"
  arquivo = caminho / f'dados_fastf1_{place}_{year}.parquet'
  arquivo2 = caminho2 / f'dados_voltas_{place}_{year}.parquet'
  bucket_name = "fastf1-datalake-caduvini"
  session = boto3.Session()
  s3_client = session.client('s3')
  s3_client.upload_file(
     Filename=str(arquivo),
     Bucket=bucket_name,
     Key=f'bronze/telemtry/year={year}/place={place}/quali={quali}/{arquivo.name}'
    )
  s3_client.upload_file(
      Filename=str(arquivo2),
      Bucket=bucket_name,
      Key=f'bronze/Data_Laps/year={year}/place={place}/quali={quali}/{arquivo2.name}'
    )

def savingS3_Silver(year,place,quali):
  caminho = Path(__file__).parent / "silver" / "telemetry" /f"year={year}" /f"place={place}" /f"quali={quali}"
  caminho2 = Path(__file__).parent / "silver" / "Data_Laps" /f"year={year}" /f"place={place}" /f"quali={quali}"
  bucket_name = "fastf1-datalake-caduvini"
  session = boto3.Session()
  s3_client = session.client('s3')
  s3_client.upload_file(

  )

def savingS3_Gold(year,place,quali):
  bucket_name = "fastf1-datalake-caduvini"
  session = boto3.Session()
  s3_client = session.client('s3')
  s3_client.upload_file(

  )
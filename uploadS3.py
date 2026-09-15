import boto3
from pathlib import Path

def savingS3_stage(stage,year,place,quali):
  caminho = Path(__file__).parent / f"{stage}" / "telemetry" /f"year={year}" /f"place={place}" /f"quali={quali}"
  caminho2 = Path(__file__).parent / f"{stage}" / "Data_Laps" /f"year={year}" /f"place={place}" /f"quali={quali}"
  arquivo = caminho / f'dados_telemetry_{stage}_{place}_{year}.parquet'
  arquivo2 = caminho2 / f'dados_voltas_{stage}_{place}_{year}.parquet'
  bucket_name = "fastf1-datalake-caduvini"
  session = boto3.Session()
  s3_client = session.client('s3')
  s3_client.upload_file(
     Filename=str(arquivo),
     Bucket=bucket_name,
     Key=f'{stage}/telemetry/year={year}/place={place}/quali={quali}/{arquivo.name}'
    )
  s3_client.upload_file(
      Filename=str(arquivo2),
      Bucket=bucket_name,
      Key=f'{stage}/Data_Laps/year={year}/place={place}/quali={quali}/{arquivo2.name}'
    )


def savingS3_gold(year,place,quali):
  caminho = Path(__file__).parent / "gold" /f"year={year}" /f"place={place}" /f"quali={quali}"
  arquivo = caminho / f'dados_gold_{place}_{year}.parquet'
  bucket_name = "fastf1-datalake-caduvini"
  session = boto3.Session()
  s3_client = session.client('s3')
  s3_client.upload_file(
     Filename=str(arquivo),
     Bucket=bucket_name,
     Key=f'gold/year={year}/place={place}/quali={quali}/{arquivo.name}'
    )

savingS3_gold(2025,'monaco','Q')
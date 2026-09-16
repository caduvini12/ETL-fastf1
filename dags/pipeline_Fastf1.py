from airflow.decorators import dag, task
from datetime import datetime
from transformData import savingData_Silver
from transformGold import savingGold
from uploadS3 import savingS3_gold, savingS3_stage


@dag(
    dag_id='dag_fastf1_pipeline',
    start_date=datetime(2026,1,1),
    schedule='@daily',
    catchup=False
)
def pipelineFastf1():
    
    @task
    def transfromSilver():
     savingData_Silver('silver',2025,'monaco','Q')
     print("etapa silver Pipeline concluida!")

    @task
    def transfromGold(): 
     savingGold('gold',2025,'monaco','Q')
     print("etapa gold Pipeline concluida!")

    @task
    def SavingS3Bronze():
      savingS3_stage('bronze',2025,'monaco','Q')
      print("dados bronze salvos na S3")

    @task
    def SavingS3Silver():
        savingS3_stage('silver',2025,'monaco','Q')
        print("dados Silver salvos na S3")

    @task
    def Savings3Gold():
      savingS3_gold(2025,'monaco','Q')
      print("dados Gold salvos na S3")

      
      

   
    task1 = transfromSilver()
    task2 = transfromGold()
    task3 = SavingS3Bronze()
    task4 = SavingS3Silver()
    task5 = Savings3Gold()

    task1 >> task2 >> task3 >> task4 >> task5

my_dag = pipelineFastf1()
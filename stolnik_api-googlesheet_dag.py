from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

sys.path.append('/srv/stolnik_api-googlesheet')

from main import main

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='run_stolnik_skrapper',
    default_args=default_args,
    description='запуск скраппера цен и запись в гугл таблицу',
    schedule_interval='daily',
    start_date=datetime(2025, 9, 26),
    catchup=True,
    tags='StolnikApi+GoogleSheet',
    max_active_runs=1
) as dag:

    run_script = PythonOperator(
        task_id='run_stolnik_skrapper',
        python_callable=main)
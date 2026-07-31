from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='krovatik_ads_load',
    default_args=default_args,
    description='инкрементальная загрузка объявлений Postgres -> ClickHouse',
    schedule_interval="0 8 * * *",
    start_date=datetime(2026, 7, 31),
    catchup=False,
    tags=['krovatik'],
    max_active_runs=1
) as dag:

    load_ads = BashOperator(
        task_id='load_ads',
        bash_command='python /opt/airflow/dags/krovatik-analytics/scripts/load_ads.py')

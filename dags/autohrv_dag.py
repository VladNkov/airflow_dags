from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from autohrv.autohrv_main import main as autohrv_main


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='autohrv_run',
    default_args=default_args,
    description='запуск парсера сайта autohrv и запись в бд',
    schedule_interval='0 */6 * * *',
    start_date=datetime(2025, 11, 16),
    catchup=False,
    tags=['autohrv'],
    max_active_runs=1
) as dag:

    run_script = PythonOperator(
        task_id='run_autohrv',
        python_callable=autohrv_main)
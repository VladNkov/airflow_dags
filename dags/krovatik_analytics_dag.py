from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import timedelta
import pendulum


PROJECT_DIR = "/opt/airflow/dags/krovatik-analytics"
DBT_PROJECT_DIR = f"{PROJECT_DIR}/dbt_krovatik"
DBT_PROFILES_DIR = "/opt/airflow/.dbt"
DBT_BIN = "/home/airflow/dbt-venv/bin/dbt"
DBT_TARGET = "prod"


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=3),
}


with DAG(
    dag_id="krovatik_ads_load",
    default_args=default_args,
    description="Postgres → ClickHouse → dbt",
    schedule_interval="0 6 * * *",
    start_date=pendulum.datetime(2026, 7, 31, tz="Europe/Zagreb",),
    catchup=False,
    tags=["krovatik"],
    max_active_runs=1,
) as dag:

    load_ads = BashOperator(
        task_id="load_ads",
        bash_command=f"python {PROJECT_DIR}/scripts/load_ads.py",
    )

    dbt_seed = BashOperator(
        task_id="dbt_seed",
        bash_command=(
            f"{DBT_BIN} seed "
            f"--project-dir {DBT_PROJECT_DIR} "
            f"--profiles-dir {DBT_PROFILES_DIR} "
            f"--target {DBT_TARGET}"
    ),
    append_env=True,
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=(
            f"{DBT_BIN} run "
            f"--project-dir {DBT_PROJECT_DIR} "
            f"--profiles-dir {DBT_PROFILES_DIR} "
            f"--target {DBT_TARGET}"
    ),
    append_env=True,
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=(
            f"{DBT_BIN} test "
            f"--project-dir {DBT_PROJECT_DIR} "
            f"--profiles-dir {DBT_PROFILES_DIR} "
            f"--target prod"
        ),
        append_env=True,
    )

    load_ads >> dbt_seed >> dbt_run >> dbt_test
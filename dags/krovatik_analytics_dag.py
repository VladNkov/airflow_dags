from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import timedelta
import pendulum


PROJECT_DIR = "/opt/airflow/dags/krovatik-analytics"
DBT_PROJECT_DIR = f"{PROJECT_DIR}/dbt_krovatik"
DBT_PROFILES_DIR = "/opt/airflow/.dbt"
UV_BIN = "/home/airflow/.local/bin/uv"
UV_ENV = "/tmp/krovatik-venv"
DBT_TARGET = "prod"

UV_RUN = (
    f"UV_PROJECT_ENVIRONMENT={UV_ENV} "
    f"{UV_BIN} run "
    f"--frozen "
    f"--python /usr/local/bin/python "
    f"--project {PROJECT_DIR}"
)



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
    schedule_interval="*/30 * * * *",
    start_date=pendulum.datetime(2026, 7, 31, tz="Europe/Zagreb",),
    catchup=False,
    tags=["krovatik"],
    max_active_runs=1,
) as dag:

    load_ads = BashOperator(
    task_id="load_ads",
    bash_command=(
        f"{UV_RUN} python "
        f"{PROJECT_DIR}/scripts/load_ads.py"
    ),
    append_env=True,
)

dbt_seed = BashOperator(
    task_id="dbt_seed",
    bash_command=(
        f"{UV_RUN} dbt seed "
        f"--project-dir {DBT_PROJECT_DIR} "
        f"--profiles-dir {DBT_PROFILES_DIR} "
        f"--target {DBT_TARGET}"
    ),
    append_env=True,
)

dbt_run = BashOperator(
    task_id="dbt_run",
    bash_command=(
        f"{UV_RUN} dbt run "
        f"--project-dir {DBT_PROJECT_DIR} "
        f"--profiles-dir {DBT_PROFILES_DIR} "
        f"--target {DBT_TARGET}"
    ),
    append_env=True,
)

dbt_test = BashOperator(
    task_id="dbt_test",
    bash_command=(
        f"{UV_RUN} dbt test "
        f"--project-dir {DBT_PROJECT_DIR} "
        f"--profiles-dir {DBT_PROFILES_DIR} "
        f"--target {DBT_TARGET}"
    ),
    append_env=True,
)

load_ads >> dbt_seed >> dbt_run >> dbt_test
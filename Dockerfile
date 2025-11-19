FROM apache/airflow:2.9.2

ENV PYTHONPATH="/opt/airflow/dags"

COPY dags/stolnik_google_sheet/requirements.txt /tmp/sgs_requirements.txt
RUN pip install --no-cache-dir -r /tmp/sgs_requirements.txt

COPY dags/autohrv/requirements.txt /tmp/autohrv_requirements.txt
RUN pip install --no-cache-dir -r /tmp/autohrv_requirements.txt

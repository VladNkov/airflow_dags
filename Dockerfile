FROM apache/airflow:2.9.2

# Устанавливаем Python-зависимости
COPY dags/stolnik+google_sheet/requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
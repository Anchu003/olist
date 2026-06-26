FROM apache/airflow:2.5.0


COPY requirements.txt /requirements.txt


RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt


COPY ./etl_module /opt/airflow/etl_module


ENV PYTHONPATH "${PYTHONPATH}:/etl_module"
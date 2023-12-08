from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator 
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.decorators import task
from airflow.models import XCom
from airflow.utils.db import provide_session
from airflow.models import Variable
import urllib.parse
from datetime import datetime, timedelta
import os 

yday = datetime.combine(datetime.today() - timedelta(1),
                                  datetime.min.time())

def _get_events_data(ti):
    data = ti.xcom_pull(task_ids=['get_events'])
    print(data)
    file_name = data[0]
    Variable.set(key="file_name", value=file_name)
    print(file_name)


def get_active_files():
    request = "SELECT * FROM public.events where is_proc is false;"
    pg_hook = PostgresHook(postgres_conn_id="postgres_default",schema='minio')
    connection=pg_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(request)
    sources = cursor.fetchone()
    for source in sources:
        print(source)
    if len(sources)>0:
        return sources[0]
    else:
        raise 'No new data'
        
def set_file_status():
    file_name = Variable.get('file_name')
    request = f"BEGIN;update public.events set is_proc=true where is_proc is false and \"key\" like \'{file_name}\';END;"
    print(request)
    pg_hook = PostgresHook(postgres_conn_id="postgres_default",schema='minio')
    connection=pg_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(request)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': yday,
    'retries': 60,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG('s3_file_sensor', default_args=default_args, schedule_interval='@hourly',
    max_active_runs=1,catchup=False)

get_events = PythonOperator(
        task_id="get_events",
        python_callable=get_active_files,
        dag=dag
    )

get_events_data = PythonOperator(
        task_id='get_events_data',
        python_callable=_get_events_data,
        dag=dag,
        provide_context=True
    )

@provide_session
def clean_xcom(session=None, **context):
    dag = context["dag"]
    dag_id = dag._dag_id 
    session.query(XCom).filter(XCom.dag_id == dag_id).delete()

delete_xcom = PythonOperator(
    task_id="delete_xcom",
    python_callable = clean_xcom, 
    dag=dag
)

processing = SparkSubmitOperator(
    task_id="processing",
    application="/opt/airflow/dags/scripts/arg_etl.py",
    conn_id="spark_conn",
    verbose=False,
    application_args=['--file', Variable.get('file_name')],
    dag=dag
)

set_file_proc = PythonOperator(
        task_id="set_file_status",
        python_callable=set_file_status,
        dag=dag
    )

get_events >> get_events_data >> delete_xcom >>  processing >> set_file_proc

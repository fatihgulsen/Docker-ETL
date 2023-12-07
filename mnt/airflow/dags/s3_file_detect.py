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

yday = datetime.combine(datetime.today() - timedelta(1),
                                  datetime.min.time())

def _get_events_data(ti):
    data = ti.xcom_pull(task_ids=['get_events'])
    # print(data)
    bucket_name = data[0][0][1]['Records'][0]['s3']['bucket']['name']
    file_name = urllib.parse.unquote(data[0][0][1]['Records'][0]['s3']['object']['key'])
    Variable.set(key="bucket_name", value=bucket_name)
    Variable.set(key="file_name", value=file_name)
    # print(bucket_name,file_name)


def get_active_files():
    request = "SELECT * FROM public.events where is_proc is false;"
    pg_hook = PostgresHook(postgres_conn_id="postgres_default",schema='minio')
    connection=pg_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(request)
    sources = cursor.fetchall()
    for source in sources:
        print(source)
    if len(sources)>0:
        return sources
    else:
        raise 'No new data'
        

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': yday,
    'retries': 60*24,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG('s3_file_sensor', default_args=default_args, schedule_interval='@daily',
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

s3_file_test = S3KeySensor(
    task_id='s3_file_test',
    soft_fail=True,
    bucket_key=Variable.get('file_name'),
    bucket_name=Variable.get('bucket_name'),
    aws_conn_id='aws_default',
    dag=dag)

processing = SparkSubmitOperator(
    task_id="processing",
    application="/opt/airflow/dags/scripts/arg_etl.py",
    conn_id="spark_conn",
    verbose=False,
    application_args=['--file', Variable.get('file_name')],
    dag=dag
)


get_events >> get_events_data >> delete_xcom >> s3_file_test >> processing

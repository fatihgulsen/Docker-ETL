from pyspark.sql import SparkSession,functions as F
from pyspark import SparkContext, SparkConf, SQLContext
import argparse
from os.path import abspath

parser = argparse.ArgumentParser(description='Argentina ETL')
parser.add_argument("-f", "--file", help="File name by s3", nargs='*')
args = parser.parse_args()

file_name = "gergia_new_ta_code.csv"
if args.file[0]:
    file_name = args.file[0]

warehouse_location = abspath('spark-warehouse')

appName = "Spark ML Pipelines"
master = "spark://spark-master:7077"
number_of_core = 16

conf = SparkConf() \
    .setAppName(appName) \
    .set("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
    .set("spark.hadoop.fs.s3a.access.key", "minio") \
    .set("spark.hadoop.fs.s3a.secret.key", "miniosecret") \
    .set("spark.hadoop.fs.s3a.path.style.access", "true") \
    .set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .set("spark.sql.warehouse.dir", warehouse_location) \

sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)
spark = sqlContext.sparkSession


def read_csv_table(csv_dir, sep=';'):
    df = spark.read \
        .option("delimiter", sep) \
        .csv(csv_dir, header='true')
    return df


def write_csv(df, csv_dir='/tmp/spark_output/csv', sep="|", write_method="overwrite"):
    df.repartition(4) \
        .write \
        .csv(path=f"s3a://{csv_dir}",
             compression='gzip',
             sep=sep,
             header=True,
             mode=write_method,
             quote='"',
             lineSep='\n'
             )


# df = read_csv_table(f'file:///opt/airflow/dags/files/gergia_new_ta_code.csv', ';')
df = read_csv_table(f's3a://argentina/{file_name}', ';')

write_csv(df, csv_dir=f'argentina/add_{file_name}')

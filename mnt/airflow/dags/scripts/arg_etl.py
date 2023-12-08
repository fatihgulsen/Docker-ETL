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

appName = f"Argentina ETL {file_name}"

conf = SparkConf() \
    .setAppName(appName) \
    .set("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
    .set("spark.hadoop.fs.s3a.access.key", "minio") \
    .set("spark.hadoop.fs.s3a.secret.key", "miniosecret") \
    .set("spark.hadoop.fs.s3a.path.style.access", "true") \
    .set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .set("spark.sql.warehouse.dir", warehouse_location) \
    .set('spark.rapids.sql.enabled', 'true') \
    .set("spark.sql.execution.arrow.pyspark.enabled", "true") \
    .set("spark.driver.extraClassPath", "enu/jars/mssql-jdbc-12.4.2.jre8.jar")

sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)
spark = sqlContext.sparkSession


def read_csv_table(csv_dir, sep=';'):
    df = spark.read \
        .option("delimiter", sep) \
        .csv(csv_dir, header='true')
    return df


def write_csv(df, csv_dir='/tmp/spark_output/csv', sep="|", write_method="overwrite"):
    csv_dir = csv_dir.replace('yeni_','')
    csv_dir = csv_dir.replace('.csv','')
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


def write_sql(df,table_name='temp'):
    table_name = table_name.replace('yeni_','')
    table_name = table_name.replace('.csv','')
    df.write \
        .format("jdbc") \
        .mode("append") \
        .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
        .option("url", "jdbc:sqlserver://10.5.0.100:1433; databaseName=test; encrypt=true; trustServerCertificate=false") \
        .option("dbtable", table_name) \
        .option("user", "sa") \
        .option("password", "TradeAtlas*") \
        .save()

df = read_csv_table(f's3a://{file_name}', ';')

write_csv(df, csv_dir=f'{file_name}_file-export')

write_sql(df,table_name=file_name)

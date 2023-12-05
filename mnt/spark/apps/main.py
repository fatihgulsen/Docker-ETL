from pyspark.sql import SparkSession, functions as F
from pyspark import SparkContext

"""
Test String


"""

# from ProcData import tables
import pyspark
from pyspark import SparkContext, SparkConf, SQLContext
from pyspark.sql.functions import col, when, regexp_replace
from pyspark.sql import functions as F
from functools import reduce, partial
import os

appName = "Spark ML Pipelines"
master = "spark://spark-master:7077"
number_of_core = 16

conf = SparkConf() \
    .setAppName(appName) \
    .setMaster(master) \
    .set("spark.hadoop.mapreduce.fileoutputcommitter.marksuccessfuljobs", "false") \
    .set("spark.driver.maxResultSize", "32g") \
    .set("spark.executor.cores", str(number_of_core)) \
    .set("spark.driver.cores", str(number_of_core // 4)) \
    .set("spark.executor.memory", "8G") \
    .set("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
    .set("spark.hadoop.fs.s3a.access.key", "minio") \
    .set("spark.hadoop.fs.s3a.secret.key", "miniosecret") \
    .set("spark.hadoop.fs.s3a.path.style.access", "true") \
    .set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")

sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)
spark = sqlContext.sparkSession


def read_csv_table(csv_dir, sep=';'):
    df = spark.read \
        .option("delimiter", sep) \
        .csv(csv_dir, header='true')
    return df

def write_csv(df, csv_dir='tmp/spark_output/csv', sep="|", write_method="overwrite"):
    appID = sc._jsc.sc().applicationId()
    df.repartition(number_of_core) \
        .write \
        .csv(path=f"s3a://{csv_dir}/{appID}",
             compression='gzip',
             sep=sep,
             header=True,
             mode=write_method,
             quote='"',
             lineSep='\n'
             )


df = read_csv_table('s3a://gold-bucket/gergia_new_ta_code.csv', ';')
# write_csv(df,'gold-bucket/test_gergia_new_ta_code')
write_csv(df)
# df.show()

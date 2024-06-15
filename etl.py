import os
from pyspark.sql import SparkSession
from delta import *

# Set up Spark session
builder = SparkSession.builder.appName("DeltaLakeExample") \
    .config("spark.jars.packages", "io.delta:delta-core_2.12:1.0.0") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()


raw_data_path = "metrics.csv"
delta_table_path = "data/delta_table"

# Extract
df = spark.read.format("csv").option("header", "true").load(raw_data_path)


# Transform
transformed_df = df.withColumnRenamed("value", "values")


#transformed_df.write.format("delta").option("mergeSchema", "true").mode("overwrite").save(delta_table_path)
transformed_df.write.format("delta").mode("overwrite").option("overwriteSchema","true").save(delta_table_path)



# load
transformed_df.write.format("delta").mode("overwrite").save(delta_table_path)

# Read
delta_df = spark.read.format("delta").load(delta_table_path)
delta_df.show()

spark.stop()

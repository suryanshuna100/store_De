from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    to_timestamp,
    year,
    month,
    dayofmonth,
    hour,
    round as spark_round
)

import glob

# ---------------------------------
# Create Spark Session
# ---------------------------------
spark = (
    SparkSession.builder
    .appName("SilverPartitioned")
    .getOrCreate()
)

print("Spark Session Created")

# ---------------------------------
# Read All Bronze Weather Files
# ---------------------------------
files = glob.glob(
    "data/raw/weather/year=*/month=*/day=*/hour=*/weather.json"
)

print(f"Files Found: {len(files)}")

df = (
    spark.read
    .option("multiline", "true")
    .json(files)
)

print("===== RAW DATA =====")

df.show(truncate=False)

print("===== RAW SCHEMA =====")

df.printSchema()

# ---------------------------------
# Silver Transformations
# ---------------------------------
df = (
    df
    .withColumn(
        "temperature",
        col("temperature").cast("double")
    )
    .withColumn(
        "humidity",
        col("humidity").cast("integer")
    )
    .withColumn(
        "pressure",
        col("pressure").cast("integer")
    )
    .withColumn(
        "wind_speed",
        col("wind_speed").cast("double")
    )
    .withColumn(
        "ingestion_ts",
        to_timestamp("ingestion_timestamp")
    )
    .withColumn(
        "temperature_f",
        spark_round(
            (col("temperature") * 9 / 5) + 32,
            2
        )
    )
    .withColumn(
        "year",
        year("ingestion_ts")
    )
    .withColumn(
        "month",
        month("ingestion_ts")
    )
    .withColumn(
        "day",
        dayofmonth("ingestion_ts")
    )
    .withColumn(
        "hour",
        hour("ingestion_ts")
    )
)

print("===== TRANSFORMED SCHEMA =====")

df.printSchema()

print("===== TRANSFORMED DATA =====")

df.show(truncate=False)

# ---------------------------------
# Sample Aggregation
# ---------------------------------
print("===== WEATHER COUNT =====")

(
    df.groupBy("weather")
    .count()
    .show()
)

# ---------------------------------
# Partitioned Silver Path
# ---------------------------------
silver_path = "data/silver/weather"

print("===== WRITING PARTITIONED SILVER =====")

(
    df.write
    .mode("overwrite")
    .partitionBy(
        "year",
        "month",
        "day"
    )
    .parquet(silver_path)
)

print(
    f"Partitioned Silver written to: {silver_path}"
)

# ---------------------------------
# Read Back Silver
# ---------------------------------
print("===== READING SILVER =====")

silver_df = spark.read.parquet(
    silver_path
)

silver_df.printSchema()

silver_df.show(
    truncate=False
)

# ---------------------------------
# Stop Spark Session
# ---------------------------------
spark.stop()

print("Spark Session Stopped")

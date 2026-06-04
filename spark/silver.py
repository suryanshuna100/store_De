from pyspark.sql import SparkSession
import glob
from pyspark.sql.functions import round as spark_round

files = glob.glob(
    "data/raw/weather/year=*/month=*/day=*/hour=*/weather.json"
)


spark = (
    SparkSession.builder
    .appName("SilverLayer")
    .getOrCreate()
)

print("Spark Session Created")

df = (
    spark.read
    .option("multiline", "true")
    .json(
        files
    )
)

df.show(truncate=False)
df.printSchema()



from pyspark.sql.functions import col, to_timestamp

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
)

df.printSchema()

from pyspark.sql.functions import year, month, dayofmonth, hour

df = (
    df
    .withColumn("year", year("ingestion_ts"))
    .withColumn("month", month("ingestion_ts"))
    .withColumn("day", dayofmonth("ingestion_ts"))
    .withColumn("hour", hour("ingestion_ts"))
    .withColumn(
    "temperature_f",
    spark_round(
        (col("temperature") * 9/5) + 32,
        2
    )
))

df.groupBy("weather").count().show()

df.orderBy(col("temperature").desc()).show()

# Silver layer output location
silver_path = "data/silver/weather"

print("===== WRITING SILVER LAYER =====")

(
    df.write
    .mode("overwrite")
    .parquet(silver_path)
)

print(f"Silver data written successfully to: {silver_path}")

print("===== READING SILVER LAYER =====")

silver_df = spark.read.parquet(
    silver_path
)

print("===== SILVER DATA =====")

silver_df.show(truncate=False)

print("===== SILVER SCHEMA =====")

silver_df.printSchema()

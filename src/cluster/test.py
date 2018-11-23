import os.path
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
spark = SparkSession.builder.getOrCreate()
sc = spark.sparkContext

from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)

# loading the saved parquet files
DATA_DIR = "/user/terenzi/wikipedia_1e-05.parquet"
wikipedia = spark.read.parquet(DATA_DIR)
wikipedia.select('title').head(5)


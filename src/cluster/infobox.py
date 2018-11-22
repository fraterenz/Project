from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
import findspark
findspark.init()


spark = SparkSession.builder.getOrCreate()
sc = spark.sparkContext

sqlContext = SQLContext(sc)

DATA_DIR = "enwiki-20180920"

wikipedia = spark.createDataFrame(sqlContext.read.format('com.databricks.spark.xml').options(rowTag='page')
                                  .load(os.path.join(DATA_PATH, "enwiki-20180920-pages-articles-multistream.xml"))
                                  .head(10000))

wikipedia.filter("ns = '0'")\
    .select("revision.text._VALUE")\
    .filter("_VALUE like '%{{Infobox military conflict%'")\
    .show(2)

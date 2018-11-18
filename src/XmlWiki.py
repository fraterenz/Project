import json
import findspark
from pyspark.sql.types import StructType
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
findspark.init()
spark = SparkSession.builder.getOrCreate()
sc = spark.sparkContext
sqlContext = SQLContext(sc)


class XmlWiki():
    def __init__(self, path, path_schema, use_schema=False, sampling_ratio=.4, rowTag='page'):
        self.path = path
        self.sampling_ratio = sampling_ratio
        self.rowTag = rowTag
        self.path_schema = path_schema
        self.schema = None
        self.use_schema = use_schema
        self.dataframe = self.__load_xml()

    def __load_xml(self):
        if self.use_schema:
            print('Loading the xml schema from {}'.format(self.path_schema))
            xml = sqlContext.read.format('com.databricks.spark.xml') \
                .options(samplingRatio=self.sampling_ratio) \
                .options(rowTag=self.rowTag) \
                .load(self.path, schema=self.__load_schema())
        else:
            xml = sqlContext.read.format('com.databricks.spark.xml') \
                .options(samplingRatio=self.sampling_ratio) \
                .options(rowTag=self.rowTag) \
                .load(self.path)
            self.schema = xml.schema
            # dump schema
            self.__dump_schema()
        xml.printSchema()
        return xml

    def __load_schema(self):
        # schema_json = spark.read.text(self.path_schema).first()[0]
        # return StructType.fromJson(json.loads(schema_json))
        with open(self.path_schema, 'r') as f_toread:
            schema_json = json.load(f_toread)
        return StructType.fromJson(schema_json)

    def __dump_schema(self):
        print('Saving schema in {} \n'.format(self.path_schema))
        with open(self.path_schema, "w") as write_file:
            json.dump(self.schema.jsonValue(), write_file, indent=2)

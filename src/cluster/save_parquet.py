import argparse
import os.path
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext

spark = SparkSession.builder.getOrCreate()
sc = spark.sparkContext

sqlContext = SQLContext(sc)

DATA_DIR = "/datasets/enwiki-20180920"
PARQUET_DIR = "/user/terenzi"

parser = argparse\
    .ArgumentParser(description='''Save huge file into parquet specifying the nb of records to sample from file''')

parser.add_argument(
    '-ratio',
    metavar='ratio',
    type=float,
    required=True,
    help='''Number of records to subsample from the file'''
)

args = vars(parser.parse_args())
if args['ratio'] > 1. or args['ratio'] < 0.:
    raise ValueError('must be between 0 and 1, not {}'.format(args['ratio'] ))
#if args['ratio'] > .5:
#    raise Warning('Will be a lot of data!')
else:
    n_ratio = args['ratio']


# n_ratio = 0.01
print('start loading data')
wikipedia = sqlContext.read.format('com.databricks.spark.xml').options(rowTag='page').options(samplingRatio=n_ratio).load(os.path.join(DATA_DIR, "enwiki-20180920-pages-articles-multistream.xml"))
print('saving into parquet')
# saving binary file to future uses
wikipedia.write.parquet(os.path.join(PARQUET_DIR, "wikipedia_{}.parquet".format(n_ratio)))


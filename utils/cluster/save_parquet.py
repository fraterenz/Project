import argparse
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext


def main():

    parser = argparse \
        .ArgumentParser(description='''Save into columnar format (parquet) the input file''')

    parser.add_argument(
        '-in',
        metavar='path',
        type=str,
        required=True,
        help='''path to parquet files'''
    )

    parser.add_argument(
        '-ratio',
        metavar='ratio',
        type=str,
        required=True,
        help='''ratio of the file to load and to export into columnar format'''
    )

    parser.add_argument(
        '-out',
        metavar='output_path',
        type=str,
        required=True,
        help='''output path of parquets filtered'''
    )

    args = vars(parser.parse_args())
    n_ratio = args['ratio']
    # '/Users/francescoterenzi/ADA/Project/temp/pietro/first.xml'

    spark = SparkSession.builder.getOrCreate()
    sc = spark.sparkContext
    sqlContext = SQLContext(sc)

    print('start loading data')
    some_data = sqlContext.read.format('com.databricks.spark.xml').options(rowTag='page') \
        .options(samplingRatio=n_ratio).load(args['in'])

    print('saving into parquet into {} folder'.format(args['out']))
    # saving binary file to future uses
    some_data.write.parquet(args['out'])


if __name__ == "__main__":
    main()

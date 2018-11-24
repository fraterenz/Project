import argparse
from pyspark.sql import SparkSession


def main():
    parser = argparse\
        .ArgumentParser(description='''Test if the parquet folders contains something meaningfull''')

    parser.add_argument(
        '-in',
        metavar='path',
        type=str,
        required=True,
        help='''path to parquet files'''
    )

    args = vars(parser.parse_args())

    spark = SparkSession.builder.getOrCreate()

    # loading the saved parquet files
    DATA_DIR = args['in']
    columnar_data = spark.read.parquet(DATA_DIR)
    print(type(columnar_data))
    print(columnar_data.show(5))
    print(columnar_data.count())


if __name__ == "__main__":
    main()

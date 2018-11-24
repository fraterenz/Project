from pyspark.sql import SparkSession


def main():
    spark = SparkSession.builder.getOrCreate()

    # loading the saved parquet files
    # DATA_DIR = "/Users/francescoterenzi/ADA/Project/temp/test_main_filtered.parquet"
    DATA_DIR = "/user/terenzi/filtered_conflicts.parquet"
    columnar_data = spark.read.parquet(DATA_DIR)
    print(type(columnar_data))
    print(columnar_data.show(5))


if __name__ == "__main__":
    main()

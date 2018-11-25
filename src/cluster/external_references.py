import argparse
import re
from operator import add
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.functions import countDistinct
from pyspark.sql.types import StringType, Row
from pyspark.sql import SQLContext


def main():
    parser = argparse\
        .ArgumentParser(description='''Count the external references''')

    parser.add_argument(
        '-in_filtered',
        metavar='path_filtered',
        type=str,
        required=True,
        help='''path to filtered parquet files'''
    )

    parser.add_argument(
        '-in_raw',
        metavar='path_raw',
        type=str,
        required=True,
        help='''path to raw parquet files'''
    )

    parser.add_argument(
        '-out',
        metavar='path_raw',
        type=str,
        required=True,
        help='''path to save parquet files'''
    )

    args = vars(parser.parse_args())

    spark = SparkSession.builder.getOrCreate()
    sc = spark.sparkContext
    sqlContext = SQLContext(sc)

    # load filtered articles
    conflict_articles = args['in_filtered']
    # load raw data
    articles = args['in_raw']

    """
    # TODO try map and reduce
    external_links = []
    for i in articles.select("revision.text._VALUE").collect():
        external_links += link_regex.findall(i[0])"""

    # find all occurences and reduce to have a final dataframe with all the external references
    external_links = sqlContext.createDataFrame(articles.rdd.map(find_ext_links).reduce(add), StringType)

    group_links = external_links.groupBy("title").agg(countDistinct("title"))\
        .select("title", F.col("count(DISTINCT title)").alias("external_links"))

    all_info = conflict_articles.join(group_links, "title", how='left').na.fill(0)
    all_info = all_info.select("id", "title", "external_links")
    all_info.write.parquet(args['out'])


def find_ext_links(dataframe, regex=r"\[\[(.*?)\]\]"):
    regex_compiled = re.compile(regex, re.IGNORECASE)
    text = dataframe.revision.text._VALUE
    refs = regex_compiled.findall(text)
    return Row(id=dataframe.id, title=dataframe.title, link=refs)


if __name__ == "__main__":
    main()

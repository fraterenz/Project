import argparse
import re
from pyspark.sql import SparkSession
from pyspark.sql.types import Row
from pyspark.sql import SQLContext
from pyspark.sql.utils import AnalysisException


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

    # craete a spark session
    spark = SparkSession.builder.getOrCreate()
    sc = spark.sparkContext
    sqlContext = SQLContext(sc)

    # load filtered articles (parquet)
    conflict_articles = spark.read.parquet(args['in_filtered'])
    # load raw data (parquet)
    wikipedia = spark.read.parquet(args['in_raw'])

    # filter to select articles with text that are not redirections
    # take articles with text without any redirection
    try: # this does not work locally but on cluster?
        articles = wikipedia.filter("ns = '0'").filter("redirect._title is null") \
            .filter("revision.text._VALUE is not null") \
            .filter("length(revision.text._VALUE) > 0")
    except AnalysisException:
        print('Not removing redirections because field redirect._title  not present in dataframe')
        articles = wikipedia.filter("ns = '0'").filter("revision.text._VALUE is not null") \
            .filter("length(revision.text._VALUE) > 0")

    external_links = sqlContext.createDataFrame(articles.rdd.map(find_ext_links))
    all_info = conflict_articles.join(external_links, "id", how='inner')
    all_info = all_info.drop("title")
    all_info.write.parquet(args['out'])


def find_ext_links(entity, regex=r"\[\[(.*?)\]\]"):
    regex_compiled = re.compile(regex, re.IGNORECASE)
    text = entity.revision.text._VALUE
    refs = regex_compiled.findall(text)
    return Row(id=entity.id, title=entity.title, link_count=len(refs), link=refs)


if __name__ == "__main__":
    main()

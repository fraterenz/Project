import argparse
import re
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType, BooleanType
from pyspark.sql.utils import AnalysisException


def main():
    parser = argparse\
        .ArgumentParser(description='''Filter out parquet files selecting articles with 
        text without any redirection that have an infobox matching the categories input by the user.
        Articles without infobox wont be considered!''')

    parser.add_argument(
        '-in',
        metavar='path',
        type=str,
        required=False,
        default="/user/terenzi/wikipedia_1.0.parquet",
        help='''path to parquet files'''
    )

    parser.add_argument(
        '-cat',
        metavar='categories',
        type=list,
        required=False,
        default=['civil conflicts', 'military conflicts', 'civilian attack'],
        help='''List of categories, string'''
    )

    parser.add_argument(
        '-out',
        metavar='output_path',
        type=str,
        required=True,
        help='''output path of parquets filtered'''
    )

    args = vars(parser.parse_args())

    if all([isinstance(ele, str) for ele in args['cat']]):
        good_categories = args['cat']  # civilian attack?
    else:
        raise ValueError('categories must be a list of string')

    PARQUET_DIR = args['in']

    # create spark context
    spark = SparkSession.builder.getOrCreate()

    # load data
    wikipedia = spark.read.parquet(PARQUET_DIR)

    # filter the data
    conflict_articles = filter_data(wikipedia, good_categories)

    # saving binary file to future uses
    conflict_articles.write.parquet(os.path.join(args['out'], 'filtered_conflicts.parquet'))


def filter_data(data, categories_to_match):
    """ Filter data stored in columnar format (.parquet) returning spark.DataFrame with only the articles with text
    and without any redirection that have an infobox with a category that matches on of the CATEGORIES_TO_MATCH.

    :param data: dat to filter, a pyspark.DataFrame
    :param categories_to_match: a list of categories that will match the articles
    :return: filtered pyspark.DataFrame according to the description.
    """

    # take articles with text without any redirection
    try:
        articles = data.filter("ns = '0'").filter("redirect._title is null")\
            .filter("revision.text._VALUE is not null")\
            .filter("length(revision.text._VALUE) > 0")  # TODO this does not work locally but on cluster?
    except AnalysisException:
        print('Not removing redirections because field redirect._title  not present in dataframe')
        articles = data.filter("ns = '0'").filter("revision.text._VALUE is not null")\
            .filter("length(revision.text._VALUE) > 0")

    # drop column redirect
    articles = articles.drop('redirect')

    # extract articles that have some defined categories in the infobox
    # regex that matches infobox
    regex = r"(?<={{infobox ).[a-zA-Z0-9.-_/ ]*" # o con \\n nel caso andasse a capo XD
    ibox_regex = re.compile(regex, re.IGNORECASE)

    # user defined func to extract the category from the infobox
    category_udf = udf(lambda text: extract_category(text, re_expression=ibox_regex), StringType())

    # create a column with the category for each article
    articles = articles.withColumn("categories", category_udf(articles.revision.text._VALUE))

    # regex that matches the categories
    regex = r"(" + '|'.join(categories_to_match) + ")(,|$)"  # military operation?
    category_selection_re = re.compile(regex, re.IGNORECASE)

    # user defined func to match the right categories
    good_category_udf = udf(lambda text: good_category(text, category_selection_re), BooleanType())
    conflict_articles = articles.withColumn("good_categories", good_category_udf(articles.categories)) \
        .filter('good_categories == true')

    return conflict_articles


def extract_category(text, re_expression):
    res = re_expression.findall(text)
    return ', '.join(res)


def good_category(text, re_expression):
    return re_expression.findall(text)


if __name__ == "__main__":
    main()

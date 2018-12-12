import pandas as pd
import re


def clean_date(the_data_pd):
    the_data_pd['end_date_clean'] = the_data_pd['end_date'].apply(find_pattern)
    return the_data_pd


def find_pattern(my_str: str) -> str:
    # if my_str == 'None', do nothing

    ongoing = re.compile(r"ongoing", re.IGNORECASE)
    digits = re.compile(r"\d{3,}")

    if re.search(ongoing, my_str):
        return "ongoing"
    if re.search(digits, my_str):
        # match the last year
        my_str_rev = my_str[::-1]
        # and reverse
        return re.search(digits, my_str_rev).group(0)[::-1]


def clean_location(df_articles):
    # explode dataframe as in spark for each location
    orignal_data_split = [
        (idx, foo) for (idx, ele) in
        zip(df_articles.location.index.values.tolist(), df_articles.location.str.split(','))
        if ele for foo in ele
    ]

    re_spaced_words = re.compile('\w+-*\s*', flags=re.IGNORECASE)
    cleaned = [(idx, ' '.join(re_spaced_words.findall(ele))) for (idx, ele) in orignal_data_split]

    # create a series with the idx of the original data with location splitted by comma
    location = pd.DataFrame([tup[1] for tup in cleaned],
                            index=[tup[0] for tup in cleaned],
                            columns=['locations'])
    location = location.groupby(location.index)['locations'].apply(lambda x: "%s" % '|'.join(x))
    return location

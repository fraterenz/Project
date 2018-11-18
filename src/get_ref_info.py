import re

from pyspark import Row


def get_ref_info(entity, full_ref_regex=re.compile(r'(<ref[^>]*[^/]>|<ref[ ]*>){{([^<]*)}}</ref')):
    """

    :param entity: RDD dataframe from data/**wiki-20181101-pages-articles-multistream loaded with XmlWiki.py class
    :param full_ref_regex: regex expression to extract a reference
    :return: Spark dataframe with id, template, url, title
    """
    text = entity.revision.text._VALUE
    # remove bot
    text = re.sub("(<!--.*?-->)", "", text, flags=re.MULTILINE)
    refs = full_ref_regex.findall(text)
    result = []
    for r in refs:
        ref_content = r[1].split(r"|")
        template = ref_content.pop(0).strip()
        properties = {}
        for field in ref_content:
            equal_index = field.find("=")
            field_name = field[0:equal_index].strip()
            field_value = field[equal_index + 1:].strip()
            properties[field_name] = field_value
        result.append(Row(id=entity.id,
                          template=template.lower(),
                          url=properties.get("url", ""),
                          title=properties.get("title")))
    return result

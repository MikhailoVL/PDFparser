import re
from setings import re_get_list_topic, re_get_title_topic, re_get_introduction, \
    re_last_element, column_title
from bs4 import BeautifulSoup
import pandas as pd


def get_clear_text(text: str) -> str:
    """
        discards unnecessary text
    :param text:
    :return: return text vis topic
    """
    text = text.strip()
    text = ' P001 ' + text.split('P001')[1].split('Abdallah, Florence 41')[0]
    text = text.replace('\n', ' ')
    text = text.replace(
        '5th World Psoriasis & Psoriatic Arthritis Conference 2018', ' ')

    text = text.replace("  ", " ")

    return text


def get_topics(clear_text) -> list:
    """
        separate articles
    :param clear_text: text
    :return: list contain articles
    """
    topics = re_get_list_topic.findall(clear_text)
    last = "  " + re_last_element.search(clear_text).group(0)
    topics.append(last)
    return topics


def get_session_name(articles: list) -> list:
    """
    get from articles - element Pxxx
    :param articles: list with topics
    :return: list (element - Pxxx)
    """
    return [str(topic)[2:6] for topic in articles]


def get_topics_tittle(articles: list) -> list:
    """

    :param articles: articles list
    :return: list ,element - tittle
    """
    return [re_get_title_topic.search(str(article)).group(0) for article in
            articles]


def get_topics_present(articles: list) -> list:
    """
    :param articles: list articles
    :return: list , element - description article
    """
    return [re_get_introduction.search(str(article)).group(0) for article in
            articles]


def get_affiliation_location(path_to_html: str, session_name) -> dict:
    """

    :param path_to_html:
    :param session_name: number of tittle
    :return: Pxxx : affiliation_location
    """
    soup = BeautifulSoup(open(path_to_html), 'html.parser')
    affiliation = {}
    for name in session_name:
        # print("My name = ", name)
        parent_tag = soup.select_one(f'span:-soup-contains({name})').parent
        children_tag = parent_tag.findChildren("span",
                                               style="font-family: TimesNewRomanPS-ItalicMT; font-size:8px")
        # print(children_tag)
        affiliation[name] = (get_affiliation_from_soup(children_tag))

    return affiliation


def get_affiliation_from_soup(soup_tags: set) -> str:
    """
        get from html affiliation
    :param soup_tags:
    :return:
    """
    affiliation = ''
    for tag in soup_tags:
        if len(tag.text.split()) >= 2 and len(tag.text) > 3:
            affiliation += (
                re.sub(r'^\s*(-\s*)?|(\s*-)?\s*$|[$-]', '',
                       tag.text)).replace(
                '\n',
                " ").replace(
                "  ", " ")
    # affiliation = ' '.join([str(elem) for elem in affiliation.split(",") if len(elem.split()) > 1])
    return affiliation


def get_name_author(articles: list, flag_end_str: dict,
                    flag_begin_str: list) -> dict:
    """
        get value between two flags
    :param flag_begin_str:
    :param articles:
    :param flag_end_str:
    :return: dict with list name autor - Pxxx : [Hailun Wang1, Michael Ni1, Japio Fung1, Kang Yan1, Xiaoxin Yao1]
    """
    number_with_names = {}
    for article in articles:
        index = articles.index(article)
        key = str(article)[2:6]
        end = flag_end_str[key].strip().split(",")[0]
        begin = flag_begin_str[index].split()[-1].replace('\\xad', '-').replace(
            ")", "").replace("(", "").replace("?", "")
        try:
            names = re.search(rf'(?<={begin})(.*?)(?={end})', str(article))
            if names:
                names = names.group(0).strip()
                number_with_names[key] = names.split(",")
            else:
                number_with_names[key] = ['']
                # print(number_with_names[key])
            # print(index, " ", key, " ",names)
        except Exception as e:
            print(e)

    return number_with_names


def save_to_excel(
        topics_numbers: list,
        affiliation_location: dict,
        topic_tittle: list,
        presentation: list,
        names_author: dict):
    """
            created excel and set data
    :param topics_numbers:
    :param affiliation_location:
    :param topic_tittle:
    :param presentation:
    :param names_author:
    :return: None
    """
    writer = pd.ExcelWriter("excel-comp-data.xlsx", engine='xlsxwriter')

    data = pd.DataFrame(column_title, index=[1])
    data.to_excel(writer, sheet_name='Sheet1')
    k = 0
    for number in topics_numbers:
        item_number = topics_numbers.index(number)
        for name in names_author[number]:
            index = item_number + 1 + k
            data.at[index, ['Affiliation(s) Name(s)']] = affiliation_location[
                number]
            data.at[index, ["Person's Location"]] = affiliation_location[number]
            data.at[index, ['Session Name']] = number
            data.at[index, ['Topic Title']] = topic_tittle[item_number]
            data.at[index, ['Presentation Abstract']] = presentation[
                item_number]
            data.at[index, ['Name (incl. titles if any mentioned)']] = name
            data.to_excel(writer, sheet_name='Sheet1')
            k += 1

    writer.save()

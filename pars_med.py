from pdfminer.high_level import extract_text, extract_text_to_fp
from pdfminer.layout import LAParams


from utils import get_clear_text, get_topics, get_session_name, \
    get_topics_tittle, get_topics_present, get_affiliation_location, \
    get_name_author, save_to_excel
from setings import path_PDF, column_title
from typing import Optional


def run_parser():
    pdf_parser: Optional[TopicParser] = TopicParser(path_PDF)
    text: str = pdf_parser.get_data_pdf_like_text()
    topics: list = get_topics(text)

    topics_numbers: list = get_session_name(topics)
    topic_tittle: list = get_topics_tittle(topics)
    presentation: list = get_topics_present(topics)

    html: str = pdf_parser.get_data_pdf_like_html()
    affiliation_location: dict = get_affiliation_location(html,
                                                          topics_numbers)
    names_author: dict = get_name_author(topics, affiliation_location,
                                         topic_tittle)

    save_to_excel(
        topics_numbers, affiliation_location,
        topic_tittle, presentation, names_author)


class TopicParser:

    def __init__(self, path):
        self.path = path
        self.topic_list = None

    def get_data_pdf_like_text(self) -> str:
        """
        :return: text from pdf
        """
        with open(self.path, 'rb') as fin:
            text = extract_text(fin)
        text = get_clear_text(text)
        return text

    def get_data_pdf_like_html(self) -> str:
        """
        create from pdf html
        :return: name file vis html
        """
        file_html = "html_for_soup.txt"
        with open(file_html, 'w') as hf:
            with open(self.path, 'rb') as fn:
                extract_text_to_fp(
                    fn, hf, laparams=LAParams(), output_type='html', codec=None)

        return file_html


#  get and prepare text to parsing
# pdf_parser: Optional[TopicParser] = TopicParser(path_PDF)
# text: str = pdf_parser.get_data_pdf_like_text()
# topics: list = get_topics(text)
#
# topics_numbers: list = get_session_name(topics)
# topic_tittle: list = get_topics_tittle(topics)
# presentation: list = get_topics_present(topics)
#
# html: str = pdf_parser.get_data_pdf_like_html()
# affiliation_location: dict = get_affiliation_location(html, topics_numbers)
# names_author: dict = get_name_author(topics, affiliation_location, topic_tittle)
#
# writer = pd.ExcelWriter("excel-comp-data.xlsx", engine='xlsxwriter')
#
# data = pd.DataFrame(column_title, index=[1])
# data.to_excel(writer, sheet_name='Sheet1')
# k = 0
# for number in topics_numbers:
#     item_number = topics_numbers.index(number)
#     for name in names_author[number]:
#         index = item_number + 1 + k
#         data.at[index, ['Affiliation(s) Name(s)']] = affiliation_location[number]
#         data.at[index, ["Person's Location"]] = affiliation_location[number]
#         data.at[index, ['Session Name']] = number
#         data.at[index, ['Topic Title']] = topic_tittle[item_number]
#         data.at[index, ['Presentation Abstract']] = presentation[item_number]
#         data.at[index, ['Name (incl. titles if any mentioned)']] = name
#         data.to_excel(writer, sheet_name='Sheet1')
#         k += 1
#
# writer.save()

if __name__ == "__main__":
    run_parser()

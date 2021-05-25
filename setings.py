import re

re_get_list_topic = re.compile('(P\d{3}\s(.*?))(?=\sP\d{3})')

# title of topic - example - "SPLENOMEGALY AND PSORIASIS - A CASE REPORT"
re_get_title_topic = re.compile('(?<=P\d{3}\s)(.*?)(?=[A-Z][a-z])')

re_last_element = re.compile(r'(P155.*)')

re_get_introduction = re.compile('((Introduction.|Introduction: The treatment|Introduction:|Background:|Objective:|Objectives:|Introduction & Objectives:|Apremilast was approved|Background\/Objective:|Introduction and Objectives:|We report a case of severe|Sarajevo Many|Croatia Psoriasis|TNF therapy has|France Psoriasis).*)')

path_PDF = 'Abstract Book from the 5th World Psoriasis and' \
           ' Psoriatic Arthritis Conference 2018.pdf'


column_title = ({'Name (incl. titles if any mentioned)': None,
                'Affiliation(s) Name(s)': None,
                "Person's Location": None,
                'Session Name': None,
                'Topic Title': None,
                'Presentation Abstract': None})
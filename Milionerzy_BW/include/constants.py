from collections import namedtuple

QUESTION_VALUES = {
    0: '500',
    1: '1000',
    2: '2000',
    3: '5000',
    4: '10 000',
    5: '20 000',
    6: '40 000',
    7: '75 000',
    8: '125 000',
    9: '250 000',
    10: '500 000',
    11: '1 000 000'
}

Language = namedtuple('Language', ['polish', 'english', 'german'])
LANGUAGES = Language(
    polish='pl',
    english='en',
    german='de'
)

currency_dict = {LANGUAGES.german: 'EUR', LANGUAGES.english: 'GBP'}

database_path = 'postgresql://postgres@localhost/millionaires'

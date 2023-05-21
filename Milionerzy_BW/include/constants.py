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

Errors = namedtuple('Errors', ['no_questions_offline', 'app_not_translated', 'no_questions'])

ERRORS = Errors(
    no_questions_offline={
        LANGUAGES.polish: "Nie mozna grac offline. Za malo pytan po polsku. Jesli chcesz grac, musisz przejsc do trybu online lub zmienic jezyk.",
        LANGUAGES.english: "Cannot play offline. Not enough questions in english. If you want to play you must get online or switch language.",
        LANGUAGES.german: "Kann nicht offline spielen. Nicht genug Fragen auf Deutsch. Wenn Sie spielen wollen, mussen Sie online gehen oder die Sprache wechseln."
    },
    app_not_translated={
        LANGUAGES.polish: "Nie mozna grac offline. Aplikacja nie zostala przetlumaczona na jezyk polski. Jesli chcesz grac, musisz przejsc do trybu online lub zmienic jezyk.",
        LANGUAGES.english: "Cannot play offline. Application not translated to english. If you want to play you must get online or switch language.",
        LANGUAGES.german: "Kann nicht offline spielen. Anwendung nicht ins Deutsche ubersetzt. Wenn Sie spielen wollen, mussen Sie online gehen oder die Sprache wechseln."
    },
    no_questions={
        LANGUAGES.polish: "Nie mozna zagrac w gre. Za malo pytan w bazie danych.",
        LANGUAGES.english: "Cannot play the game. Not enough questions in database.",
        LANGUAGES.german: "Ich kann das Spiel nicht spielen. Nicht genug Fragen in der Datenbank."
    }
)

Info = namedtuple('Info', ['application', 'questions'])
INFO = Info(
    application={
        LANGUAGES.polish: 'Przygotowywanie rozgrywki...',
        LANGUAGES.english: 'Preparing the game...',
        LANGUAGES.german: 'Das Spiel vorbereiten...'
    },
    questions={
        LANGUAGES.polish: 'Trwa tlumaczenie pytan...',
        LANGUAGES.english: 'Questions are being translated...',
        LANGUAGES.german: 'Die Fragen werden ubersetzt...'
    }
)

database_path = 'postgresql://postgres@localhost/millionaires'

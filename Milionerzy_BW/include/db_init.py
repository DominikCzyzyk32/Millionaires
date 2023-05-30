from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy import MetaData, Table, insert
from include.constants import database_path
from include.WWTBAM_import import WWTBAM_import
from include.bahadiri_import import bahadiri_import

Base = declarative_base()


# Tables structure
class AppContent(Base):
    __tablename__ = 'AppContent'
    id = Column(Integer, primary_key=True)
    tag = Column(String(50), nullable=False)
    language_id = Column(Integer, ForeignKey('Languages.id'))
    text = Column(String(2000))

    def __repr__(self):
        return "<AppContent(id={0}, tag={1}, language_id={2}, text={3})>".format(
            self.id, self.tag, self.language_id, self.text)


class Languages(Base):
    __tablename__ = 'Languages'
    __table_args__ = (
        CheckConstraint('LENGTH(name) = 2'),
        UniqueConstraint('name'),
    )
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    def __repr__(self):
        return "<Languages(id={0}, name={1})>".format(
            self.id, self.name)


class Questions(Base):
    __tablename__ = 'Questions'
    id = Column(Integer, primary_key=True)
    language_id = Column(Integer, ForeignKey("Languages.id"))
    question = Column(String(500))
    correct_answer = Column(String(50))
    wrong_answer_1 = Column(String(50))
    wrong_answer_2 = Column(String(50))
    wrong_answer_3 = Column(String(50))
    used = Column(Boolean, unique=False, default=False)

    def __repr__(self):
        return "<Questions(id={0}, language_id={1}, question={2}, correct_answer={3}, wrong_answer_1={4}, wrong_answer_2={5}, wrong_answer_3={6}, used={7})>".format(
            self.id, self.language_id, self.question, self.correct_answer, self.wrong_answer_1, self.wrong_answer_2, self.wrong_answer_3, self.used)
    
       
       
def db_init():
    # connect to database
    engine = create_engine(database_path)

    # create database if not exists
    if not database_exists(engine.url):
        create_database(engine.url)
        Base.metadata.create_all(engine)
    db = engine.connect()

    # create tables using ORM techniques
    metadata = MetaData()
    languages = Table('Languages', metadata, autoload_with=db)
    app_content = Table('AppContent', metadata, autoload_with=db)

    # insert original language
    language_id = 1
    languages_query = insert(languages).values(name='pl')

    # insert original text content
    app_content_query = insert(app_content).values(
    [
        {'tag': 'rules', 'text': 
        'Zasady: \n'
        'Twoim zadaniem jest odpowiedzieć poprawnie kolejno na dwanaście zamkniętych pytań z odpowiedziami A, B, C, D.\n'
        'Wartość każdego pytania będzie się wyświetlała w prawym dolnym rogu aplikacji.\n'
        'Po otrymaniu pytania jest możliwość zrezygnowania z gry i zabrania dotychczsowo wygranych pieniędzy.\n'
        'Istnieją dwa progi gwarantowane:\n'
        '* 1 000 zł - po odpowiedzeniu na dwa pytania\n'
        '* 40 000 zł po odpowiedzeniu na siedem pytań\n'
        'W przypadku błędnej odpowiedzi, gracz otrzymuje tyle, ile wynosi najwyższy próg gwarantowany jaki osiągnął (jeśli udzielono błędnej odpowiedzi na pierwsze lub drugie pytanie gracz nic nie wygrywa).\n'
        'Gracz ma do dyspozycji 3 koła ratunkowe (każde z nich może użyć tylko raz w trakcie gry):\n'
        '* 50 / 50 - odrzuca dwie błędne odpowiedzi\n'
        '* telefon do przyjaciela - gracz otrzymuje informację o tym, która odpowiedź (zdaniem wirtualnego przyjaciela) jest poprawna\n'
        '* pytanie do publiczności - gracz otrzymuje wykres słupkowy przedstawiający wynik głosowania publiczności w studiu\n\n'
        'Życzymy miłej gry i dużej wygranej :)...', 
        'language_id': language_id},
        {'tag': 'button_text', 'text': 'Rozpocznij grę', 'language_id': language_id},
        {'tag': 'group_box_name', 'text': 'Zasady', 'language_id': language_id},
        {'tag': 'MainWindowTitle', 'text': 'Milionerzy', 'language_id': language_id},
        {'tag': 'fifty_fifty_button_text', 'text': '50 / 50', 'language_id': language_id},
        {'tag': 'call_friend_button_text', 'text': 'Telefon do przyjaciela', 'language_id': language_id},
        {'tag': 'ask_audience_button_text', 'text': 'Pytanie do publiczności', 'language_id': language_id},
        {'tag': 'start_game_button_text', 'text': 'Rozpocznij grę', 'language_id': language_id},
        {'tag': 'MillionairesGroupBoxTitle', 'text': 'Pytanie', 'language_id': language_id},
        {'tag': 'TakingDecisionGroupBoxTitle', 'text': 'Czy chcesz grać dalej?', 'language_id': language_id},
        {'tag': 'LifebuoysGroupBoxTitle', 'text': 'Koła ratunkowe', 'language_id': language_id},
        {'tag': 'ValueOfQuestionGroupBoxTitle', 'text': 'Wartość pytania', 'language_id': language_id},
        {'tag': 'FinalResultGroupBoxTitle', 'text': 'Wynik gry', 'language_id': language_id},
        {'tag': 'correct_answer', 'text': 'Brawo, to jest poprawna odpowiedź! :)', 'language_id': language_id},
        {'tag': 'wrong_answer', 'text': 'Niestety, jest to zła odpowiedź! :(\nPoprawną odpowiedzią była odpowiedź', 'language_id': language_id},
        {'tag': 'no_answer', 'text': 'Poprawną odpowiedzią była odpowiedź', 'language_id': language_id},
        {'tag': 'victory', 'text': 'Wygrałeś/łaś', 'language_id': language_id},
        {'tag': 'no_victory', 'text': 'Niestety nic dziś nie wygrałeś/łaś :(', 'language_id': language_id},
        {'tag': 'new_game_proposition', 'text': "\nJeśli chcesz zagrać jeszcze raz kliknij przycisk 'Rozpocznij grę'", 'language_id': language_id},
        {'tag': 'million', 'text': 'Milion !!!', 'language_id': language_id},
        {'tag': 'textbox_value_of_question', 'text': 'Pytanie za', 'language_id': language_id},
        {'tag': 'lifebuoy_used', 'text': 'To koło ratunkowe zostało już użyte', 'language_id': language_id},
        {'tag': 'call_friend_result', 'text': 'Wydaje mi się, że jest to odpowiedź', 'language_id': language_id},
        {'tag': 'resign_button_text', 'text': 'Rezygnuję', 'language_id': language_id},
        {'tag': 'currency', 'text': 'PLN', 'language_id': language_id},
        {'tag': 'AskAudienceWindowTitle', 'text': 'Wyniki głosowania', 'language_id': language_id}
    ])

    # execute queries
    db.execute(languages_query)
    db.execute(app_content_query)
    db.commit()

    WWTBAM_import()
    bahadiri_import()

# WWTBAM JSON File
# https://pastebin.com/QRGzxxEy
from sqlalchemy import create_engine
from sqlalchemy import select, insert
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, CheckConstraint, UniqueConstraint
import pandas as pd
import os
import csv
from include.constants import database_path
# from include.db_init import Languages, Questions
Base = declarative_base()


class Languages(Base):
    __tablename__ = 'Languages'
    __table_args__ = (
        CheckConstraint('LENGTH(name) = 2'),
        UniqueConstraint('name'),
    )
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable = False)

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


def bahadiri_import():
    engine = create_engine(database_path)
    db = engine.connect()

    lang_exists = db.execute(select(Languages).where(Languages.name == 'tr')).fetchall()
    if not lang_exists:
        lang_query = insert(Languages).values(name='tr')
        db.execute(lang_query)
    language_id = db.execute(select(Languages.id).where(Languages.name == 'tr')).fetchall()[0][0]

    file = pd.read_csv("bahidiri_turkish.csv", names=["id", "category_id", "question", "date", "A", "B", "C", "D", "answer", "subcategory_id"])
    quests = []

    for _, question in file.iterrows():
        quest = question["question"]
        answers = [question["A"], question["B"], question["C"], question["D"]]
        correct_answer = question[question["answer"]]
        answers.remove(correct_answer)
        wrong_answer_1 = answers[0]
        wrong_answer_2 = answers[1]
        wrong_answer_3 = answers[2]

        quests.append({'question': quest,
                       'language_id': language_id,
                       'correct_answer': correct_answer,
                       'wrong_answer_1': wrong_answer_1,
                       'wrong_answer_2': wrong_answer_2,
                       'wrong_answer_3': wrong_answer_3})

    quest_query = insert(Questions).values(quests)
    db.execute(quest_query)
    db.commit()

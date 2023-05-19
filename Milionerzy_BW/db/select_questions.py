from sqlalchemy import create_engine
from sqlalchemy import select, insert, and_
from sqlalchemy.orm import declarative_base
from sqlalchemy import select, insert, and_
import urllib.request
from db_init import Languages, Questions
from translate_questions import translate_questions
from include.constants import database_path


def select_questions(lang):
    engine = create_engine(database_path)
    db = engine.connect()

    questions = parse_db_select_response(
        db.execute(
            select(Questions).join(Languages, Questions.language_id == Languages.id).where(and_(Languages.name == lang, Questions.used == False)).limit(12))
        .fetchall())
    num_of_questions = len(questions)
    if num_of_questions < 12:
        num_of_neccesary_questions = 12 - num_of_questions
        if is_internet_connection(): 
            questions_to_translate = db.execute(select(Questions).join(Languages, Questions.language_id == Languages.id).where(Questions.used == False).limit(num_of_neccesary_questions)).fetchall()
            translated_questions = translate_questions(questions_to_translate, lang)
            questions += translated_questions
            if len(questions) < 12:
                num_of_neccesary_questions = 12 - len(questions)
                seen_questions = parse_db_select_response(
                db.execute(
                    select(Questions).join(Languages, Questions.language_id == Languages.id).where(and_(Languages.name == lang, Questions.used == True)).limit(num_of_neccesary_questions))
                .fetchall())
                questions += seen_questions
            if len(questions) < 12:
                raise ValueError(f"Cannot play the game!!! Not enough questions in database.")
        else:
            seen_questions = parse_db_select_response(
                db.execute(
                    select(Questions).join(Languages, Questions.language_id == Languages.id).where(and_(Languages.name == lang, Questions.used == True)).limit(num_of_neccesary_questions))
                .fetchall())
            questions += seen_questions
            if len(questions) < 12:
                raise ValueError(f"Cannot play offline!!! Not enough questions in {lang} language. Consider changing the language of the game.")
    
    return questions


def parse_db_select_response(response):
    parsed_response = []
    for question in response:
        parsed_response.append({'id': question[0], 'language_id': question[1], 'question': question[2],
                                'correct_answer': question[3], 'wrong_answer_1': question[4], 
                                'wrong_answer_2': question[5], 'wrong_answer_3': question[6]})
    return parsed_response


def is_internet_connection(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False
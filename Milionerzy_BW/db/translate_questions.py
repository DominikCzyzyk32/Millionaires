import translators as ts
from sqlalchemy import create_engine
from sqlalchemy import select, insert, and_
from sqlalchemy.orm import declarative_base
from time import sleep
from db_init import Languages, Questions


def translate_questions(questions, lang):
    engine = create_engine("postgresql://postgres@localhost/millionaires_v3")
    db = engine.connect()

    lang_exists = db.execute(select(Languages).where(Languages.name == lang)).fetchall()
    if not lang_exists:
        lang_query = insert(Languages).values(name=lang)
        db.execute(lang_query)
        db.commit()
    language_id = db.execute(select(Languages.id).where(Languages.name == lang)).fetchall()[0][0]

    question_ids = tuple([question[0] for question in questions])
    existed_translations = db.execute(select(Questions).where(and_(Questions.question_id.in_(question_ids), Questions.language_id == language_id))).fetchall()
    
    translated_questions = []
    for question in questions:
        if question[0] in [translation[0] for translation in existed_translations]:
            quest = existed_translations[2]
            correct_answer = existed_translations[3]
            wrong_answer_1 = existed_translations[4]
            wrong_answer_2 = existed_translations[5]
            wrong_answer_3 = existed_translations[6]
            translated_questions.append({'language_id': language_id, 'question':quest, 'correct_answer':correct_answer, 
                                         'wrong_answer_1':wrong_answer_1, 'wrong_answer_2':wrong_answer_2, 'wrong_answer_3':wrong_answer_3})
        else:
            quest = question[2]
            correct_answer = question[3]
            wrong_answer_1 = question[4]
            wrong_answer_2 = question[5]
            wrong_answer_3 = question[6]
            original_language_name = db.execute(select(Languages.name).where(Languages.id == question['original_language_id'])).fetchall()[0][0]
            try:
                translated_question = ts.translate_text(quest, translator='google', from_langugage=original_language_name, to_language=lang)
                translated_correct_answer = ts.translate_text(correct_answer, translator='google', from_langugage=original_language_name, to_language=lang)
                translated_wrong_answer_1 = ts.translate_text(wrong_answer_1, translator='google', from_langugage=original_language_name, to_language=lang)
                translated_wrong_answer_2 = ts.translate_text(wrong_answer_2, translator='google', from_langugage=original_language_name, to_language=lang)
                translated_wrong_answer_3 = ts.translate_text(wrong_answer_3, translator='google', from_langugage=original_language_name, to_language=lang)
            except:
                sleep(2)
                translated_question = ts.translate_text(quest, translator='google', from_langugage=original_language_name, to_language=lang)
                translated_correct_answer = ts.translate_text(correct_answer, translator='google', from_langugage=original_language_name, to_language=lang)
                translated_wrong_answer_1 = ts.translate_text(wrong_answer_1, translator='google', from_langugage=original_language_name, to_language=lang)
                translated_wrong_answer_2 = ts.translate_text(wrong_answer_2, translator='google', from_langugage=original_language_name, to_language=lang)
                translated_wrong_answer_3 = ts.translate_text(wrong_answer_3, translator='google', from_langugage=original_language_name, to_language=lang)
            translated_questions.append({'language_id': language_id, 'question':translated_question, 
                                         'correct_answer': translated_correct_answer, 'wrong_answer_1': translated_wrong_answer_1,
                                         'wrong_answer_2': translated_wrong_answer_2, 'wrong_answer_3': translated_wrong_answer_3})
    
    translated_questions_query = insert(Questions).values(translated_questions)
    db.execute(translated_questions_query)
    db.commit()

    return translated_questions

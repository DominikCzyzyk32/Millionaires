import translators as ts
from sqlalchemy import create_engine
from sqlalchemy import select, insert
from sqlalchemy.orm import declarative_base
from time import sleep
from db_init import Languages, Questions, QuestionTranslations

# questions = [{'id':2, 'original_language_id':8, 'question':'example', 'correct_answer':'example', 'wrong_answer_1':'example', 'wrong_answer_2':'example', 'wrong_answer_3':'example'}] 
def translate_questions(questions, lang):
    engine = create_engine("postgresql://postgres@localhost/millionaires")
    db = engine.connect()

    lang_exists = db.execute(select(Languages).where(Languages.name == lang)).fetchall()
    if not lang_exists:
        lang_query = insert(Languages).values(name=lang)
        db.execute(lang_query)
        db.commit()
    language_id = db.execute(select(Languages.id).where(Languages.name == lang)).fetchall()[0][0]

    question_ids = tuple([question['id'] for question in questions])
    existed_translations = db.execute(select(QuestionTranslations).where(QuestionTranslations.question_id.in_(question_ids))).fetchall()
    existed_translations_question_ids_to_question_map = dict([{existed_translation[1]:{'question': existed_translation[3], 
                                                                                       'correct_answer': existed_translation[4],
                                                                                       'wrong_answer_1': existed_translation[5],
                                                                                       'wrong_answer_2': existed_translation[6],
                                                                                       'wrong_answer_3': existed_translation[7]}} for existed_translation in existed_translations])
    
    translated_questions = []
    for question in questions:
        if question['id'] in existed_translations_question_ids_to_question_map.keys():
            quest = existed_translations_question_ids_to_question_map[question['id']]['question']
            correct_answer = existed_translations_question_ids_to_question_map[question['id']]['correct_answer']
            wrong_answer_1 = existed_translations_question_ids_to_question_map[question['id']]['wrong_answer_1']
            wrong_answer_2 = existed_translations_question_ids_to_question_map[question['id']]['wrong_answer_2']
            wrong_answer_3 = existed_translations_question_ids_to_question_map[question['id']]['wrong_answer_3']
            translated_questions.append({'question_id': question['id'], 'language_id': language_id, 
                                         'question':quest, 'correct_answer':correct_answer, 'wrong_answer_1':wrong_answer_1, 
                                         'wrong_answer_2':wrong_answer_2, 'wrong_answer_3':wrong_answer_3})
        else:
            quest = question['question']
            correct_answer = question['correct_answer']
            wrong_answer_1 = question['wrong_answer_1']
            wrong_answer_2 = question['wrong_answer_2']
            wrong_answer_3 = question['wrong_answer_3']
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
            translated_questions.append({'question_id': question['id'], 'language_id': language_id,
                                         'question':translated_question, 'correct_answer':translated_correct_answer, 
                                         'wrong_answer_1':translated_wrong_answer_1, 'wrong_answer_2':translated_wrong_answer_2, 
                                         'wrong_answer_3':translated_wrong_answer_3})
    
    translated_questions_query = insert(QuestionTranslations).values(translated_questions)
    db.execute(translated_questions_query)
    db.commit()

    return translated_questions
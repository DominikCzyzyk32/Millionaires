import urllib.request
from sqlalchemy import create_engine
from sqlalchemy import select, insert, and_
from include.db_init import Languages, AppContent, Questions
from include.constants import database_path, LANGUAGES, currency_dict, ERRORS
from deep_translator import GoogleTranslator


def translate_app(lang):
    engine = create_engine(database_path)
    db = engine.connect()

    language_id = give_language_id(db, lang)

    translation_exists = db.execute(select(AppContent).where(AppContent.language_id == language_id)).fetchall()
    if not translation_exists:
        if not check_internet_connection():
            raise ValueError(ERRORS.app_not_translated[lang])

        deep_translator = GoogleTranslator(source=LANGUAGES.polish, target=lang)

        original_app_content = db.execute(select(AppContent).where(AppContent.language_id == 1)).fetchall()
        translated_app_content = []

        for app_text in original_app_content:
            tag = app_text[1]
            if tag == 'currency':
                translated_text = currency_dict[lang]
            else:
                text = app_text[3]
                translated_text = make_translation(deep_translator, text)
                if text[0].isupper() and not translated_text[0].isupper():
                    translated_text = translated_text[0].upper() + translated_text[1:]

            if 'PLN' in translated_text and lang != LANGUAGES.polish:
                translated_text = translated_text.replace('PLN', currency_dict[lang])

            translated_app_content.append({'tag': tag, 'text': translated_text, 'language_id': language_id})

        translated_app_content_query = insert(AppContent).values(translated_app_content)
        db.execute(translated_app_content_query)
        db.commit()


def translate_questions(questions, lang):
    engine = create_engine(database_path)
    db = engine.connect()

    language_id = give_language_id(db=db, lang=lang)

    question_ids = tuple([question[0] for question in questions])
    existed_translations = db.execute(select(Questions).where(
        and_(Questions.id.in_(question_ids), Questions.language_id == language_id))).fetchall()

    translated_questions = []
    for question in questions:
        if question[0] in [translation[0] for translation in existed_translations]:
            quest = existed_translations[2]
            correct = existed_translations[3]
            wrong_1 = existed_translations[4]
            wrong_2 = existed_translations[5]
            wrong_3 = existed_translations[6]
        else:
            original_language_name = db.execute(select(Languages.name).where(
                Languages.id == question[1])).fetchall()[0][0]
            deep_translator = GoogleTranslator(source=original_language_name, target=lang)

            quest = make_translation(deep_translator, question[2])
            correct = make_translation(deep_translator, question[3])
            wrong_1 = make_translation(deep_translator, question[4])
            wrong_2 = make_translation(deep_translator, question[5])
            wrong_3 = make_translation(deep_translator, question[6])

        translated_questions.append({'language_id': language_id, 'question': quest, 'correct_answer': correct,
                                     'wrong_answer_1': wrong_1, 'wrong_answer_2': wrong_2, 'wrong_answer_3': wrong_3})

    translated_questions_query = insert(Questions).values(translated_questions)
    db.execute(translated_questions_query)
    db.commit()

    return translated_questions


def give_language_id(db, lang):
    lang_exists = db.execute(select(Languages).where(Languages.name == lang)).fetchall()
    if not lang_exists:
        lang_query = insert(Languages).values(name=lang)
        db.execute(lang_query)
        db.commit()
    return db.execute(select(Languages.id).where(Languages.name == lang)).fetchall()[0][0]


def check_internet_connection(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False


def make_translation(translator, text):
    try:
        return translator.translate(text)
    except:
        return make_translation(translator, text)

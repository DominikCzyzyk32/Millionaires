from sqlalchemy import create_engine
from sqlalchemy import select, insert
from sqlalchemy.orm import declarative_base
from include.db_init import Languages, AppContent
from include.constants import database_path, LANGUAGES, currency_dict
from deep_translator import GoogleTranslator


def translate_app(lang):
    engine = create_engine(database_path)
    db = engine.connect()

    lang_exists = db.execute(select(Languages).where(Languages.name == lang)).fetchall()
    if not lang_exists:
        lang_query = insert(Languages).values(name=lang)
        db.execute(lang_query)
        db.commit()
    language_id = db.execute(select(Languages.id).where(Languages.name == lang)).fetchall()[0][0]

    translation_exists = db.execute(select(AppContent).where(AppContent.language_id == language_id)).fetchall()
    if not translation_exists:
        deep_translator = GoogleTranslator(source=LANGUAGES.polish, target=lang)

        original_app_content = db.execute(select(AppContent).where(AppContent.language_id == 1)).fetchall()
        translated_app_content = []

        for app_text in original_app_content:
            tag = app_text[1]
            if tag == 'currency':
                translated_text = currency_dict[lang]
            else:
                text = app_text[3]
                translated_text = deep_translator.translate(text)

            if 'PLN' in translated_text and lang != LANGUAGES.polish:
                translated_text = translated_text.replace('PLN', currency_dict[lang])
            translated_app_content.append({'tag': tag, 'text': translated_text, 'language_id': language_id})
        
        translated_app_content_query = insert(AppContent).values(translated_app_content)
        db.execute(translated_app_content_query)
        db.commit()

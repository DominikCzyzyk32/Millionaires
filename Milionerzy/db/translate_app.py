import translators as ts
from sqlalchemy import create_engine
from sqlalchemy import select, insert
from sqlalchemy.orm import declarative_base
from time import sleep
from db_init import Languages, AppContent


def translate_app(lang):
    engine = create_engine("postgresql://postgres@localhost/millionaires")
    db = engine.connect()

    lang_exists = db.execute(select(Languages).where(Languages.name == lang)).fetchall()
    if not lang_exists:
        lang_query = insert(Languages).values(name=lang)
        db.execute(lang_query)
        db.commit()
    language_id = db.execute(select(Languages.id).where(Languages.name == lang)).fetchall()[0][0]

    translation_exists = db.execute(select(AppContent).where(AppContent.language_id == language_id)).fetchall()
    if not translation_exists:
        original_app_content = db.execute(select(AppContent).where(AppContent.language_id == 1)).fetchall()
        translated_app_content = []

        for app_text in original_app_content:
            tag = app_text[1]
            text = app_text[3]
            try:
                translated_text = ts.translate_text(text, translator='google', from_langugage='pl', to_language=lang)
            except:
                sleep(2)
                translated_text = ts.translate_text(text, translator='google', from_langugage='pl', to_language=lang)
            translated_app_content.append({'tag': tag, 'text': translated_text, 'language_id': language_id})
        
        translated_app_content_query = insert(AppContent).values(translated_app_content)
        db.execute(translated_app_content_query)
        db.commit()
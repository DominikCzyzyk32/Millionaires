import urllib.request
from sqlalchemy import create_engine
from sqlalchemy import select, update, and_
from sqlalchemy.sql.expression import func
from include.db_init import Languages, Questions, AppContent
from include.constants import database_path, ERRORS
from include.translate import translate_app, translate_questions


def parse_app_content(response):
    application_text = {
        'RulesWindow': {
            'rules': '',  # '<zasady gry>'
            'button_text': '',  # 'Rozpocznij grę'
            'group_box_name': ''  # 'Zasady'
        },
        'MillionairesWindow': {
            'MainWindowTitle': '',  #
            'fifty_fifty_button_text': '',
            'call_friend_button_text': '',  #
            'ask_audience_button_text': '',  # ''
            'start_game_button_text': '',  # ''
            'resign_button_text': '',  # ''
            'MillionairesGroupBoxTitle': '',  # ''
            'TakingDecisionGroupBoxTitle': '',  # ''
            'LifebuoysGroupBoxTitle': '',  # ''
            'ValueOfQuestionGroupBoxTitle': '',  # ''
            'FinalResultGroupBoxTitle': '',  # ''
            'currency': '',  #
            'AskAudienceWindowTitle': '',
            'textbox_checking_correctness': {
                'correct_answer': '',  # ''
                'wrong_answer': '',  # ''
                'no_answer': ''  # ''
            },
            'textbox_final_result': {
                'victory': '',  # ''
                'no_victory': '',  # ''
                'new_game_proposition': '',  # ''
                'million': '',  #
            },
            'textbox_value_of_question': '',  # 'Pytanie za ',
            'textbox_lifebuoy': {
                'lifebuoy_used': '',  # 'To koło ratunkowe zostało już użyte.',
                'call_friend_result': ''  # 'Wydaje mi się, że jest to odpowiedź '
            }
        }
    }
    for app_con in response:
        if app_con[1] in ['rules', 'button_text', 'group_box_name']:
            application_text['RulesWindow'][app_con[1]] = app_con[3]
        elif app_con[1] in ['correct_answer', 'wrong_answer', 'no_answer']:
            application_text['MillionairesWindow']['textbox_checking_correctness'][app_con[1]] = app_con[3]
        elif app_con[1] in ['victory', 'no_victory', 'new_game_proposition', 'million']:
            application_text['MillionairesWindow']['textbox_final_result'][app_con[1]] = app_con[3]
        elif app_con[1] in ['lifebuoy_used', 'call_friend_result']:
            application_text['MillionairesWindow']['textbox_lifebuoy'][app_con[1]] = app_con[3]
        else:
            application_text['MillionairesWindow'][app_con[1]] = app_con[3]

    return application_text


def parse_question_content(response):
    parsed_response = []
    for question in response:
        parsed_response.append({'id': question[0], 'language_id': question[1], 'question': question[2],
                                'correct_answer': question[3], 'wrong_answer_1': question[4],
                                'wrong_answer_2': question[5], 'wrong_answer_3': question[6]})
    return parsed_response


def load_app_content(lang):
    translate_app(lang)
    engine = create_engine(database_path)
    db = engine.connect()

    app_content = parse_app_content(
        db.execute(select(AppContent).join(Languages, AppContent.language_id == Languages.id).where(
            Languages.name == lang)).fetchall()
    )

    return app_content


def load_questions(lang):
    engine = create_engine(database_path)
    db = engine.connect()

    questions = parse_question_content(
        db.execute(select(Questions).join(Languages, Questions.language_id == Languages.id).where(
                and_(Languages.name == lang, Questions.used == False)).order_by(func.random()).limit(12)).fetchall())
    num_of_questions = len(questions)
    if num_of_questions < 12:
        num_of_necessary_questions = 12 - num_of_questions
        if check_internet_connection():
            questions_to_translate = db.execute(
                select(Questions).join(Languages, Questions.language_id == Languages.id).where(
                    Questions.used == False).order_by(func.random()).limit(num_of_necessary_questions)).fetchall()
            translated_questions = translate_questions(questions_to_translate, lang)
            questions += translated_questions
            if len(questions) < 12:
                num_of_necessary_questions = 12 - len(questions)
                seen_questions = parse_question_content(
                    db.execute(
                        select(Questions).join(Languages, Questions.language_id == Languages.id).where(
                            and_(Languages.name == lang, Questions.used == True)).order_by(func.random()).limit(num_of_necessary_questions)).fetchall())
                questions += seen_questions
            if len(questions) < 12:
                raise ValueError(ERRORS.no_questions[lang])
        else:
            seen_questions = parse_question_content(
                db.execute(
                    select(Questions).join(Languages, Questions.language_id == Languages.id).where(
                        and_(Languages.name == lang, Questions.used == True)).order_by(func.random()).limit(num_of_necessary_questions)).fetchall())
            questions += seen_questions
            if len(questions) < 12:
                raise ValueError(ERRORS.no_questions_offline[lang])

    used_questions = [question['question'] for question in questions]
    db.execute(update(Questions).where(Questions.question.in_(used_questions)).values(used=True))
    db.commit()

    return questions


def check_internet_connection(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False

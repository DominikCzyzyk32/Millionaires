from sqlalchemy import create_engine
from sqlalchemy import select
from db.db_init import Languages, Questions, AppContent
from include.constants import database_path
from include.translate import translate_app


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


def parse_app_content(response):
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


def load_app_content(lang):
    translate_app(lang)
    engine = create_engine(database_path)
    db = engine.connect()

    app_content = parse_app_content(
        db.execute(select(AppContent).join(Languages, AppContent.language_id == Languages.id).where(
            Languages.name == lang)).fetchall()
    )

    return app_content

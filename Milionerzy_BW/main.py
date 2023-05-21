from include.ask_audience import AskAudienceWindow
from include.formats import BACKGROUND_COLORS, FONTS
from include.constants import QUESTION_VALUES, LANGUAGES, database_path, INFO
from include.load_from_database import load_app_content, load_questions
from include.db_init import db_init
from PyQt5.QtWidgets import QApplication, QGridLayout, QGroupBox, QDialog, QPushButton, QVBoxLayout, QTextBrowser, QLabel, QMainWindow, QMessageBox
from PyQt5.QtGui import QFont, QIcon
import random as rm
import time
import sys
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists
import random

from playsound import playsound

were_rules_read = False
was_language_chosen = False
language = None
application_text = None
questions_global = None


def merge_value_with_currency(value: str, currency: str) -> str:
    if currency in ['EUR', 'GBP']:
        return f'{currency} {value}'
    return f'{value} {currency}'


class Millionaires(QDialog):
    def __init__(self):
        super().__init__()

        self.app_texts = application_text['MillionairesWindow']

        self.my_app = None
        self.questions = []

        self.temp_ans_A = ''
        self.temp_ans_B = ''
        self.temp_ans_C = ''
        self.temp_ans_D = ''

        self.my_font = FONTS.Qfont
        self.correct_answer: str = ''
        self.amount_of_points: int = 0
        self.was_game_started: bool = False
        self.was_fifty_fifty_lifebuoy_used: bool = False
        self.was_call_friend_lifebuoy_used: bool = False
        self.was_ask_audience_lifebuoy_used: bool = False

        # Buttons
        # ------------
        self.answer_a_button = QPushButton()
        self.answer_b_button = QPushButton()
        self.answer_c_button = QPushButton()
        self.answer_d_button = QPushButton()
        self.fifty_fifty_lifebuoy_button = QPushButton(self.app_texts['fifty_fifty_button_text'])
        self.call_friend_lifebuoy_button = QPushButton(self.app_texts['call_friend_button_text'])
        self.ask_audience_lifebuoy_button = QPushButton(self.app_texts['ask_audience_button_text'])
        self.start_game_button = QPushButton(self.app_texts['start_game_button_text'])
        self.resign_button = QPushButton(self.app_texts['resign_button_text'])

        self.answer_a_button.clicked.connect(self.answer_a)
        self.answer_b_button.clicked.connect(self.answer_b)
        self.answer_c_button.clicked.connect(self.answer_c)
        self.answer_d_button.clicked.connect(self.answer_d)
        self.fifty_fifty_lifebuoy_button.clicked.connect(self.fifty_fifty_lifebuoy)
        self.call_friend_lifebuoy_button.clicked.connect(self.call_friend_lifebuoy)
        self.ask_audience_lifebuoy_button.clicked.connect(self.ask_audience_lifebuoy)
        self.start_game_button.clicked.connect(self.game_starts)
        self.resign_button.clicked.connect(self.result_of_the_game_after_resign)
        # ------------

        # TextBoxes
        # ------------
        self.textbox_question = QTextBrowser(self)
        self.textbox_checking_correctness = QTextBrowser(self)
        self.textbox_final_result = QTextBrowser(self)
        self.textbox_value_of_question = QTextBrowser(self)
        self.textbox_result_of_using_a_lifebuoy = QTextBrowser(self)
        # ------------

        # GroupBoxes
        # ------------
        self.MillionairesGroupBox = QGroupBox(self.app_texts['MillionairesGroupBoxTitle'])
        self.TakingDecisionGroupBox = QGroupBox(self.app_texts['TakingDecisionGroupBoxTitle'])
        self.LifebuoysGroupBox = QGroupBox(self.app_texts['LifebuoysGroupBoxTitle'])
        self.ValueOfQuestionGroupBox = QGroupBox(self.app_texts['ValueOfQuestionGroupBoxTitle'])
        self.FinalResultGroupBox = QGroupBox(self.app_texts['FinalResultGroupBoxTitle'])
        # ------------

        self.answer_to_button_mapping = {
            'A': self.answer_a_button,
            'B': self.answer_b_button,
            'C': self.answer_c_button,
            'D': self.answer_d_button,
        }

        self.set_formatting()

        self.createMillionairesGroupBox()
        self.createTakingDecisionGroupBox()
        self.createLifebuoysGroupBox()
        self.createValueOfQuestionGroupBox()
        self.createFinalResultGroupBox()
        self.ask_audience_window = AskAudienceWindow(self.app_texts['AskAudienceWindowTitle'])
        self.initUI()

    def initUI(self):
        self.setGeometry(50, 50, 1800, 900)
        main_layout = QGridLayout()
        main_layout.addWidget(self.MillionairesGroupBox, 0, 0)
        main_layout.addWidget(self.LifebuoysGroupBox, 0, 1)
        main_layout.addWidget(self.TakingDecisionGroupBox, 1, 0)
        main_layout.addWidget(self.ValueOfQuestionGroupBox, 1, 1)
        main_layout.addWidget(self.FinalResultGroupBox, 2, 0)
        self.setLayout(main_layout)

        self.setWindowTitle(self.app_texts['MainWindowTitle'])
        self.setWindowIcon(QIcon('milionerzy_logo.png'))

        self.show()

    def set_formatting(self):
        for button in [self.answer_a_button, self.answer_b_button, self.answer_c_button, self.answer_d_button,
                       self.call_friend_lifebuoy_button, self.fifty_fifty_lifebuoy_button,
                       self.ask_audience_lifebuoy_button, self.start_game_button, self.resign_button]:
            button.setFont(self.my_font)
            button.setStyleSheet(BACKGROUND_COLORS.gray)

        for group_box in [self.MillionairesGroupBox, self.TakingDecisionGroupBox, self.LifebuoysGroupBox,
                          self.ValueOfQuestionGroupBox, self.FinalResultGroupBox]:
            group_box.setFont(self.my_font)

    def make_sound(self, mp3_path: str):
        self.my_app.processEvents()
        playsound(mp3_path)

    def check_answer(self, correct_answer: str, my_answer: str) -> bool:
        self.show_correct_answer()
        if my_answer == correct_answer:
            self.textbox_checking_correctness.setText(self.app_texts['textbox_checking_correctness']['correct_answer'])
            self.amount_of_points += 1
            if self.amount_of_points == 12:
                self.textbox_final_result.setText(self.app_texts['textbox_final_result']['victory'] + ' ' +
                                                  self.app_texts['textbox_final_result']['million'] + ' ' +
                                                  self.app_texts['textbox_final_result']['new_game_proposition'])
                self.make_sound('music/milion_won_sound.mp3')
                self.amount_of_points = 0
                return False
            self.make_sound('music/correct_answer_sound.mp3')
            return True

        self.answer_to_button_mapping[my_answer[0]].setStyleSheet(BACKGROUND_COLORS.red)
        self.textbox_checking_correctness.setText(self.app_texts['textbox_checking_correctness']['wrong_answer'] + ': ' +
                                                  self.correct_answer)
        self.make_sound('music/bad_answer_sound.mp3')
        if self.amount_of_points <= 1:
            self.textbox_final_result.setText(self.app_texts['textbox_final_result']['no_victory'] + ' ' +
                                              self.app_texts['textbox_final_result']['new_game_proposition'])
        else:
            price = QUESTION_VALUES[1] if self.amount_of_points <= 6 else QUESTION_VALUES[6]
            self.textbox_final_result.setText(self.app_texts['textbox_final_result']['victory'] + ' ' +
                                              merge_value_with_currency(value=price,
                                                                        currency=self.app_texts['currency']) + '\n' +
                                              self.app_texts['textbox_final_result']['new_game_proposition'])
        self.amount_of_points = 0
        return False

    def get_ready_to_ask_question(self):
        for button in self.answer_to_button_mapping.values():
            button.setText('')
            button.setStyleSheet(BACKGROUND_COLORS.gray)

        self.textbox_question.setText('')
        self.textbox_checking_correctness.setText('')
        self.textbox_result_of_using_a_lifebuoy.setText('')

    def ask_question(self):
        self.get_ready_to_ask_question()

        question_content = random.choice(self.questions)
        self.questions.remove(question_content)

        question = question_content['question']
        correct_ans = question_content['correct_answer']
        answers = [question_content['correct_answer'], question_content['wrong_answer_1'],
                   question_content['wrong_answer_2'], question_content['wrong_answer_3']]

        ans_A = rm.choice(answers)
        answers.remove(ans_A)
        ans_B = rm.choice(answers)
        answers.remove(ans_B)
        ans_C = rm.choice(answers)
        answers.remove(ans_C)
        ans_D = answers[0]

        self.temp_ans_A = 'A. ' + ans_A
        self.temp_ans_B = 'B. ' + ans_B
        self.temp_ans_C = 'C. ' + ans_C
        self.temp_ans_D = 'D. ' + ans_D

        if correct_ans == ans_A:
            self.correct_answer = 'A. ' + correct_ans
        elif correct_ans == ans_B:
            self.correct_answer = 'B. ' + correct_ans
        elif correct_ans == ans_C:
            self.correct_answer = 'C. ' + correct_ans
        elif correct_ans == ans_D:
            self.correct_answer = 'D. ' + correct_ans
        else:
            raise ValueError(f'Unknown answer \'{correct_ans}\'')

        self.textbox_value_of_question.setText(self.app_texts['textbox_value_of_question'] + ' ' +
                                               merge_value_with_currency(
                                                   value=self.question_value(self.amount_of_points),
                                                   currency=self.app_texts['currency'])
                                               )

        if self.amount_of_points != 0:
            self.make_sound('music/ask_question_sound.mp3')

        self.textbox_question.setText(question)
        self.answer_a_button.setText(self.temp_ans_A)
        self.answer_b_button.setText(self.temp_ans_B)
        self.answer_c_button.setText(self.temp_ans_C)
        self.answer_d_button.setText(self.temp_ans_D)

    def shall_i_give_next_question(self, was_answer_correct: bool):
        if was_answer_correct:
            self.my_app.processEvents()
            time.sleep(1)
            self.ask_question()
        else:
            self.textbox_value_of_question.setText('')
            self.was_game_started = False

    def _any_answer(self, temp_ans: str):
        if self.was_game_started and self.answer_to_button_mapping[temp_ans[0]].text() != '':
            self.answer_to_button_mapping[temp_ans[0]].setStyleSheet(BACKGROUND_COLORS.yellow)
            self.make_sound('music/checking_answer_sound.mp3')
            self.shall_i_give_next_question(self.check_answer(self.correct_answer, temp_ans))

    def answer_a(self):
        self._any_answer(self.temp_ans_A)

    def answer_b(self):
        self._any_answer(self.temp_ans_B)

    def answer_c(self):
        self._any_answer(self.temp_ans_C)

    def answer_d(self):
        self._any_answer(self.temp_ans_D)

    def result_of_the_game_after_resign(self):
        if self.was_game_started:
            if self.amount_of_points == 0:
                self.textbox_final_result.setText(self.app_texts['textbox_final_result']['no_victory'] + ' ' +
                                                  self.app_texts['textbox_final_result']['new_game_proposition'])
            else:
                self.textbox_final_result.setText(self.app_texts['textbox_final_result']['victory'] + ' ' +
                                                  merge_value_with_currency(
                                                      value=self.question_value(self.amount_of_points - 1),
                                                      currency=self.app_texts['currency']) + ' ' +
                                                  self.app_texts['textbox_final_result']['new_game_proposition'])
                self.amount_of_points = 0
                self.textbox_value_of_question.setText('')
                self.textbox_checking_correctness.setText(self.app_texts['textbox_checking_correctness']['no_answer'] +
                                                          ' ' + self.correct_answer)
                self.show_correct_answer()
        self.was_game_started = False

    def show_correct_answer(self):
        self.answer_to_button_mapping[self.correct_answer[0]].setStyleSheet(BACKGROUND_COLORS.green)

    def game_starts(self):
        global language, questions_global
        self.textbox_final_result.setText('')
        self.amount_of_points = 0
        self.get_ready_to_ask_question()
        self.questions = dict()
        self.fifty_fifty_lifebuoy_button.setStyleSheet(BACKGROUND_COLORS.gray)
        self.call_friend_lifebuoy_button.setStyleSheet(BACKGROUND_COLORS.gray)
        self.ask_audience_lifebuoy_button.setStyleSheet(BACKGROUND_COLORS.gray)
        self.was_fifty_fifty_lifebuoy_used = False
        self.was_call_friend_lifebuoy_used = False
        self.was_ask_audience_lifebuoy_used = False

        if questions_global is not None:
            self.questions = questions_global
            questions_global = None
        else:
            try:
                self.textbox_question.setText(INFO.questions[language])
                if self.my_app is not None:
                    self.my_app.processEvents()
                self.questions = load_questions(language)
            except ValueError as error:
                show_messagebox(error)
                return

        self.was_game_started = True
        self.make_sound('music/game_starts_sound.mp3')
        self.ask_question()

    def give_bad_answers(self):
        bad_answers = ['A', 'B', 'C', 'D']
        bad_answers.remove(self.correct_answer[0])
        return bad_answers

    def fifty_fifty_lifebuoy(self):
        if not self.was_game_started:
            return

        if self.was_fifty_fifty_lifebuoy_used:
            self.textbox_result_of_using_a_lifebuoy.setText(self.app_texts['textbox_lifebuoy']['lifebuoy_used'])
            return

        bad_answers = self.give_bad_answers()
        bad_answers.remove(rm.choice(bad_answers))
        for bad_ans in bad_answers:
            self.answer_to_button_mapping[bad_ans].setText('')

        self.fifty_fifty_lifebuoy_button.setStyleSheet(BACKGROUND_COLORS.black)
        self.make_sound('music/fifty_fifty_sound.mp3')
        self.was_fifty_fifty_lifebuoy_used = True

    def call_friend_lifebuoy(self):
        if not self.was_game_started:
            return

        if self.was_call_friend_lifebuoy_used:
            self.textbox_result_of_using_a_lifebuoy.setText(self.app_texts['textbox_lifebuoy']['lifebuoy_used'])
            return

        bad_answers = self.give_bad_answers()
        n: int = rm.randint(1, 100)
        if self.was_fifty_fifty_lifebuoy_used:
            if n > 2 * self.amount_of_points:
                hint: str = self.correct_answer[0]
            else:
                for letter, button in self.answer_to_button_mapping.items():
                    if button.text() == '':
                        bad_answers.remove(letter)
                hint = bad_answers[0]
        else:
            if n > 4 * self.amount_of_points:
                hint: str = self.correct_answer[0]
            else:
                hint = rm.choice(bad_answers)

        self.textbox_result_of_using_a_lifebuoy.setText(self.app_texts['textbox_lifebuoy']['call_friend_result']
                                                        + ' ' + hint)
        self.call_friend_lifebuoy_button.setStyleSheet(BACKGROUND_COLORS.black)
        self.was_call_friend_lifebuoy_used = True

    def ask_audience_lifebuoy(self):
        if not self.was_game_started:
            return
        if self.was_ask_audience_lifebuoy_used:
            self.textbox_result_of_using_a_lifebuoy.setText(self.app_texts['textbox_lifebuoy']['lifebuoy_used'])
            return

        self.make_sound('music/ask_audience_sound.mp3')
        bad_answers = self.give_bad_answers()
        n: int = rm.randint(1, 100)
        votes_for = {'A': None, 'B': None, 'C': None, 'D': None}
        correct_ans = self.correct_answer[0]

        if self.was_fifty_fifty_lifebuoy_used:
            for ans, button in self.answer_to_button_mapping.items():
                if button.text() == '':
                    votes_for[ans] = 0
                    bad_answers.remove(ans)
            votes_for[correct_ans] = rm.randint(45, 83) if n > 2 * self.amount_of_points else rm.randint(35, 63)
            votes_for[bad_answers[0]] = 100 - votes_for[correct_ans]
        else:
            bad_ans_1 = rm.choice(bad_answers)
            bad_answers.remove(bad_ans_1)
            bad_ans_2 = rm.choice(bad_answers)
            bad_answers.remove(bad_ans_2)
            bad_ans_3 = bad_answers[0]
            votes_for[correct_ans] = rm.randint(45, 83) if n > 4 * self.amount_of_points else rm.randint(35, 63)
            votes_for[bad_ans_1] = rm.randint(0, 100 - votes_for[correct_ans])
            votes_for[bad_ans_2] = rm.randint(0, 100 - votes_for[correct_ans] - votes_for[bad_ans_1])
            votes_for[bad_ans_3] = 100 - votes_for[correct_ans] - votes_for[bad_ans_1] - votes_for[bad_ans_2]

        self.ask_audience_window.show_bar_graph(votes_for['A'], votes_for['B'], votes_for['C'], votes_for['D'])
        self.ask_audience_lifebuoy_button.setStyleSheet(BACKGROUND_COLORS.black)
        self.was_ask_audience_lifebuoy_used = True

    def createMillionairesGroupBox(self):
        layout = QVBoxLayout()
        self.add_widgets_to_layout(
            layout=layout,
            widgets=[self.start_game_button, self.textbox_question, self.answer_a_button, self.answer_b_button,
                     self.answer_c_button, self.answer_d_button, self.textbox_checking_correctness]
        )
        self.MillionairesGroupBox.setLayout(layout)

    def createTakingDecisionGroupBox(self):
        layout = QVBoxLayout()
        layout.addWidget(self.resign_button)
        self.TakingDecisionGroupBox.setLayout(layout)

    def createLifebuoysGroupBox(self):
        layout = QVBoxLayout()
        self.add_widgets_to_layout(
            layout=layout,
            widgets=[self.fifty_fifty_lifebuoy_button, self.call_friend_lifebuoy_button,
                     self.ask_audience_lifebuoy_button, self.textbox_result_of_using_a_lifebuoy]
        )
        layout.addStretch(1)
        self.LifebuoysGroupBox.setLayout(layout)

    def createValueOfQuestionGroupBox(self):
        layout = QVBoxLayout()
        layout.addWidget(self.textbox_value_of_question)
        self.ValueOfQuestionGroupBox.setLayout(layout)

    def createFinalResultGroupBox(self):
        layout = QVBoxLayout()
        layout.addWidget(self.textbox_final_result)
        self.FinalResultGroupBox.setLayout(layout)

    @staticmethod
    def add_widgets_to_layout(layout, widgets):
        for widget in widgets:
            layout.addWidget(widget)

    @staticmethod
    def question_value(points: int) -> str:
        try:
            return QUESTION_VALUES[points]
        except KeyError:
            return '0'


def show_messagebox(text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)

    # setting message for Message Box
    msg.setText(str(text))

    # setting Message box window title
    msg.setWindowTitle("Error")

    # declaring buttons on Message Box
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    # start the app
    retval = msg.exec_()


def load_text():
    global language, application_text, questions_global
    application_text = load_app_content(language)
    questions_global = load_questions(language)


def start_rules():
    try:
        load_text()
    except ValueError as error:
        show_messagebox(error)
        return

    global was_language_chosen
    was_language_chosen = True
    language_window.exit()


class LanguageWindow(QDialog):
    def __init__(self):
        global language

        self.my_app = None

        language = LANGUAGES.polish

        super().__init__()

        self.my_font = FONTS.Qfont

        # Check if database exists and create it if necessary
        # ------------
        engine = create_engine(database_path)
        if not database_exists(engine.url):
            db_init()
        # ------------

        # Buttons
        # ------------
        self.polish_button = QPushButton("Polski")
        self.english_button = QPushButton("English")
        self.german_button = QPushButton("Deutsch")
        self.confirmation_button = QPushButton("Zatwierdź")

        self.tmp_button = QPushButton()

        self.polish_button.clicked.connect(self.language_polish)
        self.english_button.clicked.connect(self.language_english)
        self.german_button.clicked.connect(self.language_german)
        self.confirmation_button.clicked.connect(self._start_rules)
        # ------------

        self.LanguageGroupBox = QGroupBox("Wybierz język")

        self.set_formatting()

        self.createLanguageGroupBox()

        self.initUI()

    def initUI(self):
        self.setGeometry(500, 300, 800, 500)
        main_layout = QGridLayout()
        main_layout.addWidget(self.LanguageGroupBox, 0, 0)
        main_layout.addWidget(self.confirmation_button, 1, 0)
        main_layout.addWidget(self.tmp_button, 2, 0)
        self.setLayout(main_layout)
        self.setWindowTitle('Menu')
        self.setWindowIcon(QIcon('milionerzy_logo.png'))
        self.show()

    def _start_rules(self):
        global language
        self.tmp_button.setText(INFO.application[language])
        if self.my_app is not None:
            self.my_app.processEvents()
        start_rules()

    def set_formatting(self):
        for button in [self.polish_button, self.english_button, self.german_button, self.confirmation_button]:
            button.setFont(self.my_font)
            button.setStyleSheet(BACKGROUND_COLORS.green if button == self.polish_button else BACKGROUND_COLORS.gray)

        self.LanguageGroupBox.setFont(self.my_font)

    def updateUI(self):
        global language
        self.reset_button_backgrounds()
        if language == LANGUAGES.polish:
            self.LanguageGroupBox.setTitle("Wybierz język")
            self.confirmation_button.setText("Zatwierdź")
            self.polish_button.setStyleSheet(BACKGROUND_COLORS.green)
        elif language == LANGUAGES.english:
            self.LanguageGroupBox.setTitle("Choose language")
            self.confirmation_button.setText("Confirm")
            self.english_button.setStyleSheet(BACKGROUND_COLORS.green)
        elif language == LANGUAGES.german:
            self.LanguageGroupBox.setTitle("Sprache auswählen")
            self.confirmation_button.setText("Bestätige")
            self.german_button.setStyleSheet(BACKGROUND_COLORS.green)
        else:
            raise ValueError(f'Unknown language \'{language}\'')

    def reset_button_backgrounds(self):
        for button in [self.polish_button, self.english_button, self.german_button]:
            button.setStyleSheet(BACKGROUND_COLORS.gray)

    def language_polish(self):
        self._language_choice(LANGUAGES.polish)

    def language_english(self):
        self._language_choice(LANGUAGES.english)

    def language_german(self):
        self._language_choice(LANGUAGES.german)

    def _language_choice(self, chosen_language):
        global language
        language = chosen_language
        self.updateUI()

    def createLanguageGroupBox(self):
        layout = QVBoxLayout()
        for button in [self.polish_button, self.english_button, self.german_button]:
            layout.addWidget(button)
        self.LanguageGroupBox.setLayout(layout)


def start_game():
    global were_rules_read
    were_rules_read = True
    rules_window.exit()


class RulesWindow(QDialog):
    def __init__(self):
        global application_text
        super().__init__()

        self.textbox_rules = QTextBrowser()
        self.textbox_rules.setText(application_text['RulesWindow']['rules'])
        self.lets_go_to_game_button = QPushButton(application_text['RulesWindow']['button_text'])
        self.lets_go_to_game_button.clicked.connect(start_game)

        self.RulesGroupBox = QGroupBox(application_text['RulesWindow']['group_box_name'])
        self.RulesGroupBox.setFont(FONTS.Qfont)
        self.createRulesGroupBox()

        self.initUI()

    def initUI(self):
        self.setGeometry(500, 300, 800, 500)
        main_layout = QGridLayout()
        main_layout.addWidget(self.RulesGroupBox, 0, 0)
        self.setLayout(main_layout)
        self.setWindowTitle('Menu')
        self.setWindowIcon(QIcon('milionerzy_logo.png'))
        self.show()

    def createRulesGroupBox(self):
        layout = QVBoxLayout()
        layout.addWidget(self.textbox_rules)
        layout.addWidget(self.lets_go_to_game_button)
        self.RulesGroupBox.setLayout(layout)


if __name__ == '__main__':
    language_window = QApplication(sys.argv)
    my_window_language = LanguageWindow()
    my_window_language.my_app = language_window
    language_window.exec_()
    language_window.closeAllWindows()

    if was_language_chosen:
        rules_window = QApplication(sys.argv)
        my_window = RulesWindow()
        rules_window.exec_()
        rules_window.closeAllWindows()

    if were_rules_read:
        app_ = QApplication(sys.argv)
        millionaires_app = Millionaires()
        millionaires_app.my_app = app_
        sys.exit(app_.exec_())

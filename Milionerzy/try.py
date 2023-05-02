#!/usr/bin/python
# -*- coding: utf-8 -*-

from include.asking_question import give_a_question_with_answers_as_tuple, set_all_questions_as_ready_to_ask_if_necessary
from include.bar_graph import draw_a_bar_graph
from include.giving_rules import give_rules
from PyQt5.QtWidgets import QApplication, QGridLayout, QGroupBox, QDialog, QPushButton, QVBoxLayout, QTextBrowser, QLabel
from PyQt5.QtGui import QFont, QIcon
import random as rm
import time
from playsound import playsound


were_rules_read = False


def start_game():

    global were_rules_read
    were_rules_read = True
    rules_window.exit()


class Millionaires(QDialog):
    def __init__(self):
        super().__init__()

        self.my_app = None

        self.temp_ans_A = ""
        self.temp_ans_B = ""
        self.temp_ans_C = ""
        self.temp_ans_D = ""

        self.my_font: QFont = QFont('Arial', 18)
        self.my_font.setBold(True)
        self.correct_answer: str = ""
        self.amount_of_points: int = 0
        self.was_game_started: bool = False
        self.was_fifty_fifty_lifebuoy_used: bool = False
        self.was_call_friend_lifebuoy_used: bool = False
        self.was_ask_audience_lifebuoy_used: bool = False

        self.answer_a_button = QPushButton()
        self.answer_a_button.setFont(self.my_font)
        self.answer_a_button.setStyleSheet("background-color:#fff;")
        self.answer_a_button.clicked.connect(self.answer_a)

        self.answer_b_button = QPushButton()
        self.answer_b_button.setFont(self.my_font)
        self.answer_b_button.clicked.connect(self.answer_b)
        self.answer_b_button.setStyleSheet("background-color:#fff;")

        self.answer_c_button = QPushButton()
        self.answer_c_button.setFont(self.my_font)
        self.answer_c_button.clicked.connect(self.answer_c)
        self.answer_c_button.setStyleSheet("background-color:#fff;")

        self.answer_d_button = QPushButton()
        self.answer_d_button.setFont(self.my_font)
        self.answer_d_button.clicked.connect(self.answer_d)
        self.answer_d_button.setStyleSheet("background-color:#fff;")

        self.fifty_fifty_lifebuoy_button = QPushButton("50 / 50")
        self.fifty_fifty_lifebuoy_button.setFont(self.my_font)
        self.fifty_fifty_lifebuoy_button.clicked.connect(self.fifty_fifty_lifebuoy)
        self.fifty_fifty_lifebuoy_button.setStyleSheet("background-color:#fff;")

        self.call_friend_lifebuoy_button = QPushButton("Telefon do przyjaciela")
        self.call_friend_lifebuoy_button.setFont(self.my_font)
        self.call_friend_lifebuoy_button.clicked.connect(self.call_friend_lifebuoy)
        self.call_friend_lifebuoy_button.setStyleSheet("background-color:#fff;")

        self.ask_audience_lifebuoy_button = QPushButton("Pytanie do publiczności")
        self.ask_audience_lifebuoy_button.setFont(self.my_font)
        self.ask_audience_lifebuoy_button.clicked.connect(self.ask_audience_lifebuoy)
        self.ask_audience_lifebuoy_button.setStyleSheet("background-color:#fff;")

        self.textbox_question = QTextBrowser(self)
        self.textbox_checking_correctness = QTextBrowser(self)
        self.textbox_final_result = QTextBrowser(self)
        self.textbox_value_of_question = QTextBrowser(self)
        self.textbox_result_of_using_a_lifebuoy = QTextBrowser(self)

        self.MillionairesGroupBox = QGroupBox("Pytanie")
        self.MillionairesGroupBox.setFont(self.my_font)
        self.TakingDecisionGroupBox = QGroupBox("Czy chcesz grać dalej?")
        self.TakingDecisionGroupBox.setFont(self.my_font)
        self.LifebuoysGroupBox = QGroupBox("Koła ratunkowe")
        self.LifebuoysGroupBox.setFont(self.my_font)
        self.ValueOfQuestionGroupBox = QGroupBox("Wartość pytania")
        self.ValueOfQuestionGroupBox.setFont(self.my_font)
        self.FinalResultGroupBox = QGroupBox("Wynik gry")
        self.FinalResultGroupBox.setFont(self.my_font)

        self.createMillionairesGroupBox()
        self.createTakingDecisionGroupBox()
        self.createLifebuoysGroupBox()
        self.createValueOfQuestionGroupBox()
        self.createFinalResultGroupBox()

        self.initUI()

    def initUI(self):
        self.setGeometry(0, 30, 2000, 1010)
        main_layout = QGridLayout()
        main_layout.addWidget(self.MillionairesGroupBox, 0, 0)
        main_layout.addWidget(self.LifebuoysGroupBox, 0, 1)
        main_layout.addWidget(self.TakingDecisionGroupBox, 1, 0)
        main_layout.addWidget(self.ValueOfQuestionGroupBox, 1, 1)
        main_layout.addWidget(self.FinalResultGroupBox, 2, 0)
        self.setLayout(main_layout)

        self.setWindowTitle("Milionerzy")
        self.setWindowIcon(QIcon('milionerzy_logo.png'))

        self.show()

    @staticmethod
    def what_is_the_value_of_the_question(points: int) -> str:
        value: str = '0'
        if points == 0:
            value = '500'
        if points == 1:
            value = '1000'
        if points == 2:
            value = '2000'
        if points == 3:
            value = '5000'
        if points == 4:
            value = '10 000'
        if points == 5:
            value = '20 000'
        if points == 6:
            value = '40 000'
        if points == 7:
            value = '75 000'
        if points == 8:
            value = '125 000'
        if points == 9:
            value = '250 000'
        if points == 10:
            value = '500 000'
        if points == 11:
            value = '1 000 000'
        return value

    def check_answer(self, correct_answer: str, my_answer: str) -> bool:
        if my_answer == correct_answer:
            self.show_correct_answer()
            self.textbox_checking_correctness.setText("Brawo, to jest poprawna odpowiedź! :)")
            self.amount_of_points += 1
            if self.amount_of_points == 12:
                self.textbox_final_result.setText("Wygrałeś Milion !!!\n"
                                                  "Jeśli chcesz zagrać jeszcze raz kliknij przycisk 'Rozpocznij grę'")
                self.my_app.processEvents()
                playsound('music/milion_won_sound.mp3')
                self.amount_of_points = 0
                return False
            self.my_app.processEvents()
            playsound('music/correct_answer_sound.mp3')
            return True
        else:
            if my_answer[0] == "A":
                self.answer_a_button.setStyleSheet("background-color:#f00;")
            if my_answer[0] == "B":
                self.answer_b_button.setStyleSheet("background-color:#f00;")
            if my_answer[0] == "C":
                self.answer_c_button.setStyleSheet("background-color:#f00;")
            if my_answer[0] == "D":
                self.answer_d_button.setStyleSheet("background-color:#f00;")
            self.show_correct_answer()
            self.textbox_checking_correctness.setText("Niestety, jest to zła odpowiedź! :(\n"
                                                      "Poprawną odpowiedzią była odpowiedź " + self.correct_answer)
            self.my_app.processEvents()
            playsound('music/bad_answer_sound.mp3')
            if self.amount_of_points <= 1:
                self.textbox_final_result.setText("Niestety nic dziś nie wygrałeś :(\n"
                                                  "Jeśli chcesz zagrać jeszcze raz kliknij przycisk 'Rozpocznij grę'")
            if 1 < self.amount_of_points <= 6:
                self.textbox_final_result.setText("Wygrałeś 1000 zł\n"
                                                  "Jeśli chcesz zagrać jeszcze raz kliknij przycisk 'Rozpocznij grę'")
            if self.amount_of_points > 6:
                self.textbox_final_result.setText("Wygrałeś 40000 zł\n"
                                                  "Jeśli chcesz zagrać jeszcze raz kliknij przycisk 'Rozpocznij grę'")
            self.amount_of_points = 0
            return False

    def make_all_answer_buttons_clear(self):
        self.textbox_question.setText("")
        self.answer_a_button.setText("")
        self.answer_b_button.setText("")
        self.answer_c_button.setText("")
        self.answer_d_button.setText("")
        self.answer_a_button.setStyleSheet("background-color:#fff;")
        self.answer_b_button.setStyleSheet("background-color:#fff;")
        self.answer_c_button.setStyleSheet("background-color:#fff;")
        self.answer_d_button.setStyleSheet("background-color:#fff;")

    def ask_question(self):
        self.make_all_answer_buttons_clear()
        self.textbox_checking_correctness.setText("")
        self.textbox_result_of_using_a_lifebuoy.setText("")
        question, ans_A, ans_B, ans_C, ans_D, correct_ans = give_a_question_with_answers_as_tuple()

        self.temp_ans_A = "A. " + ans_A
        self.temp_ans_B = "B. " + ans_B
        self.temp_ans_C = "C. " + ans_C
        self.temp_ans_D = "D. " + ans_D

        if correct_ans == ans_A:
            self.correct_answer = "A. " + correct_ans
        if correct_ans == ans_B:
            self.correct_answer = "B. " + correct_ans
        if correct_ans == ans_C:
            self.correct_answer = "C. " + correct_ans
        if correct_ans == ans_D:
            self.correct_answer = "D. " + correct_ans

        self.textbox_value_of_question.setText("Pytanie za " +
                                               self.what_is_the_value_of_the_question(self.amount_of_points) + "zł")

        if self.amount_of_points != 0:
            self.my_app.processEvents()
            playsound('music/ask_question_sound.mp3')

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
            self.textbox_value_of_question.setText("")
            self.was_game_started = False

    def answer_a(self):
        if self.was_game_started:
            self.answer_a_button.setStyleSheet("background-color:#ff0;")
            self.my_app.processEvents()
            playsound('music/checking_answer_sound.mp3')
            self.shall_i_give_next_question(self.check_answer(self.correct_answer, self.temp_ans_A))
        else:
            pass

    def answer_b(self):
        if self.was_game_started:
            self.answer_b_button.setStyleSheet("background-color:#ff0;")
            self.my_app.processEvents()
            playsound('music/checking_answer_sound.mp3')
            self.shall_i_give_next_question(self.check_answer(self.correct_answer, self.temp_ans_B))
        else:
            pass

    def answer_c(self):
        if self.was_game_started:
            self.answer_c_button.setStyleSheet("background-color:#ff0;")
            self.my_app.processEvents()
            playsound('music/checking_answer_sound.mp3')
            self.shall_i_give_next_question(self.check_answer(self.correct_answer, self.temp_ans_C))
        else:
            pass

    def answer_d(self):
        if self.was_game_started:
            self.answer_d_button.setStyleSheet("background-color:#ff0;")
            self.my_app.processEvents()
            playsound('music/checking_answer_sound.mp3')
            self.shall_i_give_next_question(self.check_answer(self.correct_answer, self.temp_ans_D))
        else:
            pass

    def result_of_the_game_after_resign(self):
        if self.amount_of_points == 0:
            self.textbox_final_result.setText("Niestety nic dziś nie wygrałeś/łaś :(")
        else:
            self.textbox_final_result.setText("Wygrałeś/łaś "
                                              + self.what_is_the_value_of_the_question(self.amount_of_points - 1)
                                              + "zł")
            self.amount_of_points = 0
            self.textbox_value_of_question.setText("")
            self.textbox_checking_correctness.setText("Poprawną odpowiedzią była odpowiedź " + self.correct_answer)
            self.show_correct_answer()
        self.was_game_started = False

    def show_correct_answer(self):
        if self.correct_answer[0] == "A":
            self.answer_a_button.setStyleSheet("background-color:#0f0;")
        if self.correct_answer[0] == "B":
            self.answer_b_button.setStyleSheet("background-color:#0f0;")
        if self.correct_answer[0] == "C":
            self.answer_c_button.setStyleSheet("background-color:#0f0;")
        if self.correct_answer[0] == "D":
            self.answer_d_button.setStyleSheet("background-color:#0f0;")

    def game_starts(self):
        # MyClass()
        self.textbox_final_result.setText("")
        self.textbox_checking_correctness.setText("")
        self.textbox_result_of_using_a_lifebuoy.setText("")
        self.amount_of_points = 0
        self.make_all_answer_buttons_clear()

        self.fifty_fifty_lifebuoy_button.setStyleSheet("background-color:#fff;")
        self.call_friend_lifebuoy_button.setStyleSheet("background-color:#fff;")
        self.ask_audience_lifebuoy_button.setStyleSheet("background-color:#fff;")
        self.was_fifty_fifty_lifebuoy_used = False
        self.was_call_friend_lifebuoy_used = False
        self.was_ask_audience_lifebuoy_used = False
        self.was_game_started = True
        set_all_questions_as_ready_to_ask_if_necessary()
        self.my_app.processEvents()
        playsound('music/game_starts_sound.mp3')
        self.ask_question()

    def fifty_fifty_lifebuoy(self):
        if self.was_game_started:
            if self.was_fifty_fifty_lifebuoy_used:
                self.textbox_result_of_using_a_lifebuoy.setText("To koło ratunkowe zostało już użyte")
            else:
                bad_answers = ["A", "B", "C", "D"]
                bad_answers.remove(self.correct_answer[0])
                answer_to_del = rm.choice(bad_answers)
                bad_answers.remove(answer_to_del)
                if bad_answers[0] == "A" or bad_answers[1] == "A":
                    self.answer_a_button.setText("")
                if bad_answers[0] == "B" or bad_answers[1] == "B":
                    self.answer_b_button.setText("")
                if bad_answers[0] == "C" or bad_answers[1] == "C":
                    self.answer_c_button.setText("")
                if bad_answers[0] == "D" or bad_answers[1] == "D":
                    self.answer_d_button.setText("")

            self.fifty_fifty_lifebuoy_button.setStyleSheet("background-color:#000;")
            self.my_app.processEvents()
            playsound('music/fifty_fifty_sound.mp3')
            self.was_fifty_fifty_lifebuoy_used = True
        else:
            pass

    def call_friend_lifebuoy(self):
        if self.was_game_started:
            if self.was_call_friend_lifebuoy_used:
                self.textbox_result_of_using_a_lifebuoy.setText("To koło ratunkowe zostało już użyte")
            else:
                bad_answers = ["A", "B", "C", "D"]
                bad_answers.remove(self.correct_answer[0])
                n: int = rm.randint(1, 100)
                if self.was_fifty_fifty_lifebuoy_used:
                    if n > 5:
                        hint: str = self.correct_answer[0]
                    else:
                        if self.answer_a_button.text() == "":
                            bad_answers.remove("A")
                        if self.answer_b_button.text() == "":
                            bad_answers.remove("B")
                        if self.answer_c_button.text() == "":
                            bad_answers.remove("C")
                        if self.answer_d_button.text() == "":
                            bad_answers.remove("D")
                        hint = bad_answers[0]
                    self.textbox_result_of_using_a_lifebuoy.setText("Wydaje mi się, że jest to odpowiedź " + hint)
                else:
                    if n > 20:
                        hint: str = self.correct_answer[0]
                    else:
                        hint = rm.choice(bad_answers)
                    self.textbox_result_of_using_a_lifebuoy.setText("Wydaje mi się, że jest to odpowiedź " + hint)

            self.call_friend_lifebuoy_button.setStyleSheet("background-color:#000;")
            self.was_call_friend_lifebuoy_used = True
        else:
            pass

    def ask_audience_lifebuoy(self):
        if self.was_game_started:
            if self.was_ask_audience_lifebuoy_used:
                self.textbox_result_of_using_a_lifebuoy.setText("To koło ratunkowe zostało już użyte")
            else:
                playsound('music/ask_audience_sound.mp3')
                bad_answers = ["A", "B", "C", "D"]
                bad_answers.remove(self.correct_answer[0])
                n: int = rm.randint(1, 100)

                if self.was_fifty_fifty_lifebuoy_used:
                    bad_answer_2 = ""
                    bad_answer_3 = ""
                    if self.answer_a_button.text() == "":
                        bad_answers.remove("A")
                        bad_answer_2 = "A"
                        bad_answer_3 = "A"
                    if self.answer_b_button.text() == "":
                        bad_answers.remove("B")
                        bad_answer_2 = "B"
                        bad_answer_3 = "B"
                    if self.answer_c_button.text() == "":
                        bad_answers.remove("C")
                        bad_answer_2 = "C"
                        bad_answer_3 = "C"
                    if self.answer_d_button.text() == "":
                        bad_answers.remove("D")
                        bad_answer_2 = "D"
                        bad_answer_3 = "D"
                    bad_answer_1 = bad_answers[0]
                    if n > 5:
                        votes_for_correct_answer = rm.randint(45, 83)
                        votes_for_bad_answer_1 = 100 - votes_for_correct_answer
                        votes_for_bad_answer_2 = 0
                        votes_for_bad_answer_3 = 0
                    else:
                        votes_for_correct_answer = rm.randint(35, 63)
                        votes_for_bad_answer_1 = 100 - votes_for_correct_answer
                        votes_for_bad_answer_2 = 0
                        votes_for_bad_answer_3 = 0
                else:
                    bad_answer_1 = rm.choice(bad_answers)
                    bad_answers.remove(bad_answer_1)
                    bad_answer_2 = rm.choice(bad_answers)
                    bad_answers.remove(bad_answer_2)
                    bad_answer_3 = bad_answers[0]
                    n: int = rm.randint(1, 100)
                    if n > 20:
                        votes_for_correct_answer = rm.randint(45, 83)
                        votes_for_bad_answer_1 = rm.randint(0, (100 - votes_for_correct_answer))
                        votes_for_bad_answer_2 = rm.randint(0,
                                                            (100 - votes_for_correct_answer - votes_for_bad_answer_1))
                        votes_for_bad_answer_3 = 100 - votes_for_correct_answer - votes_for_bad_answer_1 - votes_for_bad_answer_2
                    else:
                        votes_for_correct_answer = rm.randint(35, 63)
                        votes_for_bad_answer_1 = rm.randint(0, (100 - votes_for_correct_answer))
                        votes_for_bad_answer_2 = rm.randint(0,
                                                            (100 - votes_for_correct_answer - votes_for_bad_answer_1))
                        votes_for_bad_answer_3 = 100 - votes_for_correct_answer - votes_for_bad_answer_1 - votes_for_bad_answer_2

                votes_for_A = 0
                votes_for_B = 0
                votes_for_C = 0
                votes_for_D = 0

                if self.correct_answer[0] == "A":
                    votes_for_A = votes_for_correct_answer
                if self.correct_answer[0] == "B":
                    votes_for_B = votes_for_correct_answer
                if self.correct_answer[0] == "C":
                    votes_for_C = votes_for_correct_answer
                if self.correct_answer[0] == "D":
                    votes_for_D = votes_for_correct_answer
                if bad_answer_1 == "A":
                    votes_for_A = votes_for_bad_answer_1
                if bad_answer_1 == "B":
                    votes_for_B = votes_for_bad_answer_1
                if bad_answer_1 == "C":
                    votes_for_C = votes_for_bad_answer_1
                if bad_answer_1 == "D":
                    votes_for_D = votes_for_bad_answer_1
                if bad_answer_2 == "A":
                    votes_for_A = votes_for_bad_answer_2
                if bad_answer_2 == "B":
                    votes_for_B = votes_for_bad_answer_2
                if bad_answer_2 == "C":
                    votes_for_C = votes_for_bad_answer_2
                if bad_answer_2 == "D":
                    votes_for_D = votes_for_bad_answer_2
                if bad_answer_3 == "A":
                    votes_for_A = votes_for_bad_answer_3
                if bad_answer_3 == "B":
                    votes_for_B = votes_for_bad_answer_3
                if bad_answer_3 == "C":
                    votes_for_C = votes_for_bad_answer_3
                if bad_answer_3 == "D":
                    votes_for_D = votes_for_bad_answer_3

                draw_a_bar_graph(votes_for_A, votes_for_B, votes_for_C, votes_for_D)

            self.ask_audience_lifebuoy_button.setStyleSheet("background-color:#000;")
            self.was_ask_audience_lifebuoy_used = True
        else:
            pass

    def createMillionairesGroupBox(self):
        layout = QVBoxLayout()

        start_game_button = QPushButton("Rozpocznij grę")
        start_game_button.clicked.connect(self.game_starts)
        start_game_button.setStyleSheet("background-color:#fff;")
        start_game_button.setFont(self.my_font)
        layout.addWidget(start_game_button)
        layout.addWidget(self.textbox_question)
        layout.addWidget(self.answer_a_button)
        layout.addWidget(self.answer_b_button)
        layout.addWidget(self.answer_c_button)
        layout.addWidget(self.answer_d_button)
        layout.addWidget(self.textbox_checking_correctness)

        self.MillionairesGroupBox.setLayout(layout)

    def createTakingDecisionGroupBox(self):
        layout = QVBoxLayout()

        resign_button = QPushButton("Rezygnuję")
        resign_button.clicked.connect(self.result_of_the_game_after_resign)
        resign_button.setStyleSheet("background-color:#fff;")
        resign_button.setFont(self.my_font)
        layout.addWidget(resign_button)

        self.TakingDecisionGroupBox.setLayout(layout)

    def createLifebuoysGroupBox(self):
        layout = QVBoxLayout()

        layout.addWidget(self.fifty_fifty_lifebuoy_button)
        layout.addWidget(self.call_friend_lifebuoy_button)
        layout.addWidget(self.ask_audience_lifebuoy_button)
        layout.addWidget(self.textbox_result_of_using_a_lifebuoy)

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


class RulesWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.my_font: QFont = QFont('Arial', 18)
        self.my_font.setBold(True)

        self.RulesGroupBox = QGroupBox("")
        self.RulesGroupBox.setFont(self.my_font)

        self.createRulesGroupBox()

        self.initUI()

    def initUI(self):

        self.setGeometry(500, 300, 800, 500)
        main_layout = QGridLayout()
        main_layout.addWidget(self.RulesGroupBox, 0, 0)
        self.setLayout(main_layout)

        self.setWindowTitle("Zasady gry Milionerzy")
        self.setWindowIcon(QIcon('milionerzy_logo.png'))

        self.show()

    def createRulesGroupBox(self):
        layout = QVBoxLayout()

        textbox_rules = QTextBrowser(self)
        textbox_rules.setText(give_rules())

        layout.addWidget(textbox_rules)

        lets_go_to_game_button = QPushButton('Przejdź do gry')
        lets_go_to_game_button.clicked.connect(start_game)

        layout.addWidget(lets_go_to_game_button)

        self.RulesGroupBox.setLayout(layout)


if __name__ == '__main__':
    import sys

    rules_window = QApplication(sys.argv)
    my_window = RulesWindow()
    rules_window.exec_()
    rules_window.closeAllWindows()

    if were_rules_read:
        app_ = QApplication(sys.argv)
        millionaires_app = Millionaires()
        millionaires_app.my_app = app_
        sys.exit(app_.exec_())

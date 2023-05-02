#!/usr/bin/python
# -*- coding: utf-8 -*-

import random as rm
from typing import List, Dict, Tuple


def filling_the_list_of_questions_to_choose(question_list: Dict[Tuple[str, str, str, str, str, str], bool]) -> List[Tuple[str, str, str, str, str, str]]:
    questions_to_random_choice: List[Tuple[str, str, str, str, str, str]] = []
    for question_as_key in question_list.keys():
        if question_list[question_as_key] is True:
            questions_to_random_choice.append(question_as_key)
    return questions_to_random_choice


def set_all_questions_as_ready_to_ask_if_necessary():
    file_with_questions_to_read = open("file_with_questions.txt", "r", encoding="windows-1250")

    n: int = 0

    for line in file_with_questions_to_read:
        if line.strip()[:-3] == "True":
            n += 1

    file_with_questions_to_read.close()

    if n < 12:
        lines_from_file_with_questions = open("file_with_questions.txt", encoding="windows-1250").readlines()

        file_with_questions_to_write = open("file_with_questions.txt", "w", encoding="windows-1250")

        for line_with_word_to_change in lines_from_file_with_questions:
            file_with_questions_to_write.write(line_with_word_to_change.replace("False", "True"))

        file_with_questions_to_write.close()
    else:
        pass


def give_a_question_with_answers_as_tuple() -> Tuple[str, str, str, str, str, str]:
    #                                               [question, ans A, ans B, ans C, ans D, correct ans]
    file_with_questions_to_read = open("file_with_questions.txt", "r", encoding="windows-1250")
    questions = {}
    temp_question = ""
    correct_answer = ""
    answer_A = ""
    answer_B = ""
    answer_C = ""
    answer_D = ""
    answers_names = ["A", "B", "C", "D"]
    for line in file_with_questions_to_read:
        if line.strip()[-1] == ";":
            if line.strip()[-2] == ';':
                if line.strip()[-3] == ';':
                    if line.strip()[:-3] == "True":
                        questions[(temp_question, answer_A, answer_B, answer_C, answer_D, correct_answer)] = True
                    else:
                        questions[(temp_question, answer_A, answer_B, answer_C, answer_D, correct_answer)] = False
                    temp_question = ""
                    correct_answer = ""
                    answers_names = ["A", "B", "C", "D"]
                else:
                    what_is_the_question = rm.choice(answers_names)
                    answers_names.remove(what_is_the_question)
                    correct_answer = line.strip()[:-2]

                    if what_is_the_question == "A":
                        answer_A = line.strip()[:-2]
                    if what_is_the_question == "B":
                        answer_B = line.strip()[:-2]
                    if what_is_the_question == "C":
                        answer_C = line.strip()[:-2]
                    if what_is_the_question == "D":
                        answer_D = line.strip()[:-2]
            else:
                what_is_the_question = rm.choice(answers_names)
                answers_names.remove(what_is_the_question)

                if what_is_the_question == "A":
                    answer_A = line.strip()[:-1]
                if what_is_the_question == "B":
                    answer_B = line.strip()[:-1]
                if what_is_the_question == "C":
                    answer_C = line.strip()[:-1]
                if what_is_the_question == "D":
                    answer_D = line.strip()[:-1]
        else:
            temp_question += line.strip() + "\n"

    file_with_questions_to_read.close()
    questions_to_choose: List[Tuple[str, str, str, str, str, str]] = filling_the_list_of_questions_to_choose(questions)
    if len(questions_to_choose) == 0:
        for question, ans_a, ans_b, ans_c, ans_d, correct_ans in questions.keys():
            questions[(question, ans_a, ans_b, ans_c, ans_d, correct_ans)] = True
        questions_to_choose = filling_the_list_of_questions_to_choose(questions)
    the_chosen_question: Tuple[str, str, str, str, str, str] = rm.choice(questions_to_choose)
    questions[the_chosen_question] = False
    file_with_questions_to_write = open("file_with_questions.txt", "w",  encoding="windows-1250")
    file_with_questions_to_write.write(dict_with_questions_as_string(questions))
    file_with_questions_to_write.close()
    q, a_A, a_B, a_C, a_D, c_a = the_chosen_question
    question_ready_to_ask = q.replace(";", "")
    final_answer_a = a_A.replace(";", "")
    final_answer_b = a_B.replace(";", "")
    final_answer_c = a_C.replace(";", "")
    final_answer_d = a_D.replace(";", "")
    return question_ready_to_ask, final_answer_a, final_answer_b, final_answer_c, final_answer_d, c_a


def dict_with_questions_as_string(questions_dct: Dict[Tuple[str, str, str, str, str, str], bool]) -> str:
    dict_as_string = ""
    for quest, ans_a, ans_b, ans_c, ans_d, correct_ans in questions_dct:
        temp_ans_a = ans_a
        temp_ans_b = ans_b
        temp_ans_c = ans_c
        temp_ans_d = ans_d
        if ans_a == correct_ans:
            temp_ans_a += ";"
        if ans_b == correct_ans:
            temp_ans_b += ";"
        if ans_c == correct_ans:
            temp_ans_c += ";"
        if ans_d == correct_ans:
            temp_ans_d += ";"
        dict_as_string += quest + temp_ans_a + ";\n" + temp_ans_b + ";\n" + temp_ans_c + ";\n" + temp_ans_d + ";\n" \
                          + str(questions_dct[(quest, ans_a, ans_b, ans_c, ans_d, correct_ans)]) + ";;;\n"
    return dict_as_string


# def dict_with_questions_as_string_new(questions_dct: Dict[Tuple[str, str, str, str, str, str], bool]) -> str:
#     dict_as_string = ""
#     for quest, ans_a, ans_b, ans_c, ans_d, correct_ans in questions_dct:
#         temp_ans_a = ans_a
#         temp_ans_b = ans_b
#         temp_ans_c = ans_c
#         temp_ans_d = ans_d
#         if ans_a[0] == correct_ans:
#             temp_ans_a += ";"
#         if ans_b[0] == correct_ans:
#             temp_ans_b += ";"
#         if ans_c[0] == correct_ans:
#             temp_ans_c += ";"
#         if ans_d[0] == correct_ans:
#             temp_ans_d += ";"
#         dict_as_string += quest + temp_ans_a + ";\n" + temp_ans_b + ";\n" + temp_ans_c + ";\n" + temp_ans_d + ";\n" \
#                           + str(questions_dct[(quest, ans_a, ans_b, ans_c, ans_d, correct_ans)]) + ";;;\n"
#     return dict_as_string
#
#
# def give_a_question_with_answers_as_tuple_new() -> Tuple[str, str, str, str, str, str]:
#     #                                               [question, ans A, ans B, ans C, ans D, correct ans]
#     file_with_questions_to_read = open("file_with_questions.txt", "r", encoding="windows-1250")
#     questions = {}
#     temp_question = ""
#     correct_answer = ""
#     answer_A = ""
#     answer_B = ""
#     answer_C = ""
#     answer_D = ""
#     for line in file_with_questions_to_read:
#         if line.strip()[-1] == ";":
#             if line.strip()[-2] == ';':
#                 if line.strip()[-3] == ';':
#                     if line.strip()[:-3] == "True":
#                         questions[(temp_question, answer_A, answer_B, answer_C, answer_D, correct_answer)] = True
#                     else:
#                         questions[(temp_question, answer_A, answer_B, answer_C, answer_D, correct_answer)] = False
#                     temp_question = ""
#                     correct_answer = ""
#                 else:
#                     correct_answer = line.strip()[0]
#                     if line.strip()[0] == "A":
#                         answer_A = line.strip()[:-2]
#                     if line.strip()[0] == "B":
#                         answer_B = line.strip()[:-2]
#                     if line.strip()[0] == "C":
#                         answer_C = line.strip()[:-2]
#                     if line.strip()[0] == "D":
#                         answer_D = line.strip()[:-2]
#             else:
#                 if line.strip()[0] == "A":
#                     answer_A = line.strip()[:-1]
#                 if line.strip()[0] == "B":
#                     answer_B = line.strip()[:-1]
#                 if line.strip()[0] == "C":
#                     answer_C = line.strip()[:-1]
#                 if line.strip()[0] == "D":
#                     answer_D = line.strip()[:-1]
#         else:
#             temp_question += line.strip() + "\n"
#
#     file_with_questions_to_read.close()
#     questions_to_choose: List[Tuple[str, str, str, str, str, str]] = filling_the_list_of_questions_to_choose(questions)
#     if len(questions_to_choose) == 0:
#         for question, ans_a, ans_b, ans_c, ans_d, correct_ans in questions.keys():
#             questions[(question, ans_a, ans_b, ans_c, ans_d, correct_ans)] = True
#         questions_to_choose = filling_the_list_of_questions_to_choose(questions)
#     the_chosen_question: Tuple[str, str, str, str, str, str] = rm.choice(questions_to_choose)
#     questions[the_chosen_question] = False
#     file_with_questions_to_write = open("file_with_questions.txt", "w",  encoding="windows-1250")
#     file_with_questions_to_write.write(dict_with_questions_as_string_new(questions))
#     file_with_questions_to_write.close()
#     q, a_A, a_B, a_C, a_D, c_a = the_chosen_question
#     question_ready_to_ask = q.replace(";", "")
#     final_answer_a = a_A.replace(";", "")
#     final_answer_b = a_B.replace(";", "")
#     final_answer_c = a_C.replace(";", "")
#     final_answer_d = a_D.replace(";", "")
#     return question_ready_to_ask, final_answer_a, final_answer_b, final_answer_c, final_answer_d, c_a

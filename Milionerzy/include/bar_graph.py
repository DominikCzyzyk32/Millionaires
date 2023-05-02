#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt


def draw_a_bar_graph(votes_for_A: int, votes_for_B: int, votes_for_C: int, votes_for_D: int):
    x = ["A", "B", "C", "D"]
    y = [votes_for_A, votes_for_B, votes_for_C, votes_for_D]

    plt.figure(" ")
    plt.bar(x, y, color='b')
    plt.title("Wynik głosowania")
    plt.grid(axis='y')
    plt.show()



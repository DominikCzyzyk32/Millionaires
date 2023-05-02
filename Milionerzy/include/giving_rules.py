#!/usr/bin/python
# -*- coding: utf-8 -*-


def give_rules() -> str:
    rules = ""
    file_with_rules = open("rules.txt", "r",  encoding="utf-8")
    for line in file_with_rules:
        rules += line + '\n'
    return rules

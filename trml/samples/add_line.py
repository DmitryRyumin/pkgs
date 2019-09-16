#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Добавление линии во весь экран

python trml/samples/add_line.py
"""

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
# Персональные
from trml.trml.shell import Shell  # Работа с Shell

# ######################################################################################################################
# Выполняем только в том случае, если файл запущен сам по себе
# ######################################################################################################################
if __name__ == "__main__":
    Shell.add_line()  # Добавление линии во весь экран

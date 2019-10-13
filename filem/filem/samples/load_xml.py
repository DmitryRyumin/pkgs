#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Загрузка XML файла

python filem/samples/load_xml.py --file путь_к_файлу_XML [--no_clear_shell]
"""

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
import argparse  # Парсинг аргументов и параметров командной строки

# Персональные
from trml.shell import Shell  # Работа с Shell
from filem.xml import Xml     # Работа с XML


# ######################################################################################################################
# Выполняем только в том случае, если файл запущен сам по себе
# ######################################################################################################################
def main():
    # Построение аргументов командой строки
    ap = argparse.ArgumentParser()

    # Добавление аргументов в парсер командной строки
    ap.add_argument('--file', required=True, help='Путь к файлу XML')
    ap.add_argument('--no_clear_shell', action='store_false', help='Не очищать консоль перед выполнением')

    args = vars(ap.parse_args())  # Преобразование списка аргументов командной строки в словарь

    # Очистка консоли перед выполнением
    if args['no_clear_shell'] is True:
        Shell.clear()  # Очистка консоли

    _xml = Xml()  # Работа с XML
    data = _xml.load(args['file'])  # Загрузка XML файла

    # Данные не загружены
    if data is None:
        return None

    _xml.recursive_data_display(data)  # Рекурсивное отображение данные из словаря

    print()  # Разрыв


if __name__ == "__main__":
    main()

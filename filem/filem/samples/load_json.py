#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Загрузка JSON файла

python filem/samples/load_json.py --file путь_к_файлу_JSON [--lines 0 --create --no_clear_shell]
"""

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
import argparse   # Парсинг аргументов и параметров командной строки
import itertools  # Итераторы зацикливания

# Персональные
from trml.shell import Shell  # Работа с Shell
from filem.json import Json   # Работа с JSON


# ######################################################################################################################
# Выполняем только в том случае, если файл запущен сам по себе
# ######################################################################################################################
def main():
    # Построение аргументов командой строки
    ap = argparse.ArgumentParser()

    ap.add_argument('--file', required=True, help='Путь к файлу JSON')
    ap.add_argument('--lines', type=int, default=0, help='Количество строк для отображения')
    ap.add_argument('--create', action='store_true', help='Создание файла в случае его отсутствия')
    ap.add_argument('--no_clear_shell', action='store_false', help='Не очищать консоль перед выполнением')

    args = vars(ap.parse_args())  # Преобразование списка аргументов командной строки в словарь

    # Очистка консоли перед выполнением
    if args['no_clear_shell'] is True:
        Shell.clear()  # Очистка консоли

    _json = Json()  # Работа с JSON
    data = _json.load(args['file'], args['create'])  # Загрузка JSON файла

    # JSON файл не загружен
    if data is None:
        return False

    # Количество строк для отображения меньше 0
    if args['lines'] < 0:
        return None

    # Количество строк для отображения больше значений в загружаемом файле или равно 0
    if args['lines'] is 0 or args['lines'] > len(data):
        args['lines'] = len(data)

    data_out = dict(itertools.islice(data.items(), args['lines']))  # Срез элементов словаря

    _json.recursive_data_display(data_out)  # Рекурсивное отображение данные из словаря

    print()  # Разрыв


if __name__ == "__main__":
    main()

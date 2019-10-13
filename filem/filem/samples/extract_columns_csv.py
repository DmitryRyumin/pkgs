#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Извлечение указанных столбцов из CSV файла

python filem/samples/extract_columns_csv.py --file путь_к_файлу_CSV [--lines 0 --columns 0 --no_clear_shell]
"""

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
import argparse  # Парсинг аргументов и параметров командной строки

# Персональные
from trml.shell import Shell  # Работа с Shell
from filem.csv import Csv     # Работа с CSV


# ######################################################################################################################
# Выполняем только в том случае, если файл запущен сам по себе
# ######################################################################################################################
def main():
    # Построение аргументов командой строки
    ap = argparse.ArgumentParser()

    # Добавление аргументов в парсер командной строки
    ap.add_argument('--file', required=True, help='Путь к файлу CSV')
    ap.add_argument('--lines', type=int, default=0, help='Количество строк для отображения')
    ap.add_argument('--columns', type=int, nargs='+', default=[0],
                    help='Список номеров столбцов для извлечения')
    ap.add_argument('--no_clear_shell', action='store_false', help='Не очищать консоль перед выполнением')

    args = vars(ap.parse_args())  # Преобразование списка аргументов командной строки в словарь

    # Очистка консоли перед выполнением
    if args['no_clear_shell'] is True:
        Shell.clear()  # Очистка консоли

    _csv = Csv()  # Работа с CSVs
    df = _csv.load(args['file'])  # Загрузка CSV файла

    # Данные не загружены
    if df is None:
        return None

    # Количество строк для отображения меньше 0
    if args['lines'] < 0:
        return None

    # Количество строк для отображения больше значений в загружаемом файле или равно 0
    if args['lines'] is 0 or args['lines'] > len(df):
        args['lines'] = len(df)

    # Извлечение указанных столбцов из CSV файла
    data = _csv.extract_columns(df, args['columns'])

    if data is None:
        return None

    print(data[:args['lines']])


if __name__ == "__main__":
    main()

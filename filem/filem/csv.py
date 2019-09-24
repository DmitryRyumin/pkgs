#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Работа с CSV
"""

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
import os            # Работа с файловой системой
import pandas as pd  # Обработка и анализ данных

from datetime import datetime  # Работа со временем

# Персональные
from filem.file_manager import FileManager  # Работа с файлами


# ######################################################################################################################
# Сообщения
# ######################################################################################################################
class Messages(FileManager):
    """Класс для сообщений"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()  # Выполнение конструктора из суперкласса

        self._load_data = '[{}] Загрузка данных из файла "{}" ...'

        self._extract_all_columns = '[{}] Извлечение данных из всех столбцов "{}" ...'
        self._extract_columns = '[{}] Извлечение данных из столбцов "{}" ...'
        self._error_extract_columns = '[{}{}{}] Указаны неверные столбцы для извлечения ...'


# ######################################################################################################################
# Работа с CSV
# ######################################################################################################################
class Csv(Messages):
    """Класс для работы с CSV"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()  # Выполнение конструктора из суперкласса

    # ------------------------------------------------------------------------------------------------------------------
    #  Внешние методы
    # ------------------------------------------------------------------------------------------------------------------

    # Загрузка CSV файла
    def load(self, file,  out = True):
        """
        Загрузка CSV файла

        (str [, bool]) -> pandas.core.frame.DataFrame or None

        Аргументы:
            file - Путь к файлу CSV
            out  - Печатать процесс выполнения

        Возвращает: pandas.core.frame.DataFrame or None
        """

        # Проверка аргументов
        if type(file) is not str or type(out) is not bool:
            # Вывод сообщения
            if out is True:
                print(self._invalid_arguments.format(
                    self._red, datetime.now().strftime(self._format_time), self._end,
                    __class__.__name__ + '.' + self.load.__name__
                ))

            return None

        # Поиск CSV файла не удался
        if super().search_file(file, 'csv', out) is False:
            return None

        # Вывод сообщения
        if out is True:
            print(self._load_data.format(datetime.now().strftime(self._format_time), os.path.basename(file)))

        # Чтение данных из csv файла
        # В некоторых случаях необходимо указывать: sep='delimiter', engine='python'
        df = pd.read_csv(file, header = None, sep=',', engine='c')

        return df  # Результат

    # Извлечение указанных столбцов из CSV файла
    def extract_columns(self, df, columns, out = True):
        """
        Выбор указанных столбцов из pandas.core.frame.DataFrame

        (pandas.core.frame.DataFrame, list [, bool]) -> np.ndarray or None

        Аргументы:
            df      - pandas.core.frame.DataFrame полученный из CSV файла
            columns - Список номеров столбцов для извлечения
            out     - Печатать процесс выполнения

        Возвращает: np.ndarray выбранных стоблцов из pandas.core.frame.DataFrame or None
        """

        # Проверка аргументов
        if type(df) is not pd.core.frame.DataFrame or type(columns) is not list or len(columns) is 0 \
                or type(out) is not bool or all(isinstance(item, int) for item in columns) is False:
            # Вывод сообщения
            if out is True:
                print(self._invalid_arguments.format(
                    self._red, datetime.now().strftime(self._format_time), self._end,
                    __class__.__name__ + '.' + self.extract_columns.__name__
                ))

            return None

        # Извлечение всех столбцов
        if len(columns) is 1 and columns[0] is 0:
            self._extract_columns = self._extract_all_columns

            columns = list(range(1, df.shape[1] + 1))  # Все столбцы

        # Вывод сообщения
        if out is True:
            print(self._extract_columns.format(
                datetime.now().strftime(self._format_time), ', '.join(str(v) for v in columns)
            ))

        # Отнять у всех номеров столбцов
        columns = [v - 1 for v in columns]

        # Указаны неверные столбцы для извлечения
        for v in columns:
            if v >= len(df.columns) or v < 0:
                # Вывод сообщения
                if out is True:
                    print(self._error_extract_columns.format(
                        self._red, datetime.now().strftime(self._format_time), self._end
                    ))

                return None

        # Выбрать необходимые столбцы без заголовочной строки
        data = df.loc[:, df.index.intersection(columns)].values[1:]

        return data  # Результат

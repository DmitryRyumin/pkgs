#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Работа с JSON
"""

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
import os    # Работа с файловой системой
import json  # Кодирование и декодирование данные в удобном формате

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

        self._config_load = '[{}] Загрузка данных из файла "{}" ...'
        self._invalid_file = '[{}{}{}] Необходимые значения в файле не найдены ...'
        self._config_empty = '[{}{}{}] Файл пуст ...'


# ######################################################################################################################
# Работа с JSON
# ######################################################################################################################
class Json(Messages):
    """Класс для работы с JSON"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()  # Выполнение конструктора из суперкласса

    # ------------------------------------------------------------------------------------------------------------------
    #  Внешние методы
    # ------------------------------------------------------------------------------------------------------------------

    # Загрузка JSON файла
    def load(self, file, create = False, out = True):
        """
        Загрузка JSON файла

        (str [, bool, bool]) -> dict or None

        Аргументы:
            file   - Путь к файлу JSON
            create - Создание файла JSON в случае его отсутствия
            out    - Печатать процесс выполнения

        Возвращает словарь из json файла или None
        """

        # Проверка аргументов
        if type(file) is not str or type(create) is not bool or type(out) is not bool:
            # Вывод сообщения
            if out is True:
                print(self._invalid_arguments.format(
                    self._red, datetime.now().strftime(self._format_time), self._end,
                    __class__.__name__ + '.' + self.load.__name__
                ))

            return None

        # Поиск JSON файла не удался
        if super().search_file(file, 'json', create, out) is False:
            return None

        # Вывод сообщения
        if out is True:
            print(self._config_load.format(datetime.now().strftime(self._format_time), os.path.basename(file)))

        # Открытие файла
        with open(file, mode = 'r', encoding = 'utf-8') as json_data_file:
            try:
                config = json.load(json_data_file)
            except json.JSONDecodeError:
                # Вывод сообщения
                if out is True:
                    print(self._invalid_file.format(self._red, datetime.now().strftime(self._format_time), self._end))

                return None

        # Файл пуст
        if len(config) == 0:
            # Печать
            if out is True:
                print(self._config_empty.format(self._red, datetime.now().strftime(self._format_time), self._end))

            return None

        return config  # Результат

    # Рекурсивное отображение данные из JSON файла
    def recursive_data_display(self, data, cnt = 1, out = True):
        """
        Рекурсивное отображение данные из словаря

        (dict [, int, bool]) -> None

        Аргументы:
            data - Словарь
            cnt  - Рекурсивный счетчик
            out  - Печатать процесс выполнения

        Возвращает None
        """

        # Проверка аргументов
        if type(data) is not dict or len(data) is 0 or type(cnt) is not int or cnt < 0 or type(out) is not bool:
            # Вывод сообщения
            if out is True:
                print(self._invalid_arguments.format(
                    self._red, datetime.now().strftime(self._format_time), self._end,
                    __class__.__name__ + '.' + self.recursive_data_display.__name__
                ))

            return None

        # Вывод сообщениЙ не нужен
        if out is False:
            return None

        # Значения словаря файла
        for key, val in data.items():
            # Значение внутри словаря
            if type(val) is not dict:
                # Обработка значений
                val = str(val) if type(val) is not list else ', '.join(str(v) for v in val)

                print(('\t' * cnt) + '"' + key + '" - ' + val)
            else:
                print(('\t' * cnt) + '"' + key + '":')

                # Рекурсивный вызов функции
                self.recursive_data_display(val, cnt + 1)

        return None

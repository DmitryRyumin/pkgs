#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Работа с XML
"""

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
import os                          # Работа с файловой системой
import xml.parsers.expat as expat  # Анализ XML документа
import xmltodict                   # Преобразование XML документа в словарь
import json                        # Кодирование и декодирование данные в удобном формате

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


# ######################################################################################################################
# Работа с JSON
# ######################################################################################################################
class Xml(Messages):
    """Класс для работы с XML"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()  # Выполнение конструктора из суперкласса

    # ------------------------------------------------------------------------------------------------------------------
    #  Внешние методы
    # ------------------------------------------------------------------------------------------------------------------

    # Загрузка XML файла
    def load(self, file, out = True):
        """
        Загрузка XML файла

        (str [, bool]) -> dict or None

        Аргументы:
            file   - Путь к файлу XML
            out    - Печатать процесс выполнения

        Возвращает словарь из XML файла или None
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

        # Поиск XML файла не удался
        if super().search_file(file, 'xml', False, out) is False:
            return None

        # Вывод сообщения
        if out is True:
            print(self._config_load.format(datetime.now().strftime(self._format_time), os.path.basename(file)))

        # Открытие файла
        with open(file, encoding = 'utf-8') as fd:
            try:
                res = json.loads(json.dumps(xmltodict.parse(fd.read())))  # Парсинг XML документа
            except expat.ExpatError:
                # Вывод сообщения
                if out is True:
                    print(self._invalid_file.format(self._red, datetime.now().strftime(self._format_time), self._end))

                return None

        return res  # Результат

    # Рекурсивное отображение данные из XML файла
    def recursive_data_display(self, data, cnt = 1, out = True):
        """
        Рекурсивное отображение данные из словаря

        (dict [, int, bool]) -> None

        Аргументы:
            data   - Словарь или список
            cnt    - Рекурсивный счетчик
            out    - Печатать процесс выполнения

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

        # Значения словаря файла
        for key, val in data.items():
            print(('\t' * cnt) + '"' + key + '": ')

            # Значение внутри списка
            if type(val) is list:
                cnt += 1

                for v in val:
                    tmp = ''

                    # Значения словаря файла
                    for k_temp, v_temp in v.items():
                        tmp += ' "' + k_temp + '" - ' + v_temp + ';'

                    print(('\t' * cnt) + tmp[:-1])

            # Значение внутри словаря
            if type(val) is dict:
                # Рекурсивный вызов функции
                self.recursive_data_display(val, cnt + 1)

        return None

        res = ''

        # Список
        if type(data) is list:
            # Значения списка файла
            for val in data:
                # Значение внутри словаря
                if type(val) is dict:
                    # Рекурсивный вызов функции
                    self.recursive_data_display(val, cnt, parent)

        # Список
        if type(data) is dict:
            # Значения словаря файла
            for key, val in data.items():
                parent = key  # Родительский ключ

                # Значение внутри словаря
                if type(val) is dict or type(val) is list:
                    # Вывод сообщения
                    if out is True:
                        res += ('\t' * cnt) + '"' + key + '":'

                    # Рекурсивный вызов функции
                    self.recursive_data_display(val, cnt + 1)
                else:
                    # Обработка значений
                    val = str(val) if type(val) is not list else ', '.join(str(v) for v in val)

                    # Вывод сообщения
                    if out is True:
                        res += parent + ' "' + key + '" - ' + val

        print(res)

        return None
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Работа с файлами
"""

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
import os      # Работа с файловой системой
import shutil  # Набор функций высокого уровня для обработки файлов, групп файлов, и папок

from datetime import datetime  # Работа со временем

# Персональные
from core2pkgs import config as cfg  # Глобальный файл настроек


# ######################################################################################################################
# Сообщения
# ######################################################################################################################
class Messages(cfg.Messages):
    """Класс для сообщений"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()  # Выполнение конструктора из суперкласса

        self._file_load = '[{}] Поиск "{}" файла ...'
        self._file_name = '[{}{}{}] Необходимо указать название {} файла ...'
        self._dir_found = '[{}{}{}] Передана директория за место файла ...'
        self._file_not_found = '[{}{}{}] Файл "{}" не найден ...'
        self._file_not_found_create = '[{}] Файл "{}" не найден, но был создан ...'
        self._wrong_extension = '[{}{}{}] Расширение файла должно быть "{}" ...'

        self._clear_folder = '[{}] Очистка директории "{}" ...'
        self._clear_folder_not_found = '[{}{}{}] Директория "{}" не найдена ...'

        self._load_data = '[{}] Загрузка данных из файла "{}" ...'


# ######################################################################################################################
# Работа с файлами
# ######################################################################################################################
class FileManager(Messages):
    """Класс для работы с файлами"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()  # Выполнение конструктора из суперкласса

    # ------------------------------------------------------------------------------------------------------------------
    #  Внешние методы
    # ------------------------------------------------------------------------------------------------------------------

    # Поиск файла
    def search_file(self, file, extension, create = False, out = True):
        """
        Поиск файла

        (str, str [, bool, bool]) -> bool

        Аргументы:
            file      - Путь к файлу
            extension - Расширение файла
            create    - Создание файла в случае его отсутствия
            out       - Печатать процесс выполнения

        Возвращает True если файл найден, в обратном случае False
        """

        # Проверка аргументов
        if type(file) is not str or type(extension) is not str or type(create) is not bool or type(out) is not bool:
            # Вывод сообщения
            if out is True:
                print(self._invalid_arguments.format(
                    self.red, datetime.now().strftime(self._format_time), self.end,
                    __class__.__name__ + '.' + self.search_file.__name__
                ))

            return False

        # Файл не передан
        if not file:
            # Вывод сообщения
            if out is True:
                print(self._file_name.format(
                    self.red, datetime.now().strftime(self._format_time), self.end, extension.upper()
                ))

            return False

        # Передана директория
        if os.path.isdir(file) is True:
            # Вывод сообщения
            if out is True:
                print(self._dir_found.format(self.red, datetime.now().strftime(self._format_time), self.end))

            return False

        # Вывод сообщения
        if out is True:
            print(self._file_load.format(datetime.now().strftime(self._format_time), os.path.basename(file)))

        _, ext = os.path.splitext(file)  # Расширение файла

        if ext.replace('.', '') != extension:
            # Вывод сообщения
            if out is True:
                print(self._wrong_extension.format(
                    self.red, datetime.now().strftime(self._format_time), self.end, extension
                ))

            return False

        # Файл не найден
        if os.path.isfile(file) is False:
            # Создание файла
            if create is True:
                # Создание JSON файла
                open(file, 'a', encoding = 'utf-8').close()

                # Вывод сообщения
                if out is True:
                    print(self._file_not_found_create.format(
                        datetime.now().strftime(self._format_time), os.path.basename(file)
                    ))

                return False

            # Вывод сообщения
            if out is True:
                print(self._file_not_found.format(
                    self.red, datetime.now().strftime(self._format_time), self.end, os.path.basename(file)
                ))
            return False

        return True  # Результат

    # Очистка директории
    def clear_folder(self, path, out = True):
        """
        Очистка директории

        (str, [, bool]) -> bool

        Аргументы:
            path - Путь к директории
            out  - Печатать процесс выполнения

        Возвращает True если директория очищена, в обратном случае False
        """

        # Проверка аргументов
        if type(path) is not str or not path or type(out) is not bool:
            # Вывод сообщения
            if out is True:
                print(self._invalid_arguments.format(
                    self.red, datetime.now().strftime(self._format_time), self.end,
                    __class__.__name__ + '.' + self.clear_folder.__name__
                ))

            return False

        # Вывод сообщения
        if out is True:
            print(self._clear_folder.format(datetime.now().strftime(self._format_time), path))

        # Каталог с файлами найден
        if os.path.exists(path):
            # Очистка
            for filename in os.listdir(path):
                filepath = os.path.join(path, filename)
                try:
                    shutil.rmtree(filepath)
                except OSError:
                    os.remove(filepath)
        else:
            # Вывод сообщения
            if out is True:
                print(self._clear_folder_not_found.format(
                    self.red, datetime.now().strftime(self._format_time), self.end, path
                ))

            return False

        return True  # Результат

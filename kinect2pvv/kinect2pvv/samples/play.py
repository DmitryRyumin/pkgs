#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Воспроизведение видеоданных из сенсора Kinect 2

python kinect2pvv/samples/play.py [--config путь_к_конфигурационному_файлу --automatic_update
    --frames_to_update 25 --no_clear_shell]
"""

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
from datetime import datetime                           # Работа со временем
from types import ModuleType, FunctionType, MethodType  # Проверка объектов на модуль, метод, функцию

import sys

sys.path.append('C:/Users/NUC204/Desktop/GitHub/pkgs/kinect2pvv')

# Персональные
import kinect2pvv  # Воспроизведение видеоданных из сенсора Kinect 2

from pvv.samples import play                # Пример воспроизведения фото/видео данных
from kinect2pvv.viewer import KinectViewer  # Воспроизведение видеоданных из сенсора Kinect 2
from kinect2pvv import configs              # Конфигурационные файлы


# ######################################################################################################################
# Сообщения
# ######################################################################################################################
class Messages(play.Run):
    """Класс для сообщений"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()  # Выполнение конструктора из суперкласса


# ######################################################################################################################
# Выполняем только в том случае, если файл запущен сам по себе
# ######################################################################################################################
class Run(Messages):
    """Класс для воспроизведения видеоданных из сенсора Kinect 2"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()  # Выполнение конструктора из суперкласса

        # Текущие кадры
        self._curr_frame = None  # Цветной кадр
        self._curr_frame_depth = None  # Карта глубины
        self._curr_frame_infrared = None  # Инфракрасный кадр

        self._kinect_viewer = KinectViewer()  # Воспроизведение видеоданных из сенсора Kinect 2

    # ------------------------------------------------------------------------------------------------------------------
    #  Внутренние методы
    # ------------------------------------------------------------------------------------------------------------------

    # Построение аргументов командной строки
    def _build_args(self, conv_to_dict = True):
        """
        Построение аргументов командной строки

        ([bool]) -> None or dict

        Аргументы:
           conv_to_dict - Преобразование списка аргументов командной строки в словарь

        Возвращает: dict если парсер командной строки окончательный, в обратном случае None
        """

        super()._build_args(False)  # Выполнение функции из суперкласса

        if conv_to_dict is True:
            return vars(self._ap.parse_args())  # Преобразование списка аргументов командной строки в словарь

    # Проверка JSON файла настроек на валидность
    def _valid_json_config(self, config, out = True):
        """
        Проверка настроек JSON на валидность

        (dict [, bool]) -> bool

        Аргументы:
           config - Словарь из JSON файла
           out    - Печатать процесс выполнения

        Возвращает: True если файл валидный, в обратном случае False
        """

        # Переопределение значений из конфигурационного файла (только те которые не нужны на данном этапе)
        config['repeat'] = False  # Повторение воспроизведения видеопотока
        config['clear_image_buffer'] = True  # Очистка буфера с изображением

        # Выполнение функции из суперкласса с отрицательным результатом
        if super()._valid_json_config(config, out) is False:
            return False

        all_layer = 2  # Общее количество разделов
        curr_valid_layer = 0  # Валидное количество разделов

        # Проход по всем разделам конфигурационного файла
        for key, val in config.items():
            # 1. Отображение карты глубины
            # 2. Отображение инфракрасного кадра
            if key == 'show_depth' or key == 'show_infrared':
                # Проверка значения
                if type(val) is not bool:
                    continue

                curr_valid_layer += 1

            # Отображение карты глубины или инфракрасного кадра
            if (('show_depth' in config and config['show_depth'] is True)
                    or ('show_infrared' in config and config['show_infrared'] is True)):
                # Размер карты глубины и инфракрасного кадра для масштабирования
                if key == 'resize_depth_ir':
                    # Добавляем:
                    #     Размер карты глубины и инфракрасного кадра для масштабирования
                    all_layer += 1

                    all_layer_2 = 1  # Общее количество подразделов в текущем разделе
                    curr_valid_layer_2 = 0  # Валидное количество подразделов в текущем разделе

                    # Проверка значения
                    if type(val) is not dict or len(val) is 0:
                        continue

                    # Проход по всем подразделам текущего раздела
                    for k, v in val.items():
                        # Проверка значения
                        if type(v) is not int or v < 0 or v > 512:
                            continue

                        # Ширина изображения для масштабирования
                        if k == 'width':
                            curr_valid_layer_2 += 1

                    if all_layer_2 == curr_valid_layer_2:
                        curr_valid_layer += 1

                # Базовые координаты карты глубины и инфракрасного кадра относительно верхнего правого угла
                if key == 'labels_base_coords_depth_ir':
                    # Добавляем:
                    #     Базовые координаты карты глубины и инфракрасного кадра относительно верхнего правого угла
                    all_layer += 1

                    all_layer_2 = 2  # Общее количество подразделов в текущем разделе
                    curr_valid_layer_2 = 0  # Валидное количество подразделов в текущем разделе

                    # Проверка значения
                    if type(val) is not dict or len(val) is 0:
                        continue

                    # Проход по всем подразделам текущего раздела
                    for k, v in val.items():
                        # Проверка значения
                        if type(v) is not int or v < 0 or v > 100:
                            continue

                        # 1. Право
                        # 2. Вверх
                        if k == 'right' or k == 'top':
                            curr_valid_layer_2 += 1

                    if all_layer_2 == curr_valid_layer_2:
                        curr_valid_layer += 1

            # Отображение карты глубины или инфракрасного кадра
            if ('show_depth' in config and config['show_depth'] is True
                    and 'show_infrared' in config and config['show_infrared'] is True):
                # Расстояние между картой глубины и инфракрасным кадром
                if key == 'distance_between_depth_ir':
                    # Добавляем:
                    #     Расстояние между картой глубины и инфракрасным кадром
                    all_layer += 1

                    # Проверка значения
                    if type(val) is not int or val < 0 or val > 50:
                        continue

                    curr_valid_layer += 1

        # Сравнение общего количества разделов и валидных разделов в конфигурационном файле
        if all_layer != curr_valid_layer:
            # Вывод сообщения
            if out is True:
                print(self._invalid_file.format(
                    self.red, datetime.now().strftime(self._format_time), self.end
                ))

            return False

        return True  # Результат

    # Загрузка и проверка конфигурационного файла
    def _load_config_json(self, resources = configs, out = True):
        """
        Загрузка и проверка конфигурационного файла

        ([module, bool]) -> bool

        Аргументы:
            resources - Модуль с ресурсами
            out       - Печатать процесс выполнения

        Возвращает: True если файл загружен и валиден, в обратном случае False
        """

        # Выполнение функции из суперкласса с отрицательным результатом
        if super()._load_config_json(resources, out) is False:
            return False

        return True

    # Автоматическая проверка конфигурационного файла в момент работы программы
    def _update_config_json(self, set_window_name = True):
        """
        Автоматическая проверка конфигурационного файла в момент работы программы

        ([bool]) -> bool

        Аргументы:
            set_window_name - Установка имени окна

        Возвращает: True если аргументы переданы верно, в обратном случае False
        """

        # Выполнение функции из суперкласса с отрицательным результатом
        if super()._update_config_json(set_window_name) is False:
            return False

        return True

    # Захват фото/видеоданных
    def _grab_data(self, out = True):
        """
        Захват фото/видеоданных

        ([bool]) -> bool

        Аргументы:
           out - Печатать процесс выполнения

        Возвращает: True если захват фото/видеоданных произведен, в обратном случае False
        """

        # Запуск Kinect 2
        if self._kinect_viewer.start(out) is False:
            return False

        return True

    # Получение цветного кадра из Kinect 2
    def _get_color_frame(self):
        """
        Получение цветного кадра из Kinect 2
        """

        self._curr_frame = self._kinect_viewer.get_color_frame()  # Получение цветного кадра из Kinect 2

    # Получение карты глубины из Kinect 2
    def _get_depth_frame(self):
        """
        Получение карты глубины из Kinect 2
        """

        self._curr_frame_depth = self._kinect_viewer.get_depth_frame()  # Получение карты глубины из Kinect 2

        # Изменение размеров изображения карты глубины не стандартные
        if self._args['resize_depth_ir']['width'] is not 0:
            # Изменение размера карты глубины
            self._curr_frame_depth = self._viewer.resize_frame(
                self._curr_frame_depth, self._args['resize_depth_ir']['width'], 0
            )

            # Изображение уменьшилось
            if self._curr_frame_depth is not None:
                self._curr_frame_depth, _, _ = self._curr_frame_depth

        # Правый отступ для карты глубины
        right_margin = self._curr_frame.shape[1] - self._curr_frame_depth.shape[1]\
                       - self._args['labels_base_coords_depth_ir']['right']

        # Вставка карты глубины в основное изображение
        self._curr_frame[
            self._args['labels_base_coords_depth_ir']['top']:
                self._args['labels_base_coords_depth_ir']['top'] + self._curr_frame_depth.shape[0],
            right_margin: right_margin + self._curr_frame_depth.shape[1]] = self._curr_frame_depth

    # Получение инфракрасного кадра из Kinect 2
    def _get_infrared_frame(self):
        """
        Получение инфракрасного кадра из Kinect 2
        """

        # Получение инфракрасного кадра из Kinect 2
        self._curr_frame_infrared = self._kinect_viewer.get_infrared_frame()

        # Изменение размеров изображения карты глубины не стандартные
        if self._args['resize_depth_ir']['width'] is not 0:
            # Изменение размера карты глубины
            self._curr_frame_infrared = self._viewer.resize_frame(
                self._curr_frame_infrared, self._args['resize_depth_ir']['width'], 0
            )

            # Изображение уменьшилось
            if self._curr_frame_infrared is not None:
                self._curr_frame_infrared, _, _ = self._curr_frame_infrared

        # Правый отступ для карты глубины
        right_margin = self._curr_frame.shape[1] - self._curr_frame_infrared.shape[1]\
                       - self._args['labels_base_coords_depth_ir']['right']

        # Верхний отступ для инфракрасного кадра
        top_margin = self._args['labels_base_coords_depth_ir']['top']

        # Отображение карты глубины
        if self._args['show_depth'] is True:
            top_margin += self._curr_frame_depth.shape[0] + self._args['distance_between_depth_ir']

        # Вставка карты глубины в основное изображение
        self._curr_frame[
            top_margin: top_margin + self._curr_frame_infrared.shape[0],
            right_margin: right_margin + self._curr_frame_infrared.shape[1]] = self._curr_frame_infrared

    # Операции над кадром
    def _frame_o(self):
        """
        Операции над кадром
        """

        # Отображение карты глубины
        if self._args['show_depth'] is True:
            self._get_depth_frame()  # Получение карты глубины из Kinect 2

        # Отображение инфракрасного кадра
        if self._args['show_infrared'] is True:
            self._get_infrared_frame()  # Получение инфракрасного кадра из Kinect 2

    # Нанесение уведомления на кадр
    def _err_notification(self, condition, text, out = True):
        """
        Нанесение уведомления на кадр

        (str [, bool, bool]) -> None

        Аргументы:
           condition - Условие
           text      - Текст уведомления если условие True
           out       - Печатать процесс выполнения

        Возвращает: True если уведомление не применено, в обратном случае False
        """

        # Выполнение функции из суперкласса с отрицательным результатом
        if super()._err_notification(condition, text, out) is False:
            return False

        return True

    # Циклическое получение кадров из видеопотока
    def _loop(self, other_source = None, func = None, out = True):
        """
        Циклическое получение кадров из фото/видеопотока

        ([bool]) -> bool

        Аргументы:
           other_source - Ресурс извлечения фото/видеоданных
           func         - Функция или метод
           out          - Печатать процесс выполнения

        Возвращает: True если получение кадров осуществляется, в обратном случае False
        """

        # Выполнение функции из суперкласса с отрицательным результатом
        if super()._loop(self._get_color_frame, self._frame_o, out) is False:
            return False

        return True

    # ------------------------------------------------------------------------------------------------------------------
    #  Внешние методы
    # ------------------------------------------------------------------------------------------------------------------

    # Запуск
    def run(self, metadata = kinect2pvv, resources = configs, start = True, out = True):
        """
        Запуск

        ([module, module, bool, bool]) -> None

        Аргументы:
           metadata  - Модуль из которого необходимо извлечь информацию
           resources - Модуль с ресурсами
           start     - Запуск процесса извлечения изображений
           out       - Печатать процесс выполнения
        """

        # Выполнение функции из суперкласса с отрицательным результатом
        if super().run(metadata, resources, False, out) is False:
            return False

        # Запуск процесса извлечения изображений
        if start is True:
            self._viewer.set_loop(self._loop)  # Циклическая функция извлечения изображений
            self._viewer.start()  # Запуск


def main():
    run = Run()

    run.run()


if __name__ == "__main__":
    main()

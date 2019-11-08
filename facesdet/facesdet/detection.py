#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Поиск лиц
"""

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
import os             # Работа с файловой системой
import numpy as np    # Научные вычисления
import cv2            # Алгоритмы компьютерного зрения
import dlib           # Распознавание лиц
import pkg_resources  # Работа с ресурсами внутри пакетов

from datetime import datetime  # Работа со временем
from decimal import Decimal, ROUND_HALF_UP  # Округление по математическому закону

# Персональные
from core2pkgs import config as cfg         # Глобальный файл настроек
from filem.file_manager import FileManager  # Работа с файлами


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

        self._face_detect = '[{}] Поиск лиц ...'
        self._face_found = '[{}] Всего найдено лиц: {} ...'
        self._face_not_found = '[{}{}{}] Лица не найдены ...'
        self._load_model = '[{}] Загрузка модели "{}" ...'
        self._model_not_load = '[{}{}{}] Модель "{}" не загружена ...'
        self._precent = '{:.2f}%'


# ######################################################################################################################
# Поиск лиц
# ######################################################################################################################
class Detection(Messages):
    """Класс для поиска лиц"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(
            self,
            rectangle_color = (0, 255, 0),           # Цвет рамки прямоугольника с лицами
            rectangle_thickness = 2,                 # Толщина рамки прямоугольника с лицами
            precent_scale = 0.45,                    # Коэффициент масштабирования шрифта с процентами
            precent_thickness = 1,                   # Толщина линии шрифта (проценты)
            precent_text_color = (255, 255, 255),    # Цвет текста процентов
            precent_background_color = (0, 0, 255),  # Цвет фона процентов
            precent_padding = 5,                     # Внутренний отступ для процентов
            precent_margin_bottom = 5                # Внешний нижний отступ для процентов
    ):
        super().__init__()  # Выполнение конструктора из суперкласса

        self.title_en = 'Method'  # Название метода на английском
        self.title_ru = 'Метод'   # Назавание метода на русском

        # Необходимые расширения для моделей
        self._required_extension_models = (
            'xml',  # Поиск лиц с помощью метода Виолы-Джонса в OpenCV
            'pbtxt', 'pb',  # Поиск лиц с помощью глубокого обучения в OpenCV (TensorFlow)
            'prototxt', 'caffemodel',  # Поиск лиц с помощью глубокого обучения в OpenCV (Caffe)
            'dat'  # Поиск лиц с помощью Convolutional Neural Network в Dlib
        )

        self._dnn = ('tf', 'caffe')  # Модели нейронной сети

        # Данные методов
        self._packages_functions = {
            'opencv_haar': {
                'ru': 'Поиск лиц с помощью метода Виолы-Джонса в OpenCV',
                'en': 'Faces detection with method Viola-Jones in OpenCV'
            },
            'opencv_dnn': {
                'ru': 'Поиск лиц с помощью глубокого обучения в OpenCV',
                'en': 'Faces detection with deep learning in OpenCV'
            },
            'dlib_hog': {
                'ru': 'Поиск лиц с помощью функций HoG и SVM в Dlib',
                'en': 'Faces detection with HoG and SVM in Dlib'
            },
            'dlib_cnn': {
                'ru': 'Поиск лиц с помощью Convolutional Neural Network в Dlib',
                'en': 'Faces detection with Convolutional Neural Network in Dlib'
            }
        }

        # Названия моделей и их конфигурационных файлов
        self._path_to_files_models = {
            'opencv_haar': {
                'path_to_model': 'haarcascade_frontalface_default.xml'
            },
            'opencv_dnn': {
                'tf': {
                    'path_to_model': 'opencv_face_detector_uint8.pb',
                    'path_to_config_model': 'opencv_face_detector.pbtxt'
                },
                'caffe': {
                    'path_to_model': 'res10_300x300_ssd_iter_140000_fp16.caffemodel',
                    'path_to_config_model': 'deploy.prototxt'
                }
            },
            'dlib_cnn': {
                'path_to_model': 'mmod_human_face_detector.dat',
            }
        }

        self._model = None  # Модель

        self._file_manager = FileManager()  # Работа с файлами

        self.rectangle_color = rectangle_color  # Цвет рамки прямоугольника с лицами

        self.rectangle_thickness = rectangle_thickness  # Толщина рамки прямоугольника с лицами

        self.precent_scale = precent_scale  # Коэффициент масштабирования шрифта с процентами
        self.precent_thickness = precent_thickness  # Толщина линии шрифта (проценты)
        self.precent_text_color = precent_text_color  # Цвет текста процентов
        self.precent_background_color = precent_background_color  # Цвет фона процентов
        self.precent_padding = precent_padding  # Внутренний отступ для процентов
        self.precent_margin_bottom = precent_margin_bottom  # Внешний нижний отступ для процентов

        self._path_to_models = pkg_resources.resource_filename('facesdet', 'models')  # Путь к моделям

    # ------------------------------------------------------------------------------------------------------------------
    # Свойства
    # ------------------------------------------------------------------------------------------------------------------

    # Получение названия метода на английском
    @property
    def title_en(self):
        return self._title_en

    # Установка названия метода на английском
    @title_en.setter
    def title_en(self, name):
        self._title_en = name

    # Получение названия метода на русском
    @property
    def title_ru(self):
        return self._title_ru

    # Установка названия метода на русском
    @title_ru.setter
    def title_ru(self, name):
        self._title_ru = name

    # Получение модели
    @property
    def model(self):
        return self._model

    # Получение названий методов
    @property
    def packages_functions(self):
        return self._packages_functions

    # Получение цвета рамки прямоугольника с лицами
    @property
    def rectangle_color(self):
        return self._rectangle_color

    # Установка цвета рамки прямоугольника с лицами
    @rectangle_color.setter
    def rectangle_color(self, color):
        self._rectangle_color = color

    # Получение толщины рамки прямоугольника с лицами
    @property
    def rectangle_thickness(self):
        return self._rectangle_thickness

    # Установка толщины рамки прямоугольника с лицами
    @rectangle_thickness.setter
    def rectangle_thickness(self, thickness):
        self._rectangle_thickness = thickness

    # Получение коэффициента масштабирования шрифта с процентами
    @property
    def precent_scale(self):
        return self._precent_scale

    # Установка коэффициента масштабирования шрифта с процентами
    @precent_scale.setter
    def precent_scale(self, scale):
        self._precent_scale = scale

    # Получение толщины линии шрифта (проценты)
    @property
    def precent_thickness(self):
        return self._precent_thickness

    # Установка толщины линии шрифта (проценты)
    @precent_thickness.setter
    def precent_thickness(self, thickness):
        self._precent_thickness = thickness

    # Получение цвета текста процентов
    @property
    def precent_text_color(self):
        return self._precent_text_color

    # Установка цвета текста процентов
    @precent_text_color.setter
    def precent_text_color(self, color):
        self._precent_text_color = color

    # Получение цвета фона процентов
    @property
    def precent_background_color(self):
        return self._precent_background_color

    # Установка цвета фона процентов
    @precent_background_color.setter
    def precent_background_color(self, color):
        self._precent_background_color = color

    # Получение внутреннего отступа для процентов
    @property
    def precent_padding(self):
        return self._precent_padding

    # Установка внутреннего отступа для процентов
    @precent_padding.setter
    def precent_padding(self, padding):
        self._precent_padding = padding

    # Получение внешнего нижнего отступа для процентов
    @property
    def precent_margin_bottom(self):
        return self._precent_margin_bottom

    # Установка внешнего нижнего отступа для процентов
    @precent_margin_bottom.setter
    def precent_margin_bottom(self, margin_bottom):
        self._precent_margin_bottom = margin_bottom

    # ------------------------------------------------------------------------------------------------------------------
    #  Внутренние методы
    # ------------------------------------------------------------------------------------------------------------------

    # Изменение размеров изображения
    def __resize_frame(self, frame, width, height, out = True):
        """
        Изменение размеров изображения

        (np.ndarray, int, int [, bool]) -> tuple

        Аргументы:
            frame  - Изображение
            width  - Ширина изображения для масштабирования
            height - Высота изображения для масштабирования
            out    - Печатать процесс выполнения

        Возвращает кортеж:
            1. Масштабированное изображение
            2. Во сколько раз масштабировалось изображение по ширине
            3. Во сколько раз масштабировалось изображение по высоте
        """

        # Проверка аргументов
        if (type(frame) is not np.ndarray or len(frame) is 0
                or type(height) is not int or height < 0 or type(width) is not int or width < 0
                or type(out) is not bool):
            # Вывод сообщения
            if out is True:
                print(self._invalid_arguments.format(
                    self.red, datetime.now().strftime(self._format_time), self.end,
                    __class__.__name__ + '.' + self.__resize_frame.__name__
                ))

            return None

        frame_width = frame.shape[1]  # Ширина изображения
        frame_height = frame.shape[0]  # Высота изображения

        # Ширина изображения нулевая
        if not width:
            width = frame_width

        # Высота изображения нулевая
        if not height:
            height = int(frame_height * width / frame_width)  # Масштабирование ширины относительно изначальной ширины

        # Получение значений во сколько раз масштабировалось изображение меньше/больше исходного изображения
        scale_width = frame_width / width  # Ширина
        scale_height = frame_height / height  # Высота

        # Изменение размера изображения
        frame_resize = cv2.resize(frame, (width, height), interpolation = cv2.INTER_LINEAR)

        # Результат
        return frame_resize, scale_width, scale_height

    # ------------------------------------------------------------------------------------------------------------------
    #  Внешние методы
    # ------------------------------------------------------------------------------------------------------------------

    # Загрузка модели для метода Виолы-Джонса в OpenCV
    def load_model_opencv_haar(self, path_to_model = None, out = True):
        """
        Загрузка модели для метода Виолы-Джонса в OpenCV

        (str [, bool]) -> bool

        Аргументы:
           path_to_model - Путь к модели
           out           - Печатать процесс выполнения

        Возвращает: True если модель загружена, в обратном случае False
        """

        # Путь к модели по умолчанию
        if path_to_model is None:
            path_to_model = self._path_to_models + '/haarcascades/'\
                            + self._path_to_files_models['opencv_haar']['path_to_model']

        # Проверка аргументов
        if type(path_to_model) is not str or not path_to_model or type(out) is not bool:
            # Вывод сообщения
            if out is True:
                print(self._invalid_arguments.format(
                    self.red, datetime.now().strftime(self._format_time),
                    self.end, __class__.__name__ + '.' + self.load_model_opencv_haar.__name__
                ))

            return False

        # Файл модели не найден
        if self._file_manager.search_file(path_to_model, self._required_extension_models[0], False, out) is False:
            return False

        # Вывод сообщения
        if out is True:
            print(self._load_model.format(
                datetime.now().strftime(self._format_time),
                self.packages_functions['opencv_haar']['ru']
            ))

        try:
            # Загрузка классификатора распознавания лиц из файла
            self._model = cv2.CascadeClassifier(path_to_model)
        except SystemError:
            # Вывод сообщения
            if out is True:
                print(self._model_not_load.format(self.red, datetime.now().strftime(self._format_time), self.end,
                                                  os.path.basename(path_to_model)))

            return False

        self.title_ru = self.packages_functions['opencv_haar']['ru']  # Установка названия метода на русском
        self.title_en = self.packages_functions['opencv_haar']['en']  # Установка названия метода на английском

        return True

    # Загрузка модели для глубокого обучения в OpenCV
    def load_model_opencv_dnn(self, path_to_model = None, path_to_config_model = None, dnn = 'tf', out = True):
        """
        Загрузка модели для метода Виолы-Джонса в OpenCV

        (str, str, str [, bool]) -> bool

        Аргументы:
           path_to_model        - Путь к модели
           path_to_config_model - Путь к конфигурационному файлу модели
           dnn                  - Модель нейронной сети
           out                  - Печатать процесс выполнения

        Возвращает: True если модель загружена, в обратном случае False
        """

        none = 'DL'  # Замена None

        # Путь к модели по умолчанию
        if path_to_model is None:
            path_to_model = none

        # Путь к конфигурационному файлу модели по умолчанию
        if path_to_config_model is None:
            path_to_config_model = none

        # Проверка аргументов
        if type(path_to_model) is not str or not path_to_model or type(path_to_config_model) is not str \
                or not path_to_config_model or type(dnn) is not str or not dnn or type(out) is not bool:
            # Вывод сообщения
            if out is True:
                print(self._invalid_arguments.format(
                    self.red, datetime.now().strftime(self._format_time),
                    self.end, __class__.__name__ + '.' + self.load_model_opencv_dnn.__name__
                ))

            return False

        # Модель нейронной сети не совпадает с необходимыми
        if dnn not in self._dnn:
            return False

        # Путь к модели по умолчанию
        if path_to_model is none:
            path_to_model = self._path_to_models + '/' + self._path_to_files_models['opencv_dnn'][dnn]['path_to_model']

        # Путь к конфигурационному файлу модели по умолчанию
        if path_to_config_model is none:
            path_to_config_model = self._path_to_models + '/' \
                                   + self._path_to_files_models['opencv_dnn'][dnn]['path_to_config_model']

        required_extension_model = None  # Необходимое расширения файла модели
        required_extension_config_model = None  # Необходимое расширения конфигурационного файла модели

        # 8-битная квантованная версия с использованием TensorFlow
        if dnn == self._dnn[0]:
            # Необходимое расширения файла модели
            required_extension_model = self._required_extension_models[2]

            # Необходимое расширения конфигурационного файла модели
            required_extension_config_model = self._required_extension_models[1]

        # Версия FP16 оригинальной реализации Caffe
        if dnn == self._dnn[1]:
            # Необходимое расширения файла модели
            required_extension_model = self._required_extension_models[4]

            # Необходимое расширения конфигурационного файла модели
            required_extension_config_model = self._required_extension_models[3]

        # Файл модели не найден
        if self._file_manager.search_file(path_to_model, required_extension_model, False, out) is False:
            return False

        # Конфигурационный файл модели не найден
        if self._file_manager.search_file(path_to_config_model, required_extension_config_model, False, out) is False:
            return False

        # Вывод сообщения
        if out is True:
            print(self._load_model.format(
                datetime.now().strftime(self._format_time),
                self.packages_functions['opencv_dnn']['ru']
            ))

        try:
            # 8-битная квантованная версия с использованием TensorFlow
            if dnn == self._dnn[0]:
                # Чтение модели нейронной сети в формате TensorFlow
                self._model = cv2.dnn.readNetFromTensorflow(path_to_model, path_to_config_model)

            # Версия FP16 оригинальной реализации Caffe
            if dnn == self._dnn[1]:
                # Чтение модели нейронной сети в формате Caffe
                self._model = cv2.dnn.readNetFromCaffe(path_to_config_model, path_to_model)
        except SystemError:
            # Вывод сообщения
            if out is True:
                print(self._model_not_load.format(self.red, datetime.now().strftime(self._format_time), self.end,
                                                  os.path.basename(path_to_model)))

            return False

        self.title_ru = self.packages_functions['opencv_dnn']['ru']  # Установка названия метода на русском
        self.title_en = self.packages_functions['opencv_dnn']['en']  # Установка названия метода на английском

        return True

    # Загрузка модели для функций HoG и SVM в Dlib
    def load_model_dlib_hog(self, out = True):
        """
        Загрузка модели для функций HoG и SVM в Dlib

        ([bool]) -> bool

        Аргументы:
           out - Печатать процесс выполнения

        Возвращает: True если модель загружена, в обратном случае False
        """

        # Проверка аргументов
        if type(out) is not bool:
            return False

        # Вывод сообщения
        if out is True:
            print(self._load_model.format(
                datetime.now().strftime(self._format_time),
                self.packages_functions['dlib_hog']['ru']
            ))

        try:
            # Загрузка детектора лица по умолчанию
            self._model = dlib.get_frontal_face_detector()
        except SystemError:
            # Вывод сообщения
            if out is True:
                print(self._model_not_load.format(self.red, datetime.now().strftime(self._format_time), self.end,
                                                  'HoG и SVM в Dlib'))

            return False

        self.title_ru = self.packages_functions['dlib_hog']['ru']  # Установка названия метода на русском
        self.title_en = self.packages_functions['dlib_hog']['en']  # Установка названия метода на английском

        return True

    # Загрузка модели для Convolutional Neural Network в Dlib
    def load_model_dlib_cnn(self, path_to_model = None, out = True):
        """
        Загрузка модели для метода Виолы-Джонса в OpenCV

        (str [, bool]) -> bool

        Аргументы:
           path_to_model - Путь к модели
           out           - Печатать процесс выполнения

        Возвращает: True если модель загружена, в обратном случае False
        """

        # Путь к модели по умолчанию
        if path_to_model is None:
            path_to_model = self._path_to_models + '/' + self._path_to_files_models['dlib_cnn']['path_to_model']

        # Проверка аргументов
        if type(path_to_model) is not str or not path_to_model or type(out) is not bool:
            # Вывод сообщения
            if out is True:
                print(self._invalid_arguments.format(
                    self.red, datetime.now().strftime(self._format_time),
                    self.end, __class__.__name__ + '.' + self.load_model_opencv_haar.__name__
                ))

            return False

        # Файл модели не найден
        if self._file_manager.search_file(path_to_model, self._required_extension_models[5], False, out) is False:
            return False

        # Вывод сообщения
        if out is True:
            print(self._load_model.format(
                datetime.now().strftime(self._format_time),
                self.packages_functions['dlib_cnn']['ru']
            ))

        try:
            # Загрузка модели нейронной сети в формате Dlib
            self._model = dlib.cnn_face_detection_model_v1(path_to_model)
        except SystemError:
            # Вывод сообщения
            if out is True:
                print(self._model_not_load.format(self.red, datetime.now().strftime(self._format_time), self.end,
                                                  os.path.basename(path_to_model)))

            return False

        self.title_ru = self.packages_functions['dlib_cnn']['ru']  # Установка названия метода на русском
        self.title_en = self.packages_functions['dlib_cnn']['en']  # Установка названия метода на английском

        return True

    # Метод Виолы-Джонса в OpenCV
    def opencv_haar(self, face_cascade, frame, width = 300, height = 0, min_neighbors = 3, draw = True, out = True):
        """
        Поиск лиц с помощью метода Виолы-Джонса в OpenCV

        (cv2.CascadeClassifier, np.ndarray [, int, int, int, bool, bool]) -> tuple

        Аргументы:
            face_cascade  - Каскадный классификатор
            frame         - Изображение
            width         - Ширина изображения для масштабирования
            height        - Высота изображения для масштабирования
            min_neighbors - Количество соседей для каждого прямоугольника
            draw          - Рисование на изображении областей с лицами
            out           - Печатать процесс выполнения

        Возвращает кортеж:
            1. Обработанное изображение
            2. Список координат лиц
        """

        # Проверка аргументов
        if (type(face_cascade) is not cv2.CascadeClassifier or type(frame) is not np.ndarray or len(frame) is 0
                or type(height) is not int or height < 0 or type(width) is not int or width < 0
                or type(min_neighbors) is not int or min_neighbors <= 0 or type(draw) is not bool
                or type(out) is not bool):
            # Вывод сообщения
            if out is True:
                print(self._invalid_arguments.format(
                    self.red, datetime.now().strftime(self._format_time), self.end,
                    __class__.__name__ + '.' + self.opencv_haar.__name__
                ))

            return None

        # Вывод сообщения
        if out is True:
            print(self._face_detect.format(datetime.now().strftime(self._format_time)))

        frame_clone = frame.copy()  # Копирование изображения

        # Результат изменения размеров изображения
        res_resize_frame = self.__resize_frame(
            frame = frame_clone,
            width = width,
            height = height,
            out = out
        )

        # Изображение не масштабировалось
        if res_resize_frame is None:
            return None

        # 1. Уменьшенное изображение
        # 2. Во сколько раз масштабировалось изображение по ширине
        # 3. Во сколько раз масштабировалось изображение по высоте
        frame_clone_small, scale_width, scale_height = res_resize_frame

        # Преобразование изображения из BGR в оттенки серого
        frame_gray = cv2.cvtColor(frame_clone_small, cv2.COLOR_BGR2GRAY)

        # Обнаружение лиц разных размеров на изображении
        faces = face_cascade.detectMultiScale(frame_gray, minNeighbors = min_neighbors)

        faces_boxes = []  # Список кординат лиц

        # Пройтись по всем найденным лицам
        for (x, y, w, h) in faces:
            x1 = x  # Начальная координата по оси X
            y1 = y  # Начальная координата по оси Y
            x2 = x + w  # Конечная координата по оси X
            y2 = y + h  # Конечная координата по оси Y

            # Вычисление прямоугольной области с лицом для оригинального изображения
            rect = [
                int(x1 * scale_width),  # Начальная координата по оси X
                int(y1 * scale_height),  # Начальная координата по оси Y
                int(x2 * scale_width),  # Конечная координата по оси X
                int(y2 * scale_height)  # Конечная координата по оси Y
            ]

            faces_boxes.append(rect)  # Добавление прямоульной области с лицом в список координат лиц

            # Рисование прямоугольной области с лицом на изображении
            if draw is True:
                cv2.rectangle(
                    frame_clone,  # Исходная копия изображения
                    (rect[0], rect[1]),  # Верхняя левая точка прямоугольника
                    (rect[2], rect[3]),  # Нижняя правая точка прямоугольника
                    self.rectangle_color,  # Цвет прямоугольника
                    self.rectangle_thickness,  # Толщина рамки прямоугольника
                    cv2.LINE_4  # Тип линии
                )

        # Вывод сообщения
        if out is True:
            # Лица найдены
            if len(faces_boxes) > 0:
                print(self._face_found.format(datetime.now().strftime(self._format_time), len(faces_boxes)))
            else:
                print(self._face_not_found.format(self.red, datetime.now().strftime(self._format_time), self.end))

        # Результат
        return frame_clone, faces_boxes

    # Глубокое обучение в OpenCV
    def opencv_dnn(self, net, frame, width = 300, height = 0, conf_threshold = 0.7, draw = True, draw_precent = True,
                   out = True):
        """
        Поиск лиц с помощью глубокого обучения в OpenCV

        (cv2.dnn_Net, numpy.ndarray [, int, int, float, bool, bool, bool]) -> tuple

        Аргументы:
            net            - Нейронная сеть
            frame          - Изображение
            width          - Ширина изображения для масштабирования
            height         - Высота изображения для масштабирования
            conf_threshold - Доверительный порог
            draw           - Рисование на изображении областей с лицами
            draw_precent   - Рисование на изображении процентов для каждого найденного лица
            out            - Печатать процесс выполнения

        Возвращает кортеж:
            1. Обработанное изображение
            2. Список координат лиц
        """

        # Проверка аргументов
        if (type(net) is not cv2.dnn_Net or type(frame) is not np.ndarray or len(frame) is 0
                or type(height) is not int or height < 0 or type(width) is not int or width < 0
                or type(conf_threshold) is not float or conf_threshold < 0 or conf_threshold > 1
                or type(draw) is not bool or type(draw_precent) is not bool or type(out) is not bool):
            # Вывод сообщения
            if out is True:
                print(self._invalid_arguments.format(
                    self.red, datetime.now().strftime(self._format_time), self.end,
                    __class__.__name__ + '.' + self.opencv_dnn.__name__
                ))

            return None

        frame_clone = frame.copy()  # Копирование изображения
        frame_height = frame_clone.shape[0]  # Высота изображения
        frame_width = frame_clone.shape[1]  # Ширина изображенияs

        # Параметр ширины не указан
        if not width:
            width = frame_width

        # Параметр высоты не указан
        if not height:
            height = int(frame_height * width / frame_width)  # Масштабирование ширины относительно ширины

        # Обработка входного изображения
        # - Вычитание среднего значения из элементов каждого канала
        # - Масштабирование изображения
        blob = cv2.dnn.blobFromImage(frame_clone, 1.0, (width, height), [104, 117, 123], False, False)

        net.setInput(blob)  # Прогонка обработанного входного изображения через сеть
        detections = net.forward()  # Прогнозы с обнаруженными лицами

        faces_boxes = []  # Список кординат лиц

        # Пройтись по всем прогнозам с лицами
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]  # Получение текущего прогноза

            # Прогноз больше доверительного порога
            if confidence > conf_threshold:
                x1 = int(detections[0, 0, i, 3] * frame_width)  # Начальная координата по оси X
                y1 = int(detections[0, 0, i, 4] * frame_height)  # Начальная координата по оси Y
                x2 = int(detections[0, 0, i, 5] * frame_width)  # Конечная координата по оси X
                y2 = int(detections[0, 0, i, 6] * frame_height)  # Конечная координата по оси Y

                faces_boxes.append([x1, y1, x2, y2])  # Добавление прямоугольной области с лицом в список координат лиц

                # Рисование прямоугольной области с лицом на изображении
                if draw is True:
                    cv2.rectangle(
                        frame_clone,  # Исходная копия изображения
                        (x1, y1),  # Верхняя левая точка прямоугольника
                        (x2, y2),  # Нижняя правая точка прямоугольника
                        self.rectangle_color,  # Цвет прямоугольника
                        self.rectangle_thickness,  # Толщина рамки прямоугольника
                        cv2.LINE_4  # Тип линии
                    )

                    # Рисование на изображении процентов для каждого найденного лица
                    if draw_precent is True:
                        label_face = self._precent.format(confidence * 100)  # Процент лица

                        labels_font = cv2.FONT_HERSHEY_SIMPLEX  # Шрифт

                        # Размеры текста
                        precent_size = cv2.getTextSize(
                            label_face, labels_font, self.precent_scale, self.precent_thickness
                        )[0]

                        # Толщина рамки прямоугольника с лицами минимальная
                        if self.rectangle_thickness == 1:
                            rectangle_thickness = 0
                            margin_bottom = 2  # Дополнительный отступ
                        else:
                            # Округление толщины рамки прямоугольника с лицами
                            rectangle_thickness = int(
                                Decimal(self.rectangle_thickness / 2).to_integral_value(rounding=ROUND_HALF_UP)
                            )
                            margin_bottom = 1  # Дополнительный отступ

                        # Верхняя левая точка прямоугольника
                        labels_base_coords = (
                            x1 - rectangle_thickness,
                            y1 - rectangle_thickness - (self.precent_padding * 2) - self.precent_margin_bottom
                            - precent_size[1] - margin_bottom
                        )

                        # Рисование прямоугольной области в виде фона текста на изображении
                        cv2.rectangle(
                            frame_clone,  # Исходная копия изображения
                            # Верхняя левая точка прямоугольника
                            (labels_base_coords[0], labels_base_coords[1]),
                            # Нижняя правая точка прямоугольника
                            (labels_base_coords[0] + (self.precent_padding * 2) + precent_size[0],
                             labels_base_coords[1] + (self.precent_padding * 2) + precent_size[1]),
                            self.precent_background_color,  # Цвет прямоугольника
                            cv2.FILLED,  # Толщина рамки прямоугольника
                            cv2.LINE_AA  # Тип линии
                        )

                        # Нанесение процентов на кадр
                        cv2.putText(
                            frame_clone, label_face,
                            (x1 + self.precent_padding - rectangle_thickness,
                             y1 - self.precent_margin_bottom - self.precent_padding - rectangle_thickness
                             - margin_bottom),
                            labels_font, self.precent_scale,
                            self.precent_text_color, self.precent_thickness, cv2.LINE_AA
                        )

        # Вывод сообщения
        if out is True:
            # Лица найдены
            if len(faces_boxes) > 0:
                print(self._face_found.format(datetime.now().strftime(self._format_time), len(faces_boxes)))
            else:
                print(self._face_not_found.format(self.red, datetime.now().strftime(self._format_time), self.end))

        # Результат
        return frame_clone, faces_boxes

    # Функции HoG и SVM в Dlib
    def dlib_hog(self, detector, frame, width = 300, height = 0, draw = True, out = True):
        """
        Поиск лиц с помощью функций HoG и SVM в Dlib

        (dlib.fhog_object_detector, numpy.ndarray [, int, int, bool, bool]) -> tuple

        Аргументы:
            detector - Детектор лица
            frame    - Изображение
            width    - Ширина изображения для масштабирования
            height   - Высота изображения для масштабирования
            draw     - Рисование на изображении областей с лицами
            out      - Печатать процесс выполнения

        Возвращает кортеж:
            1. Обработанное изображение
            2. Список координат лиц
        """

        # Проверка аргументов
        if (type(detector) is not dlib.fhog_object_detector or type(frame) is not np.ndarray or len(frame) is 0
                or type(height) is not int or height < 0 or type(width) is not int or width < 0
                or type(draw) is not bool or type(out) is not bool):
            # Вывод сообщения
            if out is True:
                print(self._invalid_arguments.format(
                    self.red, datetime.now().strftime(self._format_time), self.end,
                    __class__.__name__ + '.' + self.dlib_hog.__name__
                ))

            return None

        frame_clone = frame.copy()  # Копирование изображения

        # Результат изменения размеров изображения
        res_resize_frame = self.__resize_frame(
            frame = frame_clone,
            width = width,
            height = height,
            out = out
        )

        # Изображение не масштабировалось
        if res_resize_frame is None:
            return None

        # 1. Уменьшенное изображение
        # 2. Во сколько раз масштабировалось изображение по ширине
        # 3. Во сколько раз масштабировалось изображение по высоте
        frame_clone_small, scale_width, scale_height = res_resize_frame

        # Преобразование изображения из BGR в RGB
        frame_rgb = cv2.cvtColor(frame_clone_small, cv2.COLOR_BGR2RGB)

        detections = detector(frame_rgb, 0)  # Прогнозы с обнаруженными лицами

        faces_boxes = []  # Список кординат лиц

        # Пройтись по всем прогнозам с лицами
        for face_rect in detections:
            # Прямоульная область с лицом
            rect = [
                int(face_rect.left() * scale_width), int(face_rect.top() * scale_height),
                int(face_rect.right() * scale_width), int(face_rect.bottom() * scale_height)
            ]
            faces_boxes.append(rect)  # Добавление прямоугольной области с лицом в список координат лиц

            # Рисование прямоугольной области с лицом на изображении
            if draw is True:
                cv2.rectangle(
                    frame_clone,  # Исходная копия изображения
                    (rect[0], rect[1]),  # Верхняя левая точка прямоугольника
                    (rect[2], rect[3]),  # Нижняя правая точка прямоугольника
                    self.rectangle_color,  # Цвет прямоугольника
                    self.rectangle_thickness,  # Толщина рамки прямоугольника
                    cv2.LINE_4  # Тип линии
                )

        # Вывод сообщения
        if out is True:
            # Лица найдены
            if len(faces_boxes) > 0:
                print(self._face_found.format(datetime.now().strftime(self._format_time), len(faces_boxes)))
            else:
                print(self._face_not_found.format(self.red, datetime.now().strftime(self._format_time), self.end))

        # Результат
        return frame_clone, faces_boxes

    # Convolutional Neural Network в Dlib
    def dlib_cnn(self, detector, frame, width = 300, height = 0, draw = True, out = True):
        """
        Детектор лиц на основе Convolutional Neural Network в Dlib

        (dlib.cnn_face_detection_model_v1, numpy.ndarray [, int, int, bool, bool]) -> tuple

        Аргументы:
            detector - Детектор лица
            frame    - Изображение
            height   - Высота изображения для масштабирования
            width    - Ширина изображения для масштабирования
            draw     - Рисование на изображении областей с лицами
            out      - Печатать процесс выполнения

        Возвращает кортеж:
            1. Обработанное изображение
            2. Список координат лиц
        """

        # Проверка аргументов
        if (type(detector) is not dlib.cnn_face_detection_model_v1 or type(height) is not int or height < 0
                or type(width) is not int or width < 0 or type(frame) is not np.ndarray or len(frame) is 0
                or type(draw) is not bool or type(out) is not bool):
            # Вывод сообщения
            if out is True:
                print(self._invalid_arguments.format(
                    self.red, datetime.now().strftime(self._format_time), self.end,
                    __class__.__name__ + '.' + self.dlib_cnn.__name__
                ))

            return None

        frame_clone = frame.copy()  # Копирование изображения

        # Результат изменения размеров изображения
        res_resize_frame = self.__resize_frame(
            frame = frame_clone,
            width = width,
            height = height,
            out = out
        )

        # Изображение не масштабировалось
        if res_resize_frame is None:
            return None

        # 1. Уменьшенное изображение
        # 2. Во сколько раз масштабировалось изображение по ширине
        # 3. Во сколько раз масштабировалось изображение по высоте
        frame_clone_small, scale_width, scale_height = res_resize_frame

        # Преобразование изображения из BGR в RGB
        frame_rgb = cv2.cvtColor(frame_clone_small, cv2.COLOR_BGR2RGB)

        detections = detector(frame_rgb, 0)  # Прогнозы с обнаруженными лицами

        faces_boxes = []  # Список кординат лиц

        # Пройтись по всем прогнозам с лицами
        for face_rect in detections:
            # Прямоульная область с лицом
            rect = [
                int(face_rect.rect.left() * scale_width), int(face_rect.rect.top() * scale_height),
                int(face_rect.rect.right() * scale_width), int(face_rect.rect.bottom() * scale_height)
            ]
            faces_boxes.append(rect)  # Добавление прямоугольной области с лицом в список координат лиц

            # Рисование прямоугольной области с лицом на изображении
            if draw is True:
                cv2.rectangle(
                    frame_clone,  # Исходная копия изображения
                    (rect[0], rect[1]),  # Верхняя левая точка прямоугольника
                    (rect[2], rect[3]),  # Нижняя правая точка прямоугольника
                    self.rectangle_color,  # Цвет прямоугольника
                    self.rectangle_thickness,  # Толщина рамки прямоугольника
                    cv2.LINE_4  # Тип линии
                )

        # Вывод сообщения
        if out is True:
            # Лица найдены
            if len(faces_boxes) > 0:
                print(self._face_found.format(datetime.now().strftime(self._format_time), len(faces_boxes)))
            else:
                print(self._face_not_found.format(self.red, datetime.now().strftime(self._format_time), self.end))

        # Результат
        return frame_clone, faces_boxes

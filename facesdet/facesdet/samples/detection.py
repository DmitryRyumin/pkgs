#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Поиск лиц

python facesdet/samples/detection.py [--file путь_к_фото_видео_файлу --config путь_к_конфигурационному_файлу
    --automatic_update --frames_to_update 25 --no_clear_shell]
"""

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
import cv2  # Алгоритмы компьютерного зрения

from datetime import datetime  # Работа со временем

# Персональные
import facesdet  # Поиск лиц

from pvv.samples import play  # Пример воспроизведения фото/видео данных
from facesdet.detection import Detection  # Поиск лиц
from facesdet import configs  # Конфигурационные файлы


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

        self._total_faces = 'Total found faces: {}'

        self._check_load_model = 'Error loading model ...'


# ######################################################################################################################
# Выполняем только в том случае, если файл запущен сам по себе
# ######################################################################################################################
class Run(Messages):
    """Класс для воспроизведения фото/видео данных"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()  # Выполнение конструктора из суперкласса

        # Набор методов для поиска лиц
        self._methods_data = (
            'opencv_haar',  # Поиск лиц с помощью метода Виолы-Джонса в OpenCV
            'opencv_dnn',  # Поиск лиц с помощью глубокого обучения в OpenCV
            'dlib_hog',  # Поиск лиц с помощью функций HoG и SVM в Dlib
            'dlib_cnn'  # Поиск лиц с помощью Convolutional Neural Network в Dlib
        )

        self._detection = Detection()  # Поиск лиц

        self._faces_point2 = (0, 0)  # Нижняя правая точка прямоугольника

        # Добавление вариантов ошибок при автоматическом обновлении конфигурационного файла
        self._automatic_update['model_not_load'] = False  # Модель не загружена

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

        # Выполнение функции из суперкласса с отрицательным результатом
        if super()._valid_json_config(config, out) is False:
            return False

        all_layer = 15  # Общее количество разделов
        curr_valid_layer = 0  # Валидное количество разделов

        # Проход по всем разделам конфигурационного файла
        for key, val in config.items():
            # Метод детекции лиц
            if key == 'method':
                # Проверка значения
                if type(val) is not str or not val:
                    continue

                # Поиск лиц с помощью метода Виолы-Джонса в OpenCV
                if val == 'opencv_haar':
                    curr_valid_layer += 1

                    # Отсекаем:
                    #     1. Тип нейронной сети
                    #     2. Доверительный порог поиска лица
                    #     3. Рисование на изображении процентов для каждого найденного лица
                    #     4. Коэффициент масштабирования шрифта (проценты)
                    #     5. Толщина линии шрифта (проценты)
                    #     6. Цвет текста процентов
                    #     7. Цвет фона процентов
                    #     8. Внутренний отступ для процентов
                    #     9. Внешний нижний отступ для процентов
                    all_layer -= 9

                # Поиск лиц с помощью глубокого обучения в OpenCV
                if val == 'opencv_dnn':
                    curr_valid_layer += 1

                    # Отсекаем:
                    #     Количество соседей для каждого прямоугольника
                    all_layer -= 1

                # Поиск лиц с помошью функций HoG и SVM в Dlib
                if val == 'dlib_hog':
                    curr_valid_layer += 1

                    # Отсекаем:
                    #     1. Количество соседей для каждого прямоугольника
                    #     2. Тип нейронной сети
                    #     3. Доверительный порог поиска лица
                    #     4. Рисование на изображении процентов для каждого найденного лица
                    #     5. Коэффициент масштабирования шрифта (проценты)
                    #     6. Толщина линии шрифта (проценты)
                    #     7. Цвет текста процентов
                    #     8. Цвет фона процентов
                    #     9. Внутренний отступ для процентов
                    #     10. Внешний нижний отступ для процентов
                    all_layer -= 10

                # Поиск лиц с помошью Convolutional Neural Network в Dlib
                if val == 'dlib_cnn':
                    curr_valid_layer += 1

                    # Отсекаем:
                    #     1. Количество соседей для каждого прямоугольника
                    #     2. Тип нейронной сети
                    #     3. Доверительный порог поиска лица
                    #     4. Рисование на изображении процентов для каждого найденного лица
                    #     5. Коэффициент масштабирования шрифта (проценты)
                    #     6. Толщина линии шрифта (проценты)
                    #     7. Цвет текста процентов
                    #     8. Цвет фона процентов
                    #     9. Внутренний отступ для процентов
                    #     10. Внешний нижний отступ для процентов
                    all_layer -= 10

            # Размер изображения для масштабирования
            if key == 'size':
                all_layer_2 = 1  # Общее количество подразделов в текущем разделе
                curr_valid_layer_2 = 0  # Валидное количество подразделов в текущем разделе

                # Проверка значения
                if type(val) is not dict or len(val) is 0:
                    continue

                # Проход по всем подразделам текущего раздела
                for k, v in val.items():
                    # Проверка значения
                    if type(v) is not int or v < 0:
                        continue

                    # Ширина изображения для масштабирования
                    if k == 'width':
                        curr_valid_layer_2 += 1

                    # Высота изображения для масштабирования
                    if k == 'height':
                        all_layer_2 += 1
                        curr_valid_layer_2 += 1

                if all_layer_2 == curr_valid_layer_2:
                    curr_valid_layer += 1

            # Метод детекции лиц 'opencv_haar'
            if 'method' in config and config['method'] == 'opencv_haar':
                # Количество соседей для каждого прямоугольника, работает при "method" = opencv_haar
                if key == 'min_neighbors':
                    # Проверка значения
                    if type(val) is not int or val <= 0:
                        continue

                    curr_valid_layer += 1

            # Метод детекции лиц 'opencv_dnn'
            if 'method' in config and config['method'] == 'opencv_dnn':
                # Тип нейронной сети, работает при "method" = opencv_dnn
                if key == 'dnn':
                    # Проверка значения
                    if type(val) is not str or not val:
                        continue

                    # Указан верный ключ
                    if val == 'tensorflow' or val == 'tf' or val == 'caffe':
                        curr_valid_layer += 1

                # Доверительный порог распознавания лица, работает при "method" = opencv_dnn
                if key == 'conf_threshold':
                    # Проверка значения
                    if type(val) is not float or val < 0.0 or val > 1.0:
                        continue

                    curr_valid_layer += 1

                # Рисование на изображении процентов для каждого найденного лица, работает при "method" = opencv_dnn
                if key == 'draw_precent':
                    # Проверка значения
                    if type(val) is not bool:
                        continue

                    curr_valid_layer += 1

                # Коэффициент масштабирования шрифта (проценты), работает при "method" = opencv_dnn
                if key == 'precent_scale':
                    # Проверка значения
                    if type(val) is not float or val <= 0.0 or val > 2.0:
                        continue

                    curr_valid_layer += 1

                # Толщина линии шрифта (проценты)
                if key == 'precent_thickness':
                    # Проверка значения
                    if type(val) is not int or val <= 0 or val > 4:
                        continue

                    curr_valid_layer += 1

                # 1. Цвет текста процентов
                # 2. Цвет фона процентов
                if key == 'precent_text_color' or key == 'precent_background_color':
                    all_layer_2 = 3  # Общее количество подразделов в текущем разделе
                    curr_valid_layer_2 = 0  # Валидное количество подразделов в текущем разделе

                    # Проверка значения
                    if type(val) is not dict or len(val) is 0:
                        continue

                    # Проход по всем подразделам текущего раздела
                    for k, v in val.items():
                        # Проверка значения
                        if type(v) is not int or v < 0 or v > 255:
                            continue

                        # 1. Красный
                        # 2. Зеленый
                        # 3. Синий
                        if k == 'red' or k == 'green' or k == 'blue':
                            curr_valid_layer_2 += 1

                    if all_layer_2 == curr_valid_layer_2:
                        curr_valid_layer += 1

                # 1. Внутренний отступ для процентов
                # 2. Внешний нижний отступ для процентов
                if key == 'precent_padding' or key == 'precent_margin_bottom':
                    # Проверка значения
                    if type(val) is not int or val < 0 or val > 30:
                        continue

                    curr_valid_layer += 1

            # Цвет рамки прямоугольника с лицами
            if key == 'rectangle_color':
                all_layer_2 = 3  # Общее количество подразделов в текущем разделе
                curr_valid_layer_2 = 0  # Валидное количество подразделов в текущем разделе

                # Проверка значения
                if type(val) is not dict or len(val) is 0:
                    continue

                # Проход по всем подразделам текущего раздела
                for k, v in val.items():
                    # Проверка значения
                    if type(v) is not int or v < 0 or v > 255:
                        continue

                    # 1. Красный
                    # 2. Зеленый
                    # 3. Синий
                    if k == 'red' or k == 'green' or k == 'blue':
                        curr_valid_layer_2 += 1

                if all_layer_2 == curr_valid_layer_2:
                    curr_valid_layer += 1

            # Толщина рамки прямоугольника с лицами
            if key == 'rectangle_thickness':
                # Проверка значения
                if type(val) is not int or val <= 0 or val > 10:
                    continue

                curr_valid_layer += 1

            # Расстояние между текстами
            if key == 'labels_distance':
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

        # Установка имени окна
        if set_window_name is True:
            curr_window_name = self._detection.title_en  # Текущее значение имени окна

        curr_method = self._args['method']  # Текущее значение метода
        curr_dnn = self._args['dnn']  # Текущее значение метода
        curr_size = self._args['size']  # Текущее значение размеров изображения

        # Выполнение функции из суперкласса с отрицательным результатом
        if super()._update_config_json(False) is False:
            return False

        if self._automatic_update['invalid_config_file'] is False:
            # 1. Метод был изменен
            # 2. Размер окна был изменен
            # 3. Размеры изображения были изменены
            if curr_method != self._args['method'] or curr_dnn != self._args['dnn']\
                    or curr_size['width'] != self._args['size']['width']\
                    or curr_size['height'] != self._args['size']['height']:
                # Загрузка модели
                if self._load_model() is False:
                    # Модель была загружена на прошлой проверке
                    if self._automatic_update['model_not_load'] is False:
                        # Модель не загружена в момент работы программы
                        self._automatic_update['model_not_load'] = True
                else:
                    # Модель загружена в момент работы программы
                    self._automatic_update['model_not_load'] = False

            # Установка имени окна и имя окна было изменено
            if set_window_name is True and curr_window_name != self._detection.title_en:
                self._viewer.set_window_name(self._detection.title_en)  # Установка имени окна

        return True

    # Загрузка модели
    def _load_model(self, out = True):
        """
        Загрузка модели

        ([bool]) -> bool

        Аргументы:
           out - Печатать процесс выполнения

        Возвращает: True если модель загружена, в обратном случае False
        """

        # Проверка аргументов
        if type(out) is not bool:
            return False

        # Поиск лиц с помощью метода Виолы-Джонса в OpenCV
        if self._args['method'] == self._methods_data[0]:
            return self._detection.load_model_opencv_haar(out = out)

        # Детектор лиц на основе глубокого обучения в OpenCV
        if self._args['method'] == self._methods_data[1]:
            return self._detection.load_model_opencv_dnn(dnn = self._args['dnn'], out = out)

        # Загружать если это не поиск лиц помошью функций HoG и SVM в Dlib
        if self._args['method'] == self._methods_data[2]:
            return self._detection.load_model_dlib_hog(out = out)

        # Поиск лиц с помощью Convolutional Neural Network в Dlib
        if self._args['method'] == self._methods_data[3]:
            return self._detection.load_model_dlib_cnn(out = out)

    # Поиск лиц
    def _faces_detection(self):
        """
        Поиск лиц
        """

        res_detection = None  # Результат метода поиска лиц

        # Цвет рамки прямоугольника с лицами
        self._detection.rectangle_color = (
            self._args['rectangle_color']['red'],
            self._args['rectangle_color']['green'],
            self._args['rectangle_color']['blue']
        )

        # Толщина рамки прямоугольника с лицами
        self._detection.rectangle_thickness = self._args['rectangle_thickness']

        # Метод Виолы-Джонса в OpenCV
        if self._args['method'] == self._methods_data[0]:
            res_detection = self._detection.opencv_haar(
                face_cascade = self._detection.model,
                frame = self._curr_frame,
                width = self._args['size']['width'],
                height = self._args['size']['height'],
                draw = True,
                min_neighbors = self._args['min_neighbors'],
                out = False
            )

        # Глубокое обучение в OpenCV
        if self._args['method'] == self._methods_data[1]:
            self._detection.precent_scale = self._args['precent_scale']  # Коэффициент масштабирования шрифта (проценты)
            self._detection.precent_thickness = self._args['precent_thickness']  # Толщина линии шрифта (проценты)
            # Цвет текста процентов
            self._detection.precent_text_color = (
                self._args['precent_text_color']['red'],
                self._args['precent_text_color']['green'],
                self._args['precent_text_color']['blue']
            )
            # Цвет фона процентов
            self._detection.precent_background_color = (
                self._args['precent_background_color']['red'],
                self._args['precent_background_color']['green'],
                self._args['precent_background_color']['blue']
            )
            self._detection.precent_padding = self._args['precent_padding']  # Внутренний отступ для процентов
            # Внешний нижний отступ для процентов
            self._detection.precent_margin_bottom = self._args['precent_margin_bottom']

            res_detection = self._detection.opencv_dnn(
                net = self._detection.model,
                frame = self._curr_frame,
                width = self._args['size']['width'],
                height = self._args['size']['height'],
                conf_threshold = self._args['conf_threshold'],
                draw = True,
                draw_precent = self._args['draw_precent'],
                out = False
            )

        # Функции HoG и SVM в Dlib
        if self._args['method'] == self._methods_data[2]:
            res_detection = self._detection.dlib_hog(
                detector = self._detection.model,
                frame = self._curr_frame,
                width = self._args['size']['width'],
                height = self._args['size']['height'],
                draw = True,
                out = False
            )

        # Convolutional Neural Network в Dlib
        if self._args['method'] == self._methods_data[3]:
            res_detection = self._detection.dlib_cnn(
                detector = self._detection.model,
                frame = self._curr_frame,
                width = self._args['size']['width'],
                height = self._args['size']['height'],
                draw = True,
                out = False
            )

        # Метод поиска лиц не выполнен
        if res_detection is None:
            return False

        # 1. Выходное изображение
        # 2. Количество найденных лиц
        self._curr_frame, faces_boxes = res_detection

        label_faces = self._total_faces.format(len(faces_boxes))  # Текст с количеством найденных лиц

        # Процесс нанесения информации на изображение
        # Размеры текста
        labels_size = cv2.getTextSize(
            label_faces, self._labels_font, self._args['labels_scale'], self._args['labels_thickness']
        )[0]

        # Нижняя правая точка прямоугольника
        self._faces_point2 = (
            self._args['labels_base_coords']['left'] + labels_size[0] + self._args['labels_padding'] * 2,
            self._fps_point2[1] + self._args['labels_distance'] + labels_size[1] + self._args['labels_padding'] * 2
        )

        # Рисование прямоугольной области в виде фона текста на изображении
        cv2.rectangle(
            self._curr_frame,  # Исходная копия изображения
            # Верхняя левая точка прямоугольника
            (self._fps_point1[0], self._fps_point2[1] + self._args['labels_distance']),
            # Нижняя правая точка прямоугольника
            self._faces_point2,
            # Цвет прямоугольника
            (self._args['background_color']['red'],
             self._args['background_color']['green'],
             self._args['background_color']['blue']),
            cv2.FILLED,  # Толщина рамки прямоугольника
            cv2.LINE_AA  # Тип линии
        )

        # Нанесение количества найденных лиц на кадр
        cv2.putText(
            self._curr_frame, label_faces,
            (self._args['labels_base_coords']['left'] + self._args['labels_padding'],
             self._fps_point2[1] + self._args['labels_distance'] + labels_size[1] + self._args['labels_padding']),
            self._labels_font, self._args['labels_scale'],
            (self._args['text_color']['red'], self._args['text_color']['green'], self._args['text_color']['blue']),
            self._args['labels_thickness'],
            cv2.LINE_AA
        )

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

        # Выполнение функции из суперкласса с заданными параметрами и отрицательным результатом
        if super()._err_notification(self._automatic_update['model_not_load'], self._check_load_model, out) is False:
            return False

        return True

    # Циклическое получение кадров из видеопотока
    def _loop(self, func = None, out = True):
        """
        Циклическое получение кадров из фото/видеопотока

        ([bool]) -> bool

        Аргументы:
           func - Функция или метод
           out  - Печатать процесс выполнения

        Возвращает: True если получение кадров осуществляется, в обратном случае False
        """

        # Выполнение функции из суперкласса с отрицательным результатом
        if super()._loop(self._faces_detection, out) is False:
            return False

        return True

    # ------------------------------------------------------------------------------------------------------------------
    #  Внешние методы
    # ------------------------------------------------------------------------------------------------------------------

    # Запуск
    def run(self, metadata = facesdet, resources = configs, start = True, out = True):
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

        # Загрузка модели
        if self._load_model() is False:
            return False

        self._viewer.window_name = self._detection.title_en  # Установка имени окна

        # Запуск процесса извлечения изображений
        if start is True:
            self._viewer.set_loop(self._loop)  # Циклическая функция извлечения изображений
            self._viewer.start()  # Запуск


def main():
    run = Run()

    run.run()


if __name__ == "__main__":
    main()

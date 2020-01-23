#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Поиск объектов

python objdet/samples/detection.py --file путь_к_фото_видео_файлу [--config путь_к_конфигурационному_файлу
    --automatic_update --frames_to_update 25 --no_clear_shell]
"""

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
import cv2  # Алгоритмы компьютерного зрения

from datetime import datetime  # Работа со временем
from decimal import Decimal, ROUND_HALF_UP  # Округление по математическому закону

# Персональные
import objdet  # Поиск объектов

from pvv.samples import play  # Пример воспроизведения фото/видео данных
from objdet.detection import Detection  # Поиск объектов
from objdet import configs  # Конфигурационные файлы


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

        self._total_objects = 'Total objects: {}'
        self._object_detection_not_precent = '{}'
        self._object_detection = self._object_detection_not_precent + ' - {:.2f}%'

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

        self._detection = Detection()  # Поиск объектов

        self._objects_point2 = (0, 0)  # Нижняя правая точка прямоугольника

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

        all_layer = 12  # Общее количество разделов
        curr_valid_layer = 0  # Валидное количество разделов

        # Проход по всем разделам конфигурационного файла
        for key, val in config.items():
            # 1. Путь к модели
            # 2. Путь к конфигурационному файлу модели
            if key == 'path_to_model' or key == 'path_to_labels':
                # Конфигурационный файл передан
                if self._args['config'] is not None:
                    all_layer += 1  # Увеличение общего количества разделов

                    # Проверка значения
                    if type(val) is not str or not val:
                        continue

                    curr_valid_layer += 1

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

            # 1. Цвет рамки прямоугольника с объектами
            # 2. Цвет текста для найденных объектов
            # 3. Цвет фона для найденных объектов
            if key == 'rectangle_color' or key == 'object_text_color' or key == 'object_background_color':
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

            # Толщина рамки прямоугольника с объектами
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

            # Доверительный порог детектирования объектов
            if key == 'conf_threshold':
                # Проверка значения
                if type(val) is not float or val < 0.0 or val > 1.0:
                    continue

                curr_valid_layer += 1

            # Рисование на изображении процентов для каждого найденного объекта
            if key == 'draw_precent':
                # Проверка значения
                if type(val) is not bool:
                    continue

                curr_valid_layer += 1

            # Коэффициент масштабирования шрифта для найденных объектов
            if key == 'object_scale':
                # Проверка значения
                if type(val) is not float or val <= 0.0 or val > 2.0:
                    continue

                curr_valid_layer += 1

            # Толщина линии шрифта для найденных объектов
            if key == 'object_thickness':
                # Проверка значения
                if type(val) is not int or val <= 0 or val > 4:
                    continue

                curr_valid_layer += 1

            # 1. Внутренний отступ для найденных объектов
            # 2. Внешний нижний отступ для найденных объектов
            if key == 'object_padding' or key == 'object_margin_bottom':
                # Проверка значения
                if type(val) is not int or val < 0 or val > 30:
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

        curr_path_to_model = self._args['path_to_model']  # Текущий путь к модели
        curr_path_to_labels = self._args['path_to_labels']  # Текущий путь к конфигурационному файлу модели

        # Выполнение функции из суперкласса с отрицательным результатом
        if super()._update_config_json(set_window_name) is False:
            return False

        if self._automatic_update['invalid_config_file'] is False:
            # 1. Путь к модели был изменен
            # 2. Путь к конфигурационному файлу модели был изменен
            if curr_path_to_model != self._args['path_to_model'] or curr_path_to_labels != self._args['path_to_labels']:
                # Загрузка модели для поиска объектов
                if self._detection.load_model(self._args['path_to_model'], self._args['path_to_labels']) is False:
                    # Модель была загружена на прошлой проверке
                    if self._automatic_update['model_not_load'] is False:
                        # Модель не загружена в момент работы программы
                        self._automatic_update['model_not_load'] = True
                else:
                    # Модель загружена в момент работы программы
                    self._automatic_update['model_not_load'] = False

        return True

    # Поиск объектов
    def _objects_detection(self):
        """
        Поиск объектов
        """

        # Модель была загружена
        if self._automatic_update['model_not_load'] is False:

            norm = False  # По умолчанию нормализация результатов найденных объектов не нужна

            # Изменение размеров изображения не стандартные
            if self._args['size']['width'] is not 0 or self._args['size']['height'] is not 0:
                # Изменение размеров изображения
                resize_frame, scale_width, scale_height = self._viewer.resize_frame(
                    self._curr_frame, self._args['size']['width'], self._args['size']['height']
                )

                # Изображение не уменьшилось
                if resize_frame is None:
                    resize_frame = self._curr_frame
                else:
                    norm = True  # Дальнейшая нормализация результатов найденных объектов нужна
            else:
                resize_frame = self._curr_frame

            # Поиск объектов
            output_dict = self._detection.objects(resize_frame, conf_threshold = self._args['conf_threshold'])

            # Объекты не найдены
            if output_dict is None:
                return None

            cnt_objects = 0  # Счетчик объектов

            # Объекты найдены на изображении
            if len(output_dict) > 0:
                # Пройтись по всем найденным объектам
                for key, val in output_dict.items():
                    # Пройтись по всем объектам, конкретной метки
                    for v in val:
                        cnt_objects += 1  # Увеличение счетчика найденный объектов

                        # Нормализация результатов
                        if norm is True:
                            v['boxes'][0] = \
                                int(Decimal(v['boxes'][0] * scale_width).to_integral_value(rounding=ROUND_HALF_UP))
                            v['boxes'][1] = \
                                int(Decimal(v['boxes'][1] * scale_height).to_integral_value(rounding=ROUND_HALF_UP))
                            v['boxes'][2] = \
                                int(Decimal(v['boxes'][2] * scale_width).to_integral_value(rounding=ROUND_HALF_UP))
                            v['boxes'][3] = \
                                int(Decimal(v['boxes'][3] * scale_height).to_integral_value(rounding=ROUND_HALF_UP))

                        # Рисование на изображении процентов для каждого найденного объекта
                        if self._args['draw_precent'] is True:
                            # Текст с объектом
                            label_object = self._object_detection.format(key, round(v['scores'] * 100, 2))
                        else:
                            # Текст с объектом без процентов
                            label_object = self._object_detection_not_precent.format(key)

                        # Размеры текста
                        labels_size = cv2.getTextSize(
                            label_object, self._labels_font, self._args['object_scale'], self._args['object_thickness']
                        )[0]

                        # Толщина рамки прямоугольника с объектами минимальная
                        if self._args['rectangle_thickness'] == 1:
                            rectangle_thickness = 0
                            margin_bottom = 2  # Дополнительный отступ
                        else:
                            # Округление толщины рамки прямоугольника с объектами
                            rectangle_thickness = int(
                                Decimal(self._args['rectangle_thickness'] / 2).to_integral_value(rounding=ROUND_HALF_UP)
                            )
                            margin_bottom = 1  # Дополнительный отступ

                        # Верхняя левая точка прямоугольника
                        object_base_coords = (
                            v['boxes'][0] - rectangle_thickness,
                            v['boxes'][2] - rectangle_thickness
                            - (self._args['object_padding'] * 2) - self._args['object_margin_bottom'] - labels_size[1]
                            - margin_bottom
                        )

                        # Рисование прямоугольной области в виде фона текста на изображении
                        cv2.rectangle(
                            self._curr_frame,  # Текущий кадр
                            # Верхняя левая точка прямоугольника
                            (object_base_coords[0], object_base_coords[1]),
                            # Нижняя правая точка прямоугольника
                            (object_base_coords[0] + (self._args['object_padding'] * 2) + labels_size[0],
                             object_base_coords[1] + (self._args['object_padding'] * 2) + labels_size[1]),
                            # Цвет прямоугольника
                            (self._args['object_background_color']['red'],
                             self._args['object_background_color']['green'],
                             self._args['object_background_color']['blue']),
                            cv2.FILLED,  # Толщина рамки прямоугольника
                            cv2.LINE_AA  # Тип линии
                        )

                        # Нанесение описания объекта на кадр
                        cv2.putText(
                            self._curr_frame, label_object,
                            (v['boxes'][0] + self._args['object_padding'],
                             v['boxes'][2] - self._args['object_margin_bottom'] - self._args['object_padding']
                             - rectangle_thickness - margin_bottom),
                            self._labels_font, self._args['object_scale'],
                            (self._args['object_text_color']['red'],
                             self._args['object_text_color']['green'],
                             self._args['object_text_color']['blue']),
                            self._args['object_thickness'],
                            cv2.LINE_AA
                        )

                        # Рисование прямоугольной области в виде фона текста на изображении
                        cv2.rectangle(
                            self._curr_frame,  # Текущий кадр
                            (v['boxes'][0], v['boxes'][2]),  # Верхняя левая точка прямоугольника
                            (v['boxes'][1], v['boxes'][3]),  # Нижняя правая точка прямоугольника
                            # Цвет прямоугольника
                            (self._args['rectangle_color']['red'],
                             self._args['rectangle_color']['green'],
                             self._args['rectangle_color']['blue']),
                            self._args['rectangle_thickness'],  # Толщина рамки прямоугольника
                            cv2.LINE_4  # Тип линии
                        )

            label_objects = self._total_objects.format(cnt_objects)  # Текст с количеством найденных объектов

            # Размеры текста
            labels_size = cv2.getTextSize(
                label_objects, self._labels_font, self._args['labels_scale'], self._args['labels_thickness']
            )[0]

            # Нижняя правая точка прямоугольника
            self._objects_point2 = (
                self._args['labels_base_coords']['left'] + labels_size[0] + self._args['labels_padding'] * 2,
                self._fps_point2[1] + self._args['labels_distance'] + labels_size[1] + self._args['labels_padding'] * 2
            )

            # Рисование прямоугольной области в виде фона текста на изображении
            cv2.rectangle(
                self._curr_frame,  # Исходная копия изображения
                # Верхняя левая точка прямоугольника
                (self._fps_point1[0], self._fps_point2[1] + self._args['labels_distance']),
                # Нижняя правая точка прямоугольника
                self._objects_point2,
                # Цвет прямоугольника
                (self._args['background_color']['red'],
                 self._args['background_color']['green'],
                 self._args['background_color']['blue']),
                cv2.FILLED,  # Толщина рамки прямоугольника
                cv2.LINE_AA  # Тип линии
            )

            # Нанесение количества найденных объектов на кадр
            cv2.putText(
                self._curr_frame, label_objects,
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
        if super()._loop(self._objects_detection, out) is False:
            return False

        return True

    # ------------------------------------------------------------------------------------------------------------------
    #  Внешние методы
    # ------------------------------------------------------------------------------------------------------------------

    # Запуск
    def run(self, metadata = objdet, resources = configs, start = True, out = True):
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

        # Запуск алгоритма для поиска объектов
        if self._detection.start() is False:
            return False

        # Конфигурационный файл не передан
        if self._args['config'] is None:
            self._args['path_to_model'] = None   # Путь к модели по умолчанию
            self._args['path_to_labels'] = None  # Путь к конфигурационному файлу модели по умолчанию

        # Загрузка модели для поиска объектов
        if self._detection.load_model(self._args['path_to_model'], self._args['path_to_labels']) is False:
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

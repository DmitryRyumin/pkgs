#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Воспроизведение фото/видео данных

python pvv/samples/play.py --file путь_к_фото_видео_файлу [--no_clear_shell]
"""

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
import os        # Работа с файловой системой
import time      # Работа со временем
import argparse  # Парсинг аргументов и параметров командной строки
import cv2       # Алгоритмы компьютерного зрения

from datetime import datetime  # Работа со временем

# Персональные
from core2pkgs import core     # Глобальный файл настроек
import pvv
from pvv.viewer import Viewer  # Воспроизведение фото/видео данных
from pvv import configs        # Конфигурационные файлы
from filem.json import Json    # Работа с JSON


# ######################################################################################################################
# Сообщения
# ######################################################################################################################
class Messages(core.Core):
    """Класс для сообщений"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()  # Выполнение конструктора из суперкласса

        self._run_web = '[{}] Запуск WEB камеры ...'
        self._web_not_found = '[{}{}{}] WEB-камера не найдена ...'
        self._video_not_read = '[{}{}{}] Видео повреждено ...'
        self._photo_not_read = '[{}{}{}] Фото повреждено ...'

        self._frame_rate = 'FPS: {:.2f}'
        self._frame_rate_static = 'FPS: 60+'

        self._wrong_extension = '[{}{}{}] Расширение файла для фото должно быть одним из:'\
                                '\n\t"{}" (фото данные)'\
                                '\n\t"{}" (видео данные)'

        self._config_empty = '[{}{}{}]  Файл пуст ...'
        self._check_config_file_valid = '[{}] Проверка данных на валидность ...'


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

        self._args = None  # Аргументы командной строки

        # Набор данных
        self._formats_data = (
            'web',  # WEB-камера
            'video',  # Видеофайл
            'photo'  # Фото
        )

        # Поддерживаемые видео форматы
        self._supported_video_formats = ('mp4', 'avi')
        # Поддерживаемые фото форматы
        self._supported_photo_formats = ('png', 'jpg')

        self._labels_font = cv2.FONT_HERSHEY_SIMPLEX  # Шрифт
        self._labels_thickness = 1  # Толщина линии шрифта

        self._labels_base_coords = (10, 10)  # Базовые координаты текстов
        self._labels_padding = 10  # Внутренний отступ для текстов
        self._labels_distance = 10  # Расстояние между текстами

        self._cap = None  # Захват фото/видеоданных
        self._source = None  # Ресурс захвата фото/видеоданных
        self._curr_frame = None  # Текущий кадр

        self._viewer = Viewer()  # Воспроизведение фото/видео данных

        self._json = Json()  # Работа с JSON

        self._frame_count = 0  # Счетчик кадров

        self._frames_to_update = 0  # Счетчик автоматической проверки конфигурационного файла в момент работы программ

        # Варианты ошибок при автоматическом обновлении конфигурационного файла
        self._automatic_update = {
            'invalid_config_file': False  # Результат поиска необходимых значений в конфигурационном файле
        }

    # ------------------------------------------------------------------------------------------------------------------
    #  Внутренние методы
    # ------------------------------------------------------------------------------------------------------------------

    # Построение аргументов командной строки
    @staticmethod
    def __build_args():
        # Построение аргументов командой строки
        ap = argparse.ArgumentParser()

        ap.add_argument('--file', required = True, help = 'Путь к фото/видео файлу')
        ap.add_argument('--config', help = 'Путь к конфигурационному файлу')
        ap.add_argument('--no_clear_shell', action = 'store_false', help = 'Не очищать консоль перед выполнением')
        ap.add_argument('--automatic_update', action = 'store_true',
                        help = 'Автоматическая проверка конфигурационного файла в момент работы программы '
                               '(работает при заданном --config')
        ap.add_argument('--frames_to_update', type = int, default = 25,
                        help = 'Через какое количество шагов проверять конфигурационный файл '
                               '(работает при --automatic_update, значение по умолчанию: %(default)s)')

        return vars(ap.parse_args())  # Преобразование списка аргументов командной строки в словарь

    # Проверка JSON файла настроек на валидность
    def __valid_json_config(self, config, out = True):
        """
        Проверка настроек JSON на валидность

        (dict [, bool]) -> bool

        Аргументы:
           config - Словарь из JSON файла
           out    - Печатать процесс выполнения

        Возвращает: True если файл валидный, в обратном случае False
        """

        # Проверка аргументов
        if type(config) is not dict or type(out) is not bool:
            # Вывод сообщения
            if out is True:
                print(self._invalid_arguments.format(
                    self.red, datetime.now().strftime(self._format_time),
                    self.end, __class__.__name__ + '.' + self.__valid_json_config.__name__
                ))

            return False

        # Конфигурационный файл пуст
        if len(config) == 0:
            # Вывод сообщения
            if out is True:
                print(self._config_empty.format(self.red, datetime.now().strftime(self._format_time), self.end))

            return False

        # Вывод сообщения
        if out is True:
            print(self._check_config_file_valid.format(datetime.now().strftime(self._format_time)))

        all_layer = 8  # Общее количество разделов
        curr_valid_layer = 0  # Валидное количество разделов

        # Проход по всем разделам конфигурационного файла
        for key, val in config.items():
            # 1. Отображение метаданных
            # 2. Очистка буфера с изображением
            # 3. Воспроизведение видеопотока с реальным колмчеством FPS
            if key == 'metadata' or key == 'clear_image_buffer' or key == 'real_time':
                # Проверка значения
                if type(val) is not bool:
                    continue

                curr_valid_layer += 1

            # Размер окна для масштабирования
            if key == 'resize':
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

                    # Ширина изображения/окна для масштабирования
                    if k == 'width':
                        curr_valid_layer_2 += 1

                    # Высота изображения/окна для масштабирования
                    if k == 'height':
                        all_layer_2 += 1
                        curr_valid_layer_2 += 1

                if all_layer_2 == curr_valid_layer_2:
                    curr_valid_layer += 1

            # 1. Цвет текстов
            # 2. Цвет фона текстов
            if key == 'text_color' or key == 'background_color':
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
                    # 1. Зеленый
                    # 1. Синий
                    if k == 'red' or k == 'green' or k == 'blue':
                        curr_valid_layer_2 += 1

                if all_layer_2 == curr_valid_layer_2:
                    curr_valid_layer += 1

            # Имя окна
            if key == 'window_name':
                # Проверка значения
                if type(val) is not str or not val:
                    continue

                curr_valid_layer += 1

            # Коэффициент масштабирования шрифта, который умножается на размер шрифта
            if key == 'labels_scale':
                # Проверка значения
                if type(val) is not float or val < 0.0 or val > 2.0:
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
    def __load_config_json(self, out = True):
        """
        Загрузка и проверка конфигурационного файла

        ([bool]) -> bool

        Аргументы:
           out - Печатать процесс выполнения

        Возвращает: True если файл загружен и валиден, в обратном случае False
        """

        # Проверка аргументов
        if type(out) is not bool:
            return False

        # Конфигурационный файл передан
        if self._args['config'] is not None:
            config_json = self._json.load(self._args['config'], False, out)  # Загрузка JSON файла
        else:
            # Загрузка JSON файла из ресурсов модуля
            config_json = self._json.load_resources(configs, 'config.json', out)

        # Конфигурационный файл не загружен
        if config_json is None:
            return False

        # Проверка конфигурационного файла на валидность
        res_valid_json_config = self.__valid_json_config(config_json, out)

        # Конфигурационный файл не валидный
        if res_valid_json_config is False:
            return False

        # Проход по всем разделам конфигурационного файла
        for k, v in config_json.items():
            # Добавление значения из конфигурационного файла в словарь аргументов командной строки
            self._args[k] = v

        return True

    # Автоматическая проверка конфигурационного файла в момент работы программы
    def __update_config_json(self):
        """
        Автоматическая проверка конфигурационного файла в момент работы программы

        () -> None

        Возвращает: None
        """

        # Автоматическая проверка конфигурационного файла в момент работы программы
        if self._args['automatic_update'] is True and self._frames_to_update % self._args['frames_to_update'] is 0:
            self._frames_to_update = 0  # Сброс счетчика автоматической проверки конфигурационного файла

            curr_window_name = self._args['window_name']  # Текущее значение имени окна
            curr_resize = self._args['resize']  # Текущее значение размеров окна

            # Загрузка и проверка конфигурационного файла не прошла
            if self.__load_config_json(False) is False:
                # Конфигурационный файл был валидный на прошлой проверке
                if self._automatic_update['invalid_config_file'] is False:
                    # Необходимые значения в конфигурационном файле не найдены в момент работы программы
                    self._automatic_update['invalid_config_file'] = True
            else:
                # Необходимые значения в конфигурационном файле найдены в момент работы программы
                self._automatic_update['invalid_config_file'] = False

                # Имя окна было изменено
                if curr_window_name != self._args['window_name']:
                    self._viewer.set_window_name(self._args['window_name'])  # Установка имени окна

                # Ширина и высота нулевые
                if self._args['resize']['width'] == 0 and self._args['resize']['height'] == 0:
                    self._args['resize']['height'] = self._curr_frame.shape[0]  # Высота изображения
                    self._args['resize']['width'] = self._curr_frame.shape[1]  # Ширина изображения

                # Размер окна был изменен
                if curr_resize['width'] != self._args['resize']['width'] \
                        or curr_resize['height'] != self._args['resize']['height']:
                    # Установка размеров текущего окна
                    self._viewer.set_window_size(self._args['resize']['width'], self._args['resize']['height'])

                self._viewer.clear_image_buffer = self._args['clear_image_buffer']  # Очистка буфера с изображением

        # Увеличение счетчика автоматической проверки конфигурационного файла в момент работы программ
        self._frames_to_update += 1

    # Захват фото/видеоданных
    def __grab_data(self, out = True):
        """
        Захват фото/видеоданных

        ([bool]) -> bool

        Аргументы:
           out - Печатать процесс выполнения

        Возвращает: True если захват фото/видеоданных произведен, в обратном случае False
        """

        # Проверка аргументов
        if type(out) is not bool:
            return False

        frame = None  # Кадр

        try:
            # Воспроизведение WEB-камеры
            self._args['file'] = int(self._args['file'])  # Попытка приведения названия файла к числу

            if self._args['file'] is not 0:
                return False

            # Вывод сообщения
            if out is True:
                print(self._run_web.format(datetime.now().strftime(self._format_time)))

            self._cap = cv2.VideoCapture(self._args['file'])  # Открытие камеры для захвата видеопотока
            has_frame, frame = self._cap.read()  # Захват, декодирование и возврат кадра

            # Текущий кадр не получен
            if not has_frame:
                # Вывод сообщения
                if out is True:
                    print(self._web_not_found.format(
                        self.red, datetime.now().strftime(self._format_time), self.end
                    ))

                return False

            self._source = self._formats_data[0]  # Воспроизведение с WEB-камеры
        except ValueError:
            _, ext = os.path.splitext(self._args['file'])  # Расширение файла

            # Поиск файла
            if self._json.search_file(self._args['file'], ext.replace('.', '')) is False:
                return False

            # Поддерживаемые фото/видео форматы не найдены
            if (ext.replace('.', '') not in self._supported_video_formats
                    and ext.replace('.', '') not in self._supported_photo_formats):
                # Вывод сообщения
                if out is True:
                    print(self._wrong_extension.format(
                        self.red, datetime.now().strftime(self._format_time), self.end,
                        ', '.join(x for x in self._supported_photo_formats),
                        ', '.join(x for x in self._supported_video_formats)
                    ))

                return False

            # Воспроизведение видеопотока
            if ext.replace('.', '') in self._supported_video_formats:
                # Открытие камеры для захвата видеопотока
                self._cap = cv2.VideoCapture(self._args['file'])

                has_frame, frame = self._cap.read()  # Захват, декодирование и возврат кадра

                # Текущий кадр не получен
                if not has_frame:
                    # Вывод сообщения
                    if out is True:
                        print(self._video_not_read.format(
                            self.red, datetime.now().strftime(self._format_time), self.end
                        ))

                    return False

                self._source = self._formats_data[1]  # Воспроизведение с видеофайла

            # Воспроизведение фото данных
            if ext.replace('.', '') in self._supported_photo_formats:
                # Загрузка входного изображения
                self._cap = cv2.imread(self._args['file'])

                # Текущее фото не получено
                if self._cap is None:
                    # Вывод сообщения
                    if out is True:
                        print(self._photo_not_read.format(
                            self.red, datetime.now().strftime(self._format_time), self.end
                        ))

                    return False

                self._source = self._formats_data[2]  # Воспроизведение с фото данных

                frame = self._cap  # Текущий кадр

        self._curr_frame = frame  # Текущий кадр

        return True

    # Циклическое получение кадров из видеопотока
    def __loop(self, out = True):
        """
        Циклическое получение кадров из фото/видеопотока

        ([bool]) -> bool

        Аргументы:
           out - Печатать процесс выполнения

        Возвращает: True если получение кадров осуществляется, в обратном случае False
        """

        # Проверка аргументов
        if type(out) is not bool:
            return False

        start_time = time.time()  # Отсчет времени выполнения

        self.__update_config_json()  # Автоматическая проверка конфигурационного файла в момент работы программы

        # Блокировка отображения повторных раз фото
        if self._frame_count > 1 and self._source == self._formats_data[2] and self._viewer.clear_image_buffer is False:
            return True

        # Распознавание лиц на видеопотоке или WEB-камере
        if self._source != self._formats_data[2]:
            has_frame, frame = self._cap.read()  # Захват, декодирование и возврат кадра

            # Текущий кадр не получен
            if not has_frame:
                return -1  # Прерывание цикла
        else:
            frame = self._cap  # Изображение
            self._viewer.clear_image_buffer = self._args['clear_image_buffer']  # Очистка буфера с изображением

        self._frame_count += 1  # Номер текущего кадра

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Преобразование изображения

        # Принудительная задержка для воспроизведения видеопотока с реальным колмчеством FPS
        if self._args['real_time'] is True:
            end_time = time.time() - start_time  # Конец времени выполнения

            delay = 1 / self._cap.get(cv2.CAP_PROP_FPS)  # Задержка

            # Необходимо произвести задержку видеопотока
            if delay > end_time:
                time.sleep(delay - end_time)  # Принудительная задержка

        fps = round(1 / (time.time() - start_time), 2)  # FPS

        # Количество кадров больше 60
        if fps > 60:
            label_fps = self._frame_rate_static   # Текст с стическим FPS
        else:
            label_fps = self._frame_rate.format(fps)  # Текст с FPS

        # Процесс нанесения информации на изображение
        # Размеры текста
        labels_size = cv2.getTextSize(label_fps, self._labels_font, self._args['labels_scale'], self._labels_thickness)[0]

        # Верхняя левая точка прямоугольника
        fps_point1 = (self._labels_base_coords[0], self._labels_base_coords[1])
        # Нижняя правая точка прямоугольника
        fps_point2 = (
            self._labels_base_coords[0] + labels_size[0] + self._labels_padding * 2,
            self._labels_base_coords[1] + labels_size[1] + self._labels_padding * 2
        )

        # Рисование прямоугольной области в виде фона текста на изображении
        cv2.rectangle(
            frame,  # Исходная копия изображения
            fps_point1,  # Верхняя левая точка прямоугольника
            fps_point2,  # Нижняя правая точка прямоугольника
            # Цвет прямоугольника
            (self._args['background_color']['red'],
             self._args['background_color']['green'],
             self._args['background_color']['blue']),
            cv2.FILLED,  # Толщина рамки прямоугольника
            cv2.LINE_AA  # Тип линии
        )

        # Нанесение FPS на кадр
        cv2.putText(
            frame, label_fps, (self._labels_base_coords[0] + self._labels_padding,
             self._labels_base_coords[1] + self._labels_padding + labels_size[1]),
            self._labels_font, self._args['labels_scale'],
            (self._args['text_color']['red'], self._args['text_color']['green'], self._args['text_color']['blue']),
            self._labels_thickness,
            cv2.LINE_AA
        )

        self._viewer.image_buffer = frame  # Отправка изображения в буфер

        return True

    # ------------------------------------------------------------------------------------------------------------------
    #  Внешние методы
    # ------------------------------------------------------------------------------------------------------------------

    def run(self):
        self._args = self.__build_args()  # Построение аргументов командной строки

        self.clear_shell(self._args['no_clear_shell'])  # Очистка консоли перед выполнением

        # Загрузка и проверка конфигурационного файла
        if self.__load_config_json() is False:
            return False

        # Запуск
        if self._args['metadata'] is True:
            print(self._metadata.format(
                datetime.now().strftime(self._format_time),
                pvv.__author__,
                pvv.__email__,
                pvv.__maintainer__,
                pvv.__version__
            ))

        # Захват фото/видеоданных
        if self.__grab_data() is False:
            return False

        self._viewer.window_name = self._args['window_name']  # Установка имени окна

        # Ширина и высота нулевые
        if self._args['resize']['width'] == 0 and self._args['resize']['height'] == 0:
            self._args['resize']['height'] = self._curr_frame.shape[0]  # Высота изображения
            self._args['resize']['width'] = self._curr_frame.shape[1]  # Ширина изображения

        self._viewer.window_width = self._args['resize']['width']  # Установка ширины окна 
        self._viewer.window_height = self._args['resize']['height']  # Установка высоты окна

        self._viewer.set_loop(self.__loop)  # Циклическая функция извлечения изображений
        self._viewer.start()  # Запуск


if __name__ == "__main__":
    main = Run()

    main.run()
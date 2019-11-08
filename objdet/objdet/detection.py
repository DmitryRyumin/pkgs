#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Поиск объектов
"""

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
import os                # Работа с файловой системой
import numpy as np       # Научные вычисления
import tensorflow as tf  # Библиотека машинного обучения
import pkg_resources     # Работа с ресурсами внутри пакетов

from datetime import datetime                    # Работа со временем
from distutils.version import StrictVersion      # Сравнение версий
from tensorflow.python.client import device_lib  # Интерфейс для создания серверов TensorFlow
from google.protobuf import message              # Сообщения об ошибках Google

# Персональные
from core2pkgs import config as cfg         # Глобальный файл настроек
from filem.file_manager import FileManager  # Работа с файлами

from objdet.api.utils import label_map_util  # Функции для работы с метками объектов
from objdet.api.utils import ops as utils_ops

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Порог регистрации сообщений TensorFlow

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

        self._check_curr_ver_tf = '[{}] Проверка текущей версии TensorFlow ...'
        self._ver_tf_error = '[{}{}{}] Пожалуйста, обновите TensorFlow до версии "{}" или более поздней версии! ...'
        self._ver_tf_valid = '[{}] Версия TensorFlow "{}" актуальна ...'
        self._device_not_found = '[{}{}{}] Доступные GPU/CPU устройства не найдены ...'
        self._gpu_not_found = '[{}{}{}] Доступные GPU устройства не найдены (переход на использование CPU) ...'
        self._load_model = '[{}] Загрузка модели ...'
        self._not_load_model = '[{}{}{}] Модель не загружена ...'
        self._load_labels = '[{}] Загрузка меток ...'
        self._not_load_labels = '[{}{}{}] Метки не загружены ...'


# ######################################################################################################################
# Поиск объектов
# ######################################################################################################################
class Detection(Messages):
    """Класс для поиска объектов"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()  # Выполнение конструктора из суперкласса

        self._min_tf_version = '2.0.0'  # Минимальная версия TensorFlow

        self.title_ru = 'Поиск объектов'  # Установка названия на русском
        self.title_en = 'Objects detection'  # Установка названия на английском

        self._sess = None  # Начало сеанса для выполнения операций

        self._detection_graph = None  # Граф

        self._labels = None  # Метки объектов

        self._device = None  # Список устройств для выполнения процесса поиска объектов

        self._file_manager = FileManager()  # Работа с файлами

        # Необходимые расширения для моделей
        self._required_extension_models = (
            'pbtxt', 'pb',  # Поиск объектов с помощью глубокого обучения в OpenCV (TensorFlow)
        )

        self._path_to_models = pkg_resources.resource_filename('objdet', 'models')  # Путь к моделям

        # Названия моделей и их конфигурационных файлов
        self._path_to_files_models = {
            'coco': {
                'path_to_model': 'coco/frozen_inference_graph.pb',
                'path_to_config_model': 'coco/mscoco_label_map.pbtxt'
            },
        }

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

    # Получение сеанса
    @property
    def sess(self):
        return self._sess

    # Получение меток объектов
    @property
    def labels(self):
        return self._labels

    # ------------------------------------------------------------------------------------------------------------------
    #  Внутренние методы
    # ------------------------------------------------------------------------------------------------------------------

    # Проверка текущей версии TensorFlow на валидность
    def __get_version_tf_valid(self, out = True):
        """
        Проверка текущей версии TensorFlow на валидность

        ([bool]) -> bool

        Аргументы:
            out - Печатать процесс выполнения

        Возвращает: True если текущая версия TensorFlow валидная, в обратном случае False
        """

        # Проверка аргументов
        if type(out) is not bool:
            return False

        # Вывод сообщения
        if out is True:
            print(self._check_curr_ver_tf.format(datetime.now().strftime(self._format_time)))

        # Если версия TensorFlow меньше необходимой
        if StrictVersion(tf.__version__) < StrictVersion(self._min_tf_version):
            # Вывод сообщения
            if out is True:
                print(self._ver_tf_error.format(self.red, datetime.now().strftime(self._format_time), self.end,
                                                self._min_tf_version))

            return False

        # Вывод сообщения
        if out is True:
            print(self._ver_tf_valid.format(datetime.now().strftime(self._format_time), StrictVersion(tf.__version__)))

        return True

    # Получение списка доступных устройств
    def __get_available_devices(self, out = True):
        """
        Получение списка доступных устройств

        ([bool]) -> list

        Аргументы:
            out - Печатать процесс выполнения

        Возвращает: Список устройств для выполнения процесса поиска объектов
        """

        # Проверка аргументов
        if type(out) is not bool:
            return False

        # Получение списка доступных устройств, доступных в локальном процессе
        local_devices_protos = device_lib.list_local_devices()

        gpu = []  # Список графических устройств
        cpu = []  # Список центральных процессоров

        # Извлечь из списка устройства
        for device in local_devices_protos:
            # Графическое устройство
            if device.device_type == 'GPU':
                gpu.append(device.name)  # Устройство

            # Центральный процессор
            if device.device_type == 'CPU':
                cpu.append(device.name)  # Устройство

        # Графические устройства не найдены
        if len(gpu) == 0:
            # Центральные процессоры не найдены
            if len(cpu) == 0:
                # Вывод сообщения
                if out is True:
                    print(
                        self._device_not_found.format(self.red, datetime.now().strftime(self._format_time), self.end))

                return None

            # Вывод сообщения
            if out is True:
                print(
                    self._gpu_not_found.format(self.red, datetime.now().strftime(self._format_time), self.end))

            return cpu  # Список центральный процессоров

        return gpu  # Список графических устройств

    # ------------------------------------------------------------------------------------------------------------------
    #  Внешние методы
    # ------------------------------------------------------------------------------------------------------------------

    # Запуск
    def start(self, out = True):
        """
        Запуск

        ([bool]) -> bool

        Аргументы:
            out - Печатать процесс выполнения

        Возвращает: True если запуск произведен успешно, в обратном случае False
        """

        # Проверка аргументов
        if type(out) is not bool:
            return False

        # Проверка текущей версии TensorFlow на валидность
        if self.__get_version_tf_valid(out) is False:
            return False

        self._device = self.__get_available_devices(out)  # Список устройств для выполнения процесса поиска объектов

        # Устройства не найдены
        if self._device is None:
            return False

        tf.device(self._device[0])  # Выполнение всех операций на доступном устройстве

        return True

    # Загрузка модели для поиска объектов
    def load_model(self, path_to_model = None, path_to_config_model = None, out = True):
        """
        Загрузка модели для поиска объектов

        (str, str [, bool]) -> bool

        Аргументы:
            path_to_model        - Путь к модели
            path_to_config_model - Путь к конфигурационному файлу модели
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
                or not path_to_config_model or type(out) is not bool:
            # Вывод сообщения
            if out is True:
                print(self._invalid_arguments.format(
                    self.red, datetime.now().strftime(self._format_time),
                    self.end, __class__.__name__ + '.' + self.load_model.__name__
                ))

            return False

        # Путь к модели по умолчанию
        if path_to_model is none:
            path_to_model = self._path_to_models + '/' + self._path_to_files_models['coco']['path_to_model']

        # Путь к конфигурационному файлу модели по умолчанию
        if path_to_config_model is none:
            path_to_config_model = self._path_to_models + '/' \
                                   + self._path_to_files_models['coco']['path_to_config_model']

        # Файл модели не найден
        if self._file_manager.search_file(path_to_model, self._required_extension_models[1], False, out) is False:
            return False

        # Конфигурационный файл модели не найден
        if self._file_manager.search_file(
            path_to_config_model, self._required_extension_models[0], False, out
        ) is False:
            return False

        # Вывод сообщения
        if out is True:
            print(self._load_model.format(datetime.now().strftime(self._format_time)))

        tf.compat.v1.reset_default_graph()  # Очистка графа

        detection_graph = tf.Graph()  # Создание нового пустого графа

        # Созданный пустой граф по умолчанию
        with detection_graph.as_default():
            od_graph_def = tf.compat.v1.GraphDef()  # Граф для загрузки модели

            # Работа с моделью без блокировки потока
            with tf.io.gfile.GFile(path_to_model, 'rb') as model:
                serialized_graph = model.read()  # Получение содержимого файла с моделью в виде строки

                try:
                    od_graph_def.ParseFromString(serialized_graph)
                except message.DecodeError:
                    # Вывод сообщения
                    if out is True:
                        print(self._not_load_model.format(
                            self.red, datetime.now().strftime(self._format_time), self.end
                        ))

                    return False

                tf.import_graph_def(od_graph_def, name = '')  # Импорт считанной модели

        # Вывод сообщения
        if out is True:
            print(self._load_labels.format(datetime.now().strftime(self._format_time)))

        try:
            # Загрузка меток объектов
            labels = label_map_util.create_category_index_from_labelmap(
                path_to_config_model, use_display_name = True
            )
        except ValueError:
            # Вывод сообщения
            if out is True:
                print(self._not_load_labels.format(
                    self.red, datetime.now().strftime(self._format_time), self.end
                ))

            return False

        self._detection_graph = detection_graph  # Граф

        self._sess = tf.compat.v1.Session(graph=self._detection_graph)  # Начало сеанса для выполнения операций

        self._labels = labels  # Метки объектов

        return True

    # Поиск объектов
    def objects(self, frame, conf_threshold = 0.7, out = True):
        """
        Поиск объектов

        (numpy.ndarray [, int, int, float, bool]) -> dict

        Аргументы:
            frame          - Изображение
            conf_threshold - Доверительный порог
            out            - Печатать процесс выполнения

        Возвращает словарь распознанных объектов с подробной информацией
        """

        # Проверка аргументов
        if (type(frame) is not np.ndarray or len(frame) is 0 or type(conf_threshold) is not float or conf_threshold < 0
                or conf_threshold > 1 or type(out) is not bool):
            # Вывод сообщения
            if out is True:
                print(self._invalid_arguments.format(
                    self.red, datetime.now().strftime(self._format_time), self.end,
                    __class__.__name__ + '.' + self.objects.__name__
                ))

            return None

        # Получение дескрипторов входных и выходных тензоров
        ops = self._sess.graph.get_operations()
        all_tensor_names = {output.name for op in ops for output in op.outputs}

        tensor_dict = {}  # Словарь выходных детекторов объектов

        for key in [
            'num_detections',     # Количество обнаруженных объектов
            'detection_boxes',    # Координаты обнаруженных объектов
            'detection_scores',   # Точность обнаруженных объектов
            'detection_classes',  # Названия обнаруженных объектов
            'detection_masks'     # Маски сегментаций обнаруженных объектов
        ]:
            tensor_name = key + ':0'
            if tensor_name in all_tensor_names:
                tensor_dict[key] = self._sess.graph.get_tensor_by_name(tensor_name)

        # Маски сегментаций обнаруженных объектов присутствуют
        if 'detection_masks' in tensor_dict:
            # Обработка изображения
            detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
            detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])

            # Перевод маски в координаты изображения и определение размера изображения
            real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
            detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
            detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
            detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                detection_masks, detection_boxes, frame.shape[0], frame.shape[1]
            )
            detection_masks_reframed = tf.cast(tf.greater(detection_masks_reframed, 0.5), tf.uint8)
            tensor_dict['detection_masks'] = tf.expand_dims(detection_masks_reframed, 0)

        image_tensor = self._sess.graph.get_tensor_by_name('image_tensor:0')

        # Выполнение вывода
        output_dict = self._sess.run(tensor_dict, feed_dict = {image_tensor: np.expand_dims(frame, 0)})

        # Все массивы с плавающей запятой float32, поэтому конвертировать типы по мере необходимости
        output_dict['num_detections'] = int(output_dict['num_detections'][0])
        output_dict['detection_classes'] = output_dict['detection_classes'][0].astype(np.uint8)
        output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
        output_dict['detection_scores'] = output_dict['detection_scores'][0]
        if 'detection_masks' in output_dict:
            output_dict['detection_masks'] = output_dict['detection_masks'][0]

        objects = {}  # Словарь распознанных объектов с подробной информацией

        for index, value in enumerate(output_dict['detection_classes']):
            # Доверительный порог равен или больше заданного
            if output_dict['detection_scores'][index] >= conf_threshold:
                # Вычисление координат
                y_min, x_min, y_max, x_max = tuple(output_dict['detection_boxes'][index].tolist())

                # Нормализация координат
                left, right, top, bottom = tuple(map(
                        lambda x: isinstance(x, float) and int(round(x, 0)) or x,
                        (x_min * frame.shape[1], x_max * frame.shape[1], y_min * frame.shape[0], y_max * frame.shape[0])
                    ))

                # Информация об объекте
                info_object = {
                    'id': self.labels.get(value)['id'],                      # Идентификатор
                    'scores': output_dict['detection_scores'][index],        # Точность
                    'boxes': [int(left), int(right), int(top), int(bottom)]  # Координаты
                }

                # В словаре текущего объекта не найдено
                if objects.get(self.labels.get(value)['name']) is None:
                    # Добавление объекта в словарь
                    objects.update(dict.fromkeys([self.labels.get(value)['name']], [
                        info_object  # Информация об объекте
                    ]))
                else:
                    # Добавление объекта в уже существующий объект
                    objects[self.labels.get(value)['name']].append(
                        info_object  # Информация об объекте
                    )

        return objects  # Результат

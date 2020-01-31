#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Воспроизведение видеоданных из сенсора Kinect 2
"""

# ######################################################################################################################
# Заглушка
# ######################################################################################################################

import sys  # Доступ к некоторым переменным и функциям Python

MIN_OS_WINDOWS = (8, 0)

# linux или OS X
if sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
    raise RuntimeError("Требуется операционная система Windows >= {}.{}".format(MIN_OS_WINDOWS[0], MIN_OS_WINDOWS[1]))

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
import time         # Работа со временем
import numpy as np  # Научные вычисления
import cv2          # Алгоритмы компьютерного зрения

from datetime import datetime  # Работа со временем

# Персональные
from core2pkgs import config as cfg  # Глобальный файл настроек
from kinect2pvv.core import PyKinectRuntime, PyKinectV2  # Работа с Kinect 2


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

        self._run_kinect = '[{}] Запуск сенсора Kinect 2 ...'
        self._kinect_not_found = '[{}{}{}] Достигнут лимит ожидания запуска сенсора Kinect 2 в {} секунд ...'


# ######################################################################################################################
# Воспроизведение видеоданных из сенсора Kinect 2
# ######################################################################################################################
class KinectViewer(Messages):
    """Класс для Воспроизведения видеоданных из сенсора Kinect 2"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()  # Выполнение конструктора из суперкласса

        self._kinect = None  # Kinect 2

        self._wait = 10  # Количество секунд для ожидания включения Kinect 2

    # ------------------------------------------------------------------------------------------------------------------
    # Свойства
    # ------------------------------------------------------------------------------------------------------------------

    # Получение Kinect 2
    @property
    def kinect(self):
        return self._kinect

    # ------------------------------------------------------------------------------------------------------------------
    #  Внешние методы
    # ------------------------------------------------------------------------------------------------------------------

    # Запуск
    def start(self, out = True):
        """
        Запуск Kinect 2

        ([bool, bool]) -> bool

        Аргументы:
           out - Печатать процесс выполнения

        Возвращает: True если запуск Kinect произведен, в обратном случае False
        """

        # Проверка аргументов
        if type(out) is not bool:
            return False

        # Вывод сообщения
        if out is True:
            print(self._run_kinect.format(datetime.now().strftime(self._format_time)))

        # Инициализация Kinect 2 на получение цветного изображения, карты глубины и скелетных моделей
        # noinspection PyUnreachableCode
        self._kinect = PyKinectRuntime.PyKinectRuntime(
            PyKinectV2.FrameSourceTypes_Color
            | PyKinectV2.FrameSourceTypes_Body
            | PyKinectV2.FrameSourceTypes_Depth
            | PyKinectV2.FrameSourceTypes_Infrared
            | PyKinectV2.FrameSourceTypes_BodyIndex
        )

        start_time = time.time()  # Отсчет времени выполнения

        # Ожидаем получение информации из Kinect 2
        while True:
            if self._kinect.has_new_color_frame() and \
                    self._kinect.has_new_depth_frame() and \
                    self._kinect.has_new_infrared_frame():
                return True

            end_time = round(time.time() - start_time, 2)  # Конец времени выполнения

            if end_time >= self._wait:
                # Вывод сообщения
                if out is True:
                    print(self._kinect_not_found.format(
                        self.red, datetime.now().strftime(self._format_time), self.end, self._wait
                    ))

                return False

    # Получение цветного кадра из Kinect 2
    def get_color_frame(self):
        """
        Получение цветного кадра из Kinect 2

        () -> numpy.ndarray

        Возвращает: Цветной кадр
        """

        out_frame = self.kinect.get_last_color_frame()  # Получение цветного кадра с Kinect

        # Преобразование кадра в необходимый формат (1920, 1080, RGB)
        out_frame = cv2.cvtColor(
            cv2.cvtColor(out_frame.reshape(1080, 1920, -1).astype(np.uint8), cv2.COLOR_RGBA2RGB), cv2.COLOR_BGR2RGB
        )

        return out_frame  # Результат

    # Получение карты глубины из Kinect 2
    def get_depth_frame(self):
        """
        Получение карты глубины из Kinect 2

        () -> numpy.ndarray

        Возвращает: Карту глубины в цветном формате
        """

        out_frame = self.kinect.get_last_depth_frame()  # Получение карты глубины с Kinect

        # Преобразование карты глубины в необходимый формат (512, 424)
        out_frame = out_frame.reshape(((424, 512))).astype(np.uint16)

        out_frame = cv2.applyColorMap(cv2.convertScaleAbs(out_frame, alpha = 255 / (4500 - 500)), cv2.COLORMAP_JET)

        return out_frame  # Результат

    # Получение инфракрасного кадра из Kinect 2
    def get_infrared_frame(self):
        """
        Получение инфракрасного кадра из Kinect 2

        () -> numpy.ndarray

        Возвращает: Инфракрасный кадр преобразованный под цветной формат
        """

        out_frame = self.kinect.get_last_infrared_frame()  # Получение инфракрасного кадра с Kinect

        # Преобразование инфракрасного кадра в необходимый формат (512, 424)
        out_frame = out_frame.reshape(((424, 512))).astype(np.uint16)

        out_frame = cv2.cvtColor(cv2.convertScaleAbs(out_frame, alpha = 255 / 65535), cv2.COLOR_GRAY2RGB)

        return out_frame  # Результат

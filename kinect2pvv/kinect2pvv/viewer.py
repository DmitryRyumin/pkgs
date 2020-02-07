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
from _testcapi import USHRT_MAX  # Максимально доступное число для формата ushort

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

        self._cnt_bodies = 0  # Количество найденных скелетов

        self._skeleton_landmarks_color = {}  # Ориентиры скелетов для соединения линиями
        self._skeleton_landmarks_depth = {}  # Ориентиры скелетов карт глубины

    # ------------------------------------------------------------------------------------------------------------------
    # Свойства
    # ------------------------------------------------------------------------------------------------------------------

    # Получение Kinect 2
    @property
    def kinect(self):
        return self._kinect

    # ------------------------------------------------------------------------------------------------------------------
    #  Внутренние методы
    # ------------------------------------------------------------------------------------------------------------------

    # Извлечение кординат скелетной точки
    def __draw_body_bone_color(self, joint_points, joints, joint):
        """
        Извлечение кординат скелетной точки

        TODO: Описание
        """

        # TODO: Проверка аргументов

        joint_state = joints[joint].TrackingState  # Отслеживание состояние сустава

        # Координаты сустава не отслежены
        if joint_state == PyKinectV2.TrackingState_NotTracked or joint_state == PyKinectV2.TrackingState_Inferred:
            return None

        # Координаты сустава
        return {
            'x': int(joint_points[joint].x),
            'y': int(joint_points[joint].y)
        }

    # Извлечение кординат скелетной точки из карты глубины
    def __draw_body_bone_depth(self, joint_points, joints, joint):
        """
        Извлечение кординат скелетной точки из карты глубины

        TODO: Описание
        """

        # TODO: Проверка аргументов

        joint_state = joints[joint].TrackingState  # Отслеживание состояние сустава

        # Координаты сустава не отслежены
        if joint_state == PyKinectV2.TrackingState_NotTracked or joint_state == PyKinectV2.TrackingState_Inferred:
            return None

        x = int(joint_points[joint].x)
        y = int(joint_points[joint].y)
        z = int(self._depth_frame[y * self.kinect.depth_frame_desc.Width + x])

        # Координаты сустава
        return {
            'x': x,
            'y': y,
            'z': z
        }

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
    def get_infrared_frame(self, norm = 0.32, out = True):
        """
        Получение инфракрасного кадра из Kinect 2

        ([float]) -> numpy.ndarray

        Аргументы:
           norm - Нормализация значений инфракрасной камеры

        Возвращает: Инфракрасный кадр преобразованный под цветной формат
        """

        # Проверка аргументов
        if type(norm) is not float or norm < 0.01 or norm > 1 or type(out) is not bool:
            # Вывод сообщения
            if out is True:
                print(self._invalid_arguments.format(
                    self.red, datetime.now().strftime(self._format_time), self.end,
                    __class__.__name__ + '.' + self.get_infrared_frame.__name__
                ))

            return None

        out_frame = self.kinect.get_last_infrared_frame()  # Получение инфракрасного кадра с Kinect

        # Преобразование инфракрасного кадра в необходимый формат (512, 424)
        out_frame = out_frame.reshape(((424, 512))).astype(np.uint16)

        # Нормализация значений инфракрасной камеры
        if norm < 1.0:
            out_frame = cv2.max(
                0.01, cv2.min(
                    1.0, (out_frame / USHRT_MAX) / norm
                )
            ) * USHRT_MAX

        out_frame = cv2.cvtColor(cv2.convertScaleAbs(out_frame, alpha = 255 / USHRT_MAX), cv2.COLOR_GRAY2RGB)

        return out_frame  # Результат

    # Получение ориентиров скелета
    def get_bodies(self):
        """
        Получение ориентиров скелета

        () ->

        Возвращает: Словари с ориентирами скелетов в цветном формате и карте глубины
        """

        bodies = self.kinect.get_last_body_frame()  # Получение ориентиров скелета

        out_joints_color = {}  # Словарь с найдеными скелетами
        out_joints_depth = {}  # Словарь с найдеными скелетами карты глубины

        self._cnt_bodies = 0  # Обнуление количества найденных скелетов

        # Ориентиры скелета возможно присутствуют
        if bodies is not None:
            # Пройтись по всем возможным скелетам
            for i in range(0, self.kinect.max_body_count):
                body = bodies.bodies[i]  # Скелетная модель
                # Скелетная модель не найдена
                if not body.is_tracked:
                    continue

                self._cnt_bodies += 1  # Увеличение счетчика количества найденных скелетов

                temp_joints_color = {}  # Словарь с найденным скелетом
                temp_joints_depth = {}  # Словарь с найденным скелетом карты глубины

                joints = body.joints  # Скелетная модель

                # Получение скелетной модели для цветного кадра
                joint_points_color = self.kinect.body_joints_to_color_space(joints)

                # Получение скелетной модели для карты глубины
                joint_points_depth = self.kinect.body_joints_to_depth_space(joints)

                # Суставы скелетной модели
                joints_type = {
                    'neck': PyKinectV2.JointType_Neck,                     # Шея
                    'spine_shoulder': PyKinectV2.JointType_SpineShoulder,  # Позвоночник на уровне плеч
                    'spine_mid': PyKinectV2.JointType_SpineMid,            # Позвоночник по центру тела
                    'spine_base': PyKinectV2.JointType_SpineBase,          # Позвоночник на уровне ног (центр таза)
                    'shoulder_right': PyKinectV2.JointType_ShoulderRight,  # Правое плечо
                    'elbow_right': PyKinectV2.JointType_ElbowRight,        # Правый локоть
                    'wrist_right': PyKinectV2.JointType_WristRight,        # Правое запястье
                    'shoulder_left': PyKinectV2.JointType_ShoulderLeft,    # Левое плечо
                    'elbow_left': PyKinectV2.JointType_ElbowLeft,          # Левый локоть
                    'wrist_left': PyKinectV2.JointType_WristLeft,          # Левое запястье
                    'hand_right': PyKinectV2.JointType_HandRight,          # Правая рука
                    'hand_left': PyKinectV2.JointType_HandLeft,            # Левая рука
                    'trumb_right': PyKinectV2.JointType_ThumbRight,        # Большой палец правой руки
                    'hand_tip_right': PyKinectV2.JointType_HandTipRight,   # 4 пальца правой руки
                    'trumb_left': PyKinectV2.JointType_ThumbLeft,          # Большой палец левой руки
                    'hand_tip_left': PyKinectV2.JointType_HandTipLeft,     # 4 пальца левой руки
                    'hip_right': PyKinectV2.JointType_HipRight,            # Правое бедро
                    'knee_right': PyKinectV2.JointType_KneeRight,          # Правое колено
                    'ankle_right': PyKinectV2.JointType_AnkleRight,        # Правая лодыжка
                    'foot_right': PyKinectV2.JointType_FootRight,          # Правая нога
                    'hip_left': PyKinectV2.JointType_HipLeft,              # Левое бедро
                    'knee_left': PyKinectV2.JointType_KneeLeft,            # Левое колено
                    'ankle_left': PyKinectV2.JointType_AnkleLeft,          # Левая лодыжка
                    'foot_left': PyKinectV2.JointType_FootLeft,            # Левая нога
                    'head': PyKinectV2.JointType_Head                      # Голова
                }

                # Проход по всем возможным суставам скелетной модели
                for key, val in joints_type.items():
                    # Извлечение кординат скелетной точки
                    temp_joints_color[key] = self.__draw_body_bone_color(joint_points_color, joints, val)

                    # Извлечение кординат скелетной точки карт глубины
                    temp_joints_depth[key] = self.__draw_body_bone_depth(joint_points_depth, joints, val)

                # Добавление скелета в словарь со всеми найденными скелетами
                out_joints_color[self._cnt_bodies] = temp_joints_color  # Цветное изображение
                out_joints_depth[self._cnt_bodies] = temp_joints_depth  # Карта глубины

        # Ориентиры скелетов
        self._skeleton_landmarks_color = out_joints_color  # Цветная камера
        self._skeleton_landmarks_depth = out_joints_depth  # Карта глубины

        print(type(self._skeleton_landmarks_color), self._skeleton_landmarks_depth)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Воспроизведение фото/видео данных
"""

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
import time         # Работа со временем
import threading    # Многопоточность
import cv2          # Алгоритмы компьютерного зрения
import numpy as np  # Научные вычисления

from datetime import datetime  # Работа со временем
from OpenGL import GL, GLUT    # Работа с графикой

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

        self._data_not_received = '[{}{}{}] Данные не получены ...'
        self._program_close = '[{}] Программа закрыта ...'


# ######################################################################################################################
# Воспроизведение фото/видео данных
# ######################################################################################################################
class Viewer(Messages):
    """Класс для воспроизведения фото/видео данных"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(
            self,
            window_name = 'Window',    # Имя окна
            window_width = 1280,       # Ширина окна
            window_height = 720,       # Высота окна
            min_window_width = 100,    # Минимальная ширина окна
            min_window_height = 100,   # Минимальная высота окна
            move_window_x = 30,        # Перемещение окна по оси X
            move_window_y = 30,        # Перемещение окна по оси Y
            clear_image_buffer = True  # Очистка буфера с изображением
    ):
        super().__init__()  # Выполнение конструктора из суперкласса

        self.window_name = window_name

        self._min_window_width = min_window_width
        self._min_window_height = min_window_height

        self.window_width = window_width
        self.window_height = window_height

        self.move_window_x = move_window_x
        self.move_window_y = move_window_y

        self.clear_image_buffer = clear_image_buffer

        self.image_buffer = None  # Буфер с изображением
        self._cnt = 0  # Счетчик кадров
        self._prev_time = time.time()  # Время выполнения

        self._tm = 0

        self._idle_function = None  # Циклическая функция извлечения изображений

    # ------------------------------------------------------------------------------------------------------------------
    # Свойства
    # ------------------------------------------------------------------------------------------------------------------

    # Получение имени окна
    @property
    def window_name(self):
        return self._window_name

    # Установка имени окна
    @window_name.setter
    def window_name(self, name):
        self._window_name = bytes(name, "ascii")

    # Получение ширины окна
    @property
    def window_width(self):
        return self._window_width

    # Установка ширины окна
    @window_width.setter
    def window_width(self, width):
        # Установка минимальной ширины окна
        if width < self._min_window_width:
            self._window_width = self._min_window_width
        else:
            self._window_width = width

    # Получение высоты окна
    @property
    def window_height(self):
        return self._window_height

    # Установка высоты окна
    @window_height.setter
    def window_height(self, height):
        # Установка минимальной высоты окна
        if height < self._min_window_height:
            self._window_height = self._min_window_height
        else:
            self._window_height = height

    # Получение значения перемещения окна по оси X
    @property
    def move_window_x(self):
        return self._move_window_x

    # Установка значения перемещения окна по оси X
    @move_window_x.setter
    def move_window_x(self, x):
        if x < 0:
            self._move_window_x = 0
        else:
            self._move_window_x = x

    # Получение значения перемещения окна по оси Y
    @property
    def move_window_y(self):
        return self._move_window_y

    # Установка значения перемещения окна по оси Y
    @move_window_y.setter
    def move_window_y(self, y):
        if y < 0:
            self._move_window_y = 0
        else:
            self._move_window_y = y

    # Получение результата очистки изображения из буфера
    @property
    def clear_image_buffer(self):
        return self._clear_image_buffer

    # Установка результата очистки изображения из буфера
    @clear_image_buffer.setter
    def clear_image_buffer(self, clear):
        self._clear_image_buffer = clear

    # Получение изображения из буфера
    @property
    def image_buffer(self):
        return self._image_buffer

    # Передача изображения в буфер
    @image_buffer.setter
    def image_buffer(self, img):
        self._image_buffer = img

    # Получение номера изображения
    @property
    def cnt(self):
        return self._cnt

    # ------------------------------------------------------------------------------------------------------------------
    # Внутренние методы
    # ------------------------------------------------------------------------------------------------------------------

    # Отображение изображения (перерисовка окна)
    def __draw(self):
        """
        Отображение изображения (перерисовка окна)
        """

        if self._idle_function is not None:
            if self._idle_function() is -1:
                return None

            if self._idle_function() is False:
                raise SystemExit(self._data_not_received.format(
                    self.red, datetime.now().strftime(self._format_time), self.end
                ))

        # Изображение найдено в буфере
        if self.image_buffer is not None:
            try:
                self._cnt += 1  # Текущий кадр
                if time.time() - self._tm > 1.0:
                    self._tm = time.time()
                    self._cnt = 0  # Сброс текущего кадра
                    for i in threading.enumerate():
                        if i.name == "MainThread":
                            if i.is_alive() is False:
                                raise SystemExit(self._data_not_received.format(
                                    self.red, datetime.now().strftime(self._format_time), self.end
                                ))

                GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)  # Очистка буфера
                GL.glColor3f(1.0, 1.0, 1.0)  # Цвет
                GL.glMatrixMode(GL.GL_PROJECTION)  # Применять матричные операции к стеку проекционных матриц
                GL.glLoadIdentity()  # Единичная матрица
                GL.glOrtho(-1, 1, -1, 1, -1, 1)  # Умножение текущей матрицы на ортографическую матрицу
                GL.glMatrixMode(GL.GL_MODELVIEW)  # Установка текущей матрицы
                GL.glLoadIdentity()  # Единичная матрица
                # Двухмерная текстура изображения
                GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB,
                                self.image_buffer.shape[1], self.image_buffer.shape[0],
                                0, GL.GL_RGB, GL.GL_UNSIGNED_BYTE, self.image_buffer)
                GL.glEnable(GL.GL_TEXTURE_2D)
                GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
                GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
                GL.glBegin(GL.GL_QUADS)
                GL.glTexCoord2d(0.0, 1.0)
                r = self.window_width / self.window_height
                ir = self.image_buffer.shape[1] / self.image_buffer.shape[0]
                x_ratio = 1.0
                y_ratio = 1.0
                if r > ir:
                    x_ratio = ir / r
                else:
                    y_ratio = r / ir
                GL.glVertex3d(-x_ratio, -y_ratio, 0.0)
                GL.glTexCoord2d(1.0, 1.0)
                GL.glVertex3d(x_ratio, -y_ratio, 0.0)
                GL.glTexCoord2d(1.0, 0.0)
                GL.glVertex3d(x_ratio, y_ratio, 0.0)
                GL.glTexCoord2d(0.0, 0.0)
                GL.glVertex3d(-x_ratio, y_ratio, 0.0)
                GL.glEnd()

                GL.glFlush()
            except:
                raise SystemExit(self._data_not_received.format(
                    self.red, datetime.now().strftime(self._format_time), self.end
                ))

            # Очистка изображения из буфера
            # if self.clear_image_buffer is True:
            #     self.image_buffer = None
        else:
            raise SystemExit(self._data_not_received.format(
                self.red, datetime.now().strftime(self._format_time), self.end
            ))

        # Время выполнения
        if time.time() - self._prev_time < 0.008:
            time.sleep(0.005)  # Принудительная задержка

        self._prev_time = time.time()  # Старт времени выполнения

    # Изменение размеров окна
    def __resize(self, width, height):
        """
        Изменение размеров окна

        (int, int) -> None

        Аргументы:
           width - Ширина окна
           height - Высота окна

        Возвращает: None
        """

        # Проверка аргументов
        if type(width) is not int or width < 0 or type(height) is not int or height < 0:
            return None

        self.window_width = width  # Установка ширины окна
        self.window_height = height  # Установка высоты окна

        GL.glViewport(0, 0, width, height)

        return None

    # Обработка нажатий на клавиатуру
    def __keyboard(self, key, x, y):
        """
        Обработка нажатий на клавиатуру

        TODO: Описание
        """

        # TODO: Проверка аргументов

        if type(key) == bytes:
            key = ord(key)
        else:
            key = 0x0100 + key

        if key == 27 or key == b'\x1b':
            raise SystemExit(self._program_close.format(
                datetime.now().strftime(self._format_time)
            ))

    # ------------------------------------------------------------------------------------------------------------------
    # Внешние методы
    # ------------------------------------------------------------------------------------------------------------------

    # Изменение размеров изображения
    def resize_frame(self, frame, width, height, out = True):
        """
        Изменение размеров изображения

        (numpy.ndarray, int, int [, bool]) -> tuple

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
        if type(frame) is not np.ndarray or len(frame) is 0 or type(height) is not int or height < 0 or type(width) is \
                not int or width < 0 or type(out) is not bool:
            # Вывод сообщения
            if out is True:
                print(self._invalid_arguments.format(
                    self.red, datetime.now().strftime(self._format_time), self.end,
                    __class__.__name__ + '.' + self.resize_frame.__name__
                ))

            return None

        frame_clone = frame.copy()  # Копирование изображения

        frame_width = frame_clone.shape[1]  # Ширина изображения
        frame_height = frame_clone.shape[0]  # Высота изображения

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
        frame_resize = cv2.resize(frame_clone, (width, height), interpolation = cv2.INTER_LINEAR)

        # Результат
        return frame_resize, scale_width, scale_height

    # Циклическое извлечение изображений
    def set_loop(self, func):
        """
        Циклическое извлечение изображений

        (method) -> None

        Аргументы:
           func - Метод класса

        Возвращает: None
        """

        # TODO: Проверка аргументов

        self._idle_function = func

    # Запуск
    def start(self):
        """
        Запуск
        """

        GLUT.glutInit([])  # Инициализация библиотеки GLUT
        buffering = GLUT.GLUT_SINGLE  # Вариант буферизации
        color_model = GLUT.GLUT_RGB  # Вариант цветовой модели

        # Инициализация отображения в нужном режимах
        GLUT.glutInitDisplayMode(buffering | color_model | GLUT.GLUT_DEPTH)
        GLUT.glutInitWindowSize(self.window_width, self.window_height)  # Размер окна
        GLUT.glutInitWindowPosition(self.move_window_x, self.move_window_y)  # Позиция окна
        GLUT.glutCreateWindow(self.window_name)  # Создание окна с указанным именем

        GLUT.glutDisplayFunc(self.__draw)  # Отображение изображения (перерисовка окна)
        GLUT.glutIdleFunc(self.__draw)  # Вызывается системой всякий раз, когда приложение простаивает

        GLUT.glutReshapeFunc(self.__resize)  # Изменение размеров окна

        # Обработка нажатий на клавиатуру (клавиши Backspace, Delete и Escape)
        GLUT.glutKeyboardFunc(self.__keyboard)
        GLUT.glutSpecialFunc(self.__keyboard)  # Обработка нажатий на клавиатуру

        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glMatrixMode(GL.GL_PROJECTION)  # Применять матричные операции к стеку проекционных матриц
        GL.glLoadIdentity()  # Единичная матрица
        GL.glOrtho(-1, 1, -1, 1, -1, 1)  # Умножение текущей матрицы на ортографическую матрицу

        GLUT.glutMainLoop()  # Цикл обработки событий GLUT

    # Изменение размеров текущего окна
    def set_window_size(self, width, height):
        """
        Изменение размеров окна

        (int, int) -> None

        Аргументы:
           width - Ширина окна
           height - Высота окна

        Возвращает: None
        """

        # Проверка аргументов
        if type(width) is not int or width < 0 or type(height) is not int or height < 0:
            return None

        self.window_width = width  # Установка ширины окна
        self.window_height = height  # Установка высоты окна

        GLUT.glutReshapeWindow(self.window_width, self.window_height)  # Размер окна

    # Изменение положения текущего окна
    def set_window_move(self, x, y):
        """
        Изменение положения текущего окна

        (int, int) -> None

        Аргументы:
           x - Перемещение окна по оси X
           y - Перемещение окна по оси Y

        Возвращает: None
        """

        # Проверка аргументов
        if type(x) is not int or x < 0 or type(y) is not int or y < 0:
            return None

        self.move_window_x = x  # Перемещение окна по оси X
        self.move_window_y = y  # Перемещение окна по оси Y

        GLUT.glutPositionWindow(self.move_window_x, self.move_window_y)  # Положение окна

    # Изменение имени текущего окна
    def set_window_name(self, name):
        """
        Изменение имени текущего окна

        (str) -> None

        Аргументы:
           name - Имя окна

        Возвращает: None
        """

        # Проверка аргументов
        if type(name) is not str or not name:
            return None

        self.window_name = name  # Установка имени окна

        GLUT.glutSetWindowTitle(self.window_name)  # Имя окна

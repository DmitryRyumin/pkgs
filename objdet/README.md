# Поиск объектов

![PyPI](https://img.shields.io/pypi/v/objdet)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/objdet)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/objdet)
![PyPI - Status](https://img.shields.io/pypi/status/objdet)
![PyPI - License](https://img.shields.io/pypi/l/objdet)

## [История релизов](https://github.com/DmitryRyumin/pkgs/blob/master/objdet/NOTES.md)

## Установка

### Вариант 1

```shell script
pip install objdet  # CPU
```

### Вариант 2

```shell script
pip install objdet --gpu  # GPU (Linux или Windows)
```

## Обновление

### Вариант 1

```shell script
pip install --upgrade objdet  # CPU
```

### Вариант 2

```shell script
pip install --upgrade objdet --gpu  # GPU (Linux или Windows)
```

## Зависимости

| Пакеты | Минимальная версия | Текущая версия |
| ------ | ------------------ | -------------- |
`pvv` | `19.11.12.2` | ![PyPI](https://img.shields.io/pypi/v/pvv) |
`numpy` | `1.17.4` | ![PyPI](https://img.shields.io/pypi/v/numpy) | 
`tensorflow`<br>`tensorflow-gpu` | `2.0.0`<br>`2.0.0` | ![PyPI](https://img.shields.io/pypi/v/tensorflow)<br>![PyPI](https://img.shields.io/pypi/v/tensorflow-gpu) |

## Класс для поиска объектов - [смотреть](https://github.com/DmitryRyumin/pkgs/blob/master/objdet/objdet/detection.py)

<h4 align="center"><span style="color:#EC256F;">Примеры</span></h4>

| Файлы/скрипты | Аргументы командной строки | Описания |
| ------------- | -------------------------- | -------- |
| [detection.py](https://github.com/DmitryRyumin/pkgs/blob/master/objdet/objdet/samples/detection.py)<br>`objdet_play` | `--file str` - Путь к файлу<br>`--config str` - Путь к конфигурационному файлу<br>`--automatic_update` - Автоматическая проверка конфигурационного файла в момент работы программы (работает при заданном `--config`)<br>`--frames_to_update int=25` - Через какое количество шагов проверять конфигурационный файл (работает при `--automatic_update`)<br>`--no_clear_shell` - Не очищать консоль перед выполнением | Поиск объектов |

### [Конфигурационный файл](https://github.com/DmitryRyumin/pkgs/blob/master/objdet/objdet/configs/config.json)

#### Параметры

| Параметры `json` | Типы | Описания | Допустимые значения |
| ---------------- | ---  | -------- | ------------------- |
| metadata | bool | Вывод метаданных | - |
| window_name | str | Имя окна | - |
| path_to_model | str | Путь к модели | - |
| path_to_labels | str | Путь к конфигурационному файлу модели | - |
| size | dict | Размер изображения для масштабирования | - |
| resize | dict | Размер окна для масштабирования | - |
| text_color | dict | Цвет текстов | От `0` до `255` |
| background_color | dict | Цвет фона текстов | От `0` до `255` |
| rectangle_color | dict | Цвет рамки прямоугольника с объектами | От `0` до `255` |
| rectangle_thickness | int | Толщина рамки прямоугольника с объектами | От `1` до `10` |
| label_scale | float | Коэффициент масштабирования шрифта | От `>0.0` до `2.0` |
| labels_thickness | int | Толщина линии шрифта | От `1` до `4` |
| labels_base_coords | int | Начальные координаты текстов | От `0` до `100` |
| labels_padding | int | Внутренний отступ для текстов | От `0` до `30` |
| labels_distance | int | Расстояние между текстами | От `0` до `50` |
| clear_image_buffer | bool | Очистка буфера с изображением | - |
| real_time | bool | Воспроизведение фото/видеопотока с реальным количеством FPS | - |
| conf_threshold | float | Доверительный порог детекции объектами | От `0.0` до `1.0` |
| draw_precent | bool | Рисование на изображении процентов для каждого детектированного объекта | - |
| object_scale | float | Коэффициент масштабирования шрифта (объект - проценты) | От `>0.0` до `2.0` |
| object_thickness | int | Толщина линии шрифта (объект - проценты) | От `1` до `4` |
| object_text_color | dict | Цвет текста объекта - процентов | От `0` до `255` |
| object_background_color | dict | Цвет фона объекта - процентов | От `0` до `255` |
| object_padding | int | Внутренний отступ для объектов - процентов | От `0` до `30` |
| object_margin_bottom | int | Внешний нижний отступ для объектов - процентов | От `0` до `30` |

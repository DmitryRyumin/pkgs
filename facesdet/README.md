# Поиск лиц

![PyPI](https://img.shields.io/pypi/v/facesdet)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/facesdet)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/facesdet)
![PyPI - Status](https://img.shields.io/pypi/status/facesdet)
![PyPI - License](https://img.shields.io/pypi/l/facesdet)

## [История релизов](https://github.com/DmitryRyumin/pkgs/blob/master/facesdet/NOTES.md)

## Установка

```shell script
pip install facesdet
```

### Примечание для Windows

1. Удалить `PyOpenGL`

    ```shell script
    pip uninstall PyOpenGL
    ```

2. Скачать и установить [PyOpenGL](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl)

## Обновление

```shell script
pip install --upgrade facesdet
```

## Зависимости

| Пакеты | Минимальная версия | Текущая версия |
| ------ | ------------------ | -------------- |
`pvv` | `20.1.27.1` | ![PyPI](https://img.shields.io/pypi/v/pvv) |
`numpy` | `1.18.1` | ![PyPI](https://img.shields.io/pypi/v/numpy) | 
`dlib` | `19.19.0` | ![PyPI](https://img.shields.io/pypi/v/dlib) |

## Класс для поиска лиц - [смотреть](https://github.com/DmitryRyumin/pkgs/blob/master/facesdet/facesdet/detection.py)

<h4 align="center"><span style="color:#EC256F;">Примеры</span></h4>

| Файлы/скрипты | Аргументы командной строки | Описания |
| ------------- | -------------------------- | -------- |
| [detection.py](https://github.com/DmitryRyumin/pkgs/blob/master/facesdet/facesdet/samples/detection.py)<br>`facesdet_play` | `--file str=0` - Путь к файлу<br>`--config str` - Путь к конфигурационному файлу<br>`--automatic_update` - Автоматическая проверка конфигурационного файла в момент работы программы (работает при заданном `--config`)<br>`--frames_to_update int=25` - Через какое количество шагов проверять конфигурационный файл (работает при `--automatic_update`)<br>`--no_clear_shell` - Не очищать консоль перед выполнением | Поиск лиц |

### [Конфигурационный файл](https://github.com/DmitryRyumin/pkgs/blob/master/facesdet/facesdet/configs/config.json)

#### Параметры

| Параметры `json` | Типы | Описания | Допустимые значения |
| ---------------- | ---  | -------- | ------------------- |
| metadata | bool | Вывод метаданных | - |
| window_name | str | Имя окна | - |
| method | str | Метод детекции лиц | `opencv_haar`<br>`opencv_dnn`<br>`dlib_hog`<br>`dlib_cnn` |
| min_neighbors | int | Количество соседей для каждого прямоугольника<br>`"method" = opencv_haar` | - |
| dnn | str | Тип нейронной сети<br>`"method" = opencv_dnn` | `tf`<br>`caffe` |
| size | dict | Размер изображения для масштабирования | - |
| resize | dict | Размер окна для масштабирования | - |
| text_color | dict | Цвет текстов | От `0` до `255` |
| background_color | dict | Цвет фона текстов | От `0` до `255` |
| rectangle_color | dict | Цвет рамки прямоугольника с лицами | От `0` до `255` |
| rectangle_thickness | int | Толщина рамки прямоугольника с лицами | От `1` до `10` |
| label_scale | float | Коэффициент масштабирования шрифта | От `>0.0` до `2.0` |
| labels_thickness | int | Толщина линии шрифта | От `1` до `4` |
| labels_base_coords | int | Начальные координаты текстов | От `0` до `100` |
| labels_padding | int | Внутренний отступ для текстов | От `0` до `30` |
| labels_distance | int | Расстояние между текстами | От `0` до `50` |
| clear_image_buffer | bool | Очистка буфера с изображением | - |
| real_time | bool | Воспроизведение фото/видеопотока с реальным количеством FPS | - |
| repeat | bool | Повторение воспроизведения видеопотока | - |
| fps | int | Пользовательский FPS<br>`"real_time" = true` | От `0` до `60` |
| conf_threshold | float | Доверительный порог детекции лиц<br>`"method" = opencv_dnn` | От `0.0` до `1.0` |
| draw_precent | bool | Рисование на изображении процентов для каждого детектированного лица<br>`"method" = opencv_dnn` | - |
| precent_scale | float | Коэффициент масштабирования шрифта (проценты)<br>`"method" = opencv_dnn` | От `>0.0` до `2.0` |
| precent_thickness | int | Толщина линии шрифта (проценты)<br>`"method" = opencv_dnn` | От `1` до `4` |
| precent_text_color | dict | Цвет текста процентов<br>`"method" = opencv_dnn` | От `0` до `255` |
| precent_background_color | dict | Цвет фона процентов<br>`"method" = opencv_dnn` | От `0` до `255` |
| precent_padding | int | Внутренний отступ для процентов<br>`"method" = opencv_dnn` | От `0` до `30` |
| precent_margin_bottom | int | Внешний нижний отступ для процентов<br>`"method" = opencv_dnn` | От `0` до `30` |

#### Горячие клавиши

| Клавиши | Сценарий |
| ------- | -------  |
| `esc` | Закрытие окна приложения |
| `r` | Повторение воспроизведения видеопотока |
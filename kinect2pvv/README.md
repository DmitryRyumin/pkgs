# Воспроизведение видеоданных из сенсора Kinect 2

![PyPI](https://img.shields.io/pypi/v/kinect2pvv)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/kinect2pvv)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/kinect2pvv)
![PyPI - Status](https://img.shields.io/pypi/status/kinect2pvv)
![PyPI - License](https://img.shields.io/pypi/l/kinect2pvv)

## [История релизов](https://github.com/DmitryRyumin/pkgs/blob/master/kinect2pvv/NOTES.md)

## Установка

```shell script
pip install kinect2pvv
```

### Примечание

1. Удалить `PyOpenGL`

    ```shell script
    pip uninstall PyOpenGL
    ```

2. Скачать и установить [PyOpenGL](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl)

## Обновление

```shell script
pip install --upgrade kinect2pvv
```

## Зависимости

| Пакеты | Минимальная версия | Текущая версия |
| ------ | ------------------ | -------------- |
`pvv` | `20.1.29.0` | ![PyPI](https://img.shields.io/pypi/v/pvv) |
`comtypes` | `1.1.7` | ![PyPI](https://img.shields.io/pypi/v/comtypes) |

## Класс воспроизведения видеоданных из сенсора Kinect 2 - [смотреть](https://github.com/DmitryRyumin/pkgs/blob/master/kinect2pvv/kinect2pvv/viewer.py)

<h4 align="center"><span style="color:#EC256F;">Примеры</span></h4>

| Файлы/скрипты | Аргументы командной строки | Описания |
| ------------- | -------------------------- | -------- |
| [play.py](https://github.com/DmitryRyumin/pkgs/blob/master/kinect2pvv/kinect2pvv/samples/play.py)<br>`kinect2pvv_play` | `--config str` - Путь к конфигурационному файлу<br>`--automatic_update` - Автоматическая проверка конфигурационного файла в момент работы программы (работает при заданном `--config`)<br>`--frames_to_update int=25` - Через какое количество шагов проверять конфигурационный файл (работает при `--automatic_update`)<br>`--no_clear_shell` - Не очищать консоль перед выполнением | Воспроизведение видеоданных из сенсора Kinect 2 |

### [Конфигурационный файл](https://github.com/DmitryRyumin/pkgs/blob/master/kinect2pvv/kinect2pvv/configs/config.json)

#### Параметры

| Параметры `json` | Типы | Описания | Допустимые значения |
| ---------------- | ---  | -------- | ------------------- |
| metadata | bool | Вывод метаданных | - |
| window_name | str | Имя окна | - |
| resize | dict | Размер окна для масштабирования | - |
| text_color | dict | Цвет текстов | От `0` до `255` |
| background_color | dict | Цвет фона текстов | От `0` до `255` |
| label_scale | float | Коэффициент масштабирования шрифта | От `>0.0` до `2.0` |
| labels_thickness | int | Толщина линии шрифта | От `1` до `4` |
| labels_base_coords | int | Начальные координаты текстов | От `0` до `100` |
| labels_padding | int | Внутренний отступ для текстов | От `0` до `30` |
| real_time | bool | Воспроизведение фото/видеопотока с реальным количеством FPS | - |
| fps | int | Пользовательский FPS<br>`"real_time" = true` | От `0` до `60` |
| show_depth | bool | Отображение карты глубины | - |
| show_infrared | bool | Отображение инфракрасного кадра | - |
| resize_depth_ir | bool | Размер карты глубины и инфракрасного кадра для масштабирования<br>`"show_depth" = true` или `"show_infrared" = true` | От `0` до `512` |
| labels_base_coords_depth_ir | int | Начальные координаты карты глубины и инфракрасного кадра относительно верхнего правого угла<br>`"show_depth" = true` или `"show_infrared" = true` | От `0` до `100` |
| distance_between_depth_ir | int | Расстояние между картой глубины и инфракрасным кадром<br>`"show_depth" = true` и `"show_infrared" = true` | От `0` до `50` |
| norm_infrared | float | Нормализация значений инфракрасной камеры<br>`"show_infrared" = true` | От `0.01` до `1.0` |

#### Горячие клавиши

| Клавиши | Сценарий |
| ------- | -------  |
| `esc` | Закрытие окна приложения |
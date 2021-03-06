# Воспроизведение фото/видео данных

![PyPI](https://img.shields.io/pypi/v/pvv)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pvv)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/pvv)
![PyPI - Status](https://img.shields.io/pypi/status/pvv)
![PyPI - License](https://img.shields.io/pypi/l/pvv)

## [История релизов](https://github.com/DmitryRyumin/pkgs/blob/master/pvv/NOTES.md)

## Установка

```shell script
pip install pvv
```

### Примечание для Windows

1. Удалить `PyOpenGL`

    ```shell script
    pip uninstall PyOpenGL
    ```

2. Скачать и установить [PyOpenGL](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl)

## Обновление

```shell script
pip install --upgrade pvv
```

## Зависимости

| Пакеты | Минимальная версия | Текущая версия |
| ------ | ------------------ | -------------- |
`filem` | `19.11.12.1` | ![PyPI](https://img.shields.io/pypi/v/filem) |
`opencv-contrib-python` | `4.1.2.30` | ![PyPI](https://img.shields.io/pypi/v/opencv-contrib-python) | 
`PyOpenGL` | `3.1.5` | ![PyPI](https://img.shields.io/pypi/v/PyOpenGL) |

## Класс для воспроизведения фото/видео данных - [смотреть](https://github.com/DmitryRyumin/pkgs/blob/master/pvv/pvv/viewer.py)

<h4 align="center"><span style="color:#EC256F;">Примеры</span></h4>

| Файлы/скрипты | Аргументы командной строки | Описания |
| ------------- | -------------------------- | -------- |
| [play.py](https://github.com/DmitryRyumin/pkgs/blob/master/pvv/pvv/samples/play.py)<br>`pvv_play` | `--file str=0` - Путь к файлу<br>`--config str` - Путь к конфигурационному файлу<br>`--automatic_update` - Автоматическая проверка конфигурационного файла в момент работы программы (работает при заданном `--config`)<br>`--frames_to_update int=25` - Через какое количество шагов проверять конфигурационный файл (работает при `--automatic_update`)<br>`--no_clear_shell` - Не очищать консоль перед выполнением | Воспроизведение фото/видео данных |

### [Конфигурационный файл](https://github.com/DmitryRyumin/pkgs/blob/master/pvv/pvv/configs/config.json)

#### Параметры

| Параметры `json` | Типы | Описания | Допустимые значения |
| ---------------- | ---  | -------- | ------------------- |
| metadata | bool | Вывод метаданных | - |
| window_name | str | Имя окна | - |
| resize | dict | Размер окна для масштабирования | От `0` до `∞` |
| text_color | dict | Цвет текстов | От `0` до `255` |
| background_color | dict | Цвет фона текстов | От `0` до `255` |
| label_scale | float | Коэффициент масштабирования шрифта | От `>0.0` до `2.0` |
| labels_thickness | int | Толщина линии шрифта | От `1` до `4` |
| labels_base_coords | int | Начальные координаты текстов | От `0` до `100` |
| labels_padding | int | Внутренний отступ для текстов | От `0` до `30` |
| clear_image_buffer | bool | Очистка буфера с изображением | - |
| real_time | bool | Воспроизведение фото/видеопотока с реальным количеством FPS | - |
| repeat | bool | Повторение воспроизведения видеопотока | - |
| fps | int | Пользовательский FPS<br>`"real_time" = true` | От `0` до `60` |

#### Горячие клавиши

| Клавиши | Сценарий |
| ------- | -------  |
| `esc` | Закрытие окна приложения |
| `r` | Повторение воспроизведения видеопотока |

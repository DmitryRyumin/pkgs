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

## Обновление

```shell script
pip install --upgrade pvv
```

## Зависимости

| Пакеты | Минимальная версия | Текущая версия |
| ------ | ------------------ | -------------- |
`filem` | `19.10.13.0` | ![PyPI](https://img.shields.io/pypi/v/filem) |
`opencv-contrib-python` | `4.1.1.26` | ![PyPI](https://img.shields.io/pypi/v/opencv-contrib-python) | 
`PyOpenGL` | `3.1.0` | ![PyPI](https://img.shields.io/pypi/v/PyOpenGL) |

## Класс для воспроизведения фото/видео данных - [смотреть](https://github.com/DmitryRyumin/pkgs/blob/master/pvv/pvv/viewer.py)

<h4 align="center"><span style="color:#EC256F;">Примеры</span></h4>

| Файлы/скрипты | Аргументы командной строки | Описания |
| ------------- | -------------------------- | -------- |
| [play.py](https://github.com/DmitryRyumin/pkgs/blob/master/pvv/pvv/samples/play.py)<br>`pvv_play` | `--file str` - Путь к файлу<br>`--config str` - Путь к конфигурационному файлу<br>`--automatic_update` - Автоматическая проверка конфигурационного файла в момент работы программы (работает при заданном `--config`)<br>`--frames_to_update int=25` - Через какое количество шагов проверять конфигурационный файл (работает при `--automatic_update`)<br>`--no_clear_shell` - Не очищать консоль перед выполнением | Воспроизведение фото/видео данных |

### [Конфигурационный файл](https://github.com/DmitryRyumin/pkgs/blob/master/pvv/pvv/configs/config.json)

#### Параметры

| Параметры `json` | Типы | Описания | Допустимые значения |
| ---------------- | ---  | -------- | ------------------- |
| metadata | bool | Вывод метаданных | - |
| window_name | str | Имя окна | - |
| resize | dict | Размер окна для масштабирования | - |
| text_color | dict | Цвет текстов | От `0` до `255` |
| background_color | dict | Цвет фона текстов | От `0` до `255` |
| label_scale | float | Коэффициент масштабирования шрифта | От `0.0` до `2.0` |
| clear_image_buffer | bool | Очистка буфера с изображением | - |
| real_time | bool | Воспроизведение фото/видеопотока с реальным количеством FPS | - |

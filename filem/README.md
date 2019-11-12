# Работа с файлами

![PyPI](https://img.shields.io/pypi/v/filem)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/filem)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/filem)
![PyPI - Status](https://img.shields.io/pypi/status/filem)
![PyPI - License](https://img.shields.io/pypi/l/filem)

## [История релизов](https://github.com/DmitryRyumin/pkgs/blob/master/filem/NOTES.md)

## Установка

```shell script
pip install filem
```

## Обновление

```shell script
pip install --upgrade filem
```

## Зависимости

| Пакеты | Минимальная версия | Текущая версия |
| ------ | ------------------ | -------------- |
`core2pkgs` | `19.11.11.0` | ![PyPI](https://img.shields.io/pypi/v/core2pkgs) | 
`pandas` | `0.25.3` | ![PyPI](https://img.shields.io/pypi/v/pandas) |
`xmltodict` | `0.12.0` | ![PyPI](https://img.shields.io/pypi/v/xmltodict) |

## Класс для работы с файлами - [смотреть](https://github.com/DmitryRyumin/pkgs/blob/master/filem/filem/file_manager.py)

<h4 align="center"><span style="color:#EC256F;">Примеры</span></h4>

| Файлы/скрипты | Аргументы командной строки | Описания |
| ------------- | -------------------------- | -------- |
| [search_file.py](https://github.com/DmitryRyumin/pkgs/blob/master/filem/filem/samples/search_file.py)<br>`filem_search_file` | `--file str` - Путь к файлу<br>`--create` - Создание файла в случае его отсутствия<br>`--no_clear_shell` - Не очищать консоль перед выполнением | Поиск файла |
| [clear_folder.py](https://github.com/DmitryRyumin/pkgs/blob/master/filem/filem/samples/clear_folder.py)<br>`filem_clear_folder` | `--path str` - Путь к директории<br>`--no_clear_shell` - Не очищать консоль перед выполнением | Очистка директории |

### Класс для работы с CSV - [смотреть](https://github.com/DmitryRyumin/pkgs/blob/master/filem/filem/csv.py)

<h4 align="center"><span style="color:#EC256F;">Примеры</span></h4>

| Файлы/скрипты | Аргументы командной строки | Описания |
| ------------- | -------------------------- | -------- |
| [load_csv.py](https://github.com/DmitryRyumin/pkgs/blob/master/filem/filem/samples/load_csv.py)<br>`filem_load_csv` | `--file str` - Путь к файлу CSV<br>`--lines int=0` - Количество строк для отображения (По умолчанию: все строки)<br>`--no_clear_shell` - Не очищать консоль перед выполнением | Загрузка CSV файла |
| [extract_columns_csv.py](https://github.com/DmitryRyumin/pkgs/blob/master/filem/filem/samples/extract_columns_csv.py)<br>`filem_extract_columns_csv` | `--file str` - Путь к файлу CSV<br>`--lines int=0` - Количество строк для отображения (По умолчанию: все строки)<br>`--columns int=[0]` - Список номеров столбцов для извлечения (По умолчанию: все столбцы)<br>`--no_clear_shell` - Не очищать консоль перед выполнением | Извлечение указанных столбцов из CSV файла |

### Класс для работы с JSON - [смотреть](https://github.com/DmitryRyumin/pkgs/blob/master/filem/filem/json.py)

<h4 align="center"><span style="color:#EC256F;">Примеры</span></h4>

| Файлы/скрипты | Аргументы командной строки | Описания |
| ------------- | -------------------------- | -------- |
| [load_json.py](https://github.com/DmitryRyumin/pkgs/blob/master/filem/filem/samples/load_json.py)<br>`filem_load_json` | `--file str` - путь_к_файлу_JSON<br>`--lines int=0` - Количество строк для отображения (По умолчанию: все строки)<br>`--no_clear_shell` - Не очищать консоль перед выполнением | Загрузка JSON файла |

### Класс для работы с XML - [смотреть](https://github.com/DmitryRyumin/pkgs/blob/master/filem/filem/xml.py)

<h4 align="center"><span style="color:#EC256F;">Примеры</span></h4>

| Файлы/скрипты | Аргументы командной строки | Описания |
| ------------- | -------------------------- | -------- |
| [load_xml.py](https://github.com/DmitryRyumin/pkgs/blob/master/filem/filem/samples/load_xml.py)<br>`filem_load_xml` | `--file str` - путь_к_файлу_XML<br>`--no_clear_shell` - Не очищать консоль перед выполнением | Загрузка XML файла |
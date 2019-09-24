# Работа с файлами

![PyPI](https://img.shields.io/pypi/v/filem)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/filem)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/filem)
![PyPI - Status](https://img.shields.io/pypi/status/filem)
![PyPI - License](https://img.shields.io/pypi/l/filem)

## Установка

```shell script
pip install filem
```

## Обновление

```shell script
pip install --upgrade filem
```

## Зависимости

- `core2pkgs`

## Класс для работы с файлами - [смотреть](https://github.com/DmitryRyumin/pkgs/blob/master/filem/filem/file_manager.py)

<h4 align="center"><span style="color:#EC256F;">Примеры</span></h4>

| Файлы/скрипты | Аргументы командной строки | Ссылки | Описания |
| ------------- | -------------------------- | ------ | -------- |
| search_file.py<br>`filem_search_file` | `--file str` - Путь к файлу<br>`--create` - Создание файла в случае его отсутствия<br>`--no_clear_shell` - Не очищать консоль перед выполнением | [Смотреть](https://github.com/DmitryRyumin/pkgs/blob/master/filem/filem/samples/search_file.py) | Поиск файла |
| clear_folder.py<br>`filem_clear_folder` | `--path str` - Путь к директории<br>`--no_clear_shell` - Не очищать консоль перед выполнением | [Смотреть](https://github.com/DmitryRyumin/pkgs/blob/master/filem/filem/samples/clear_folder.py) | Очистка директории |

### Класс для работы с CSV - [смотреть](https://github.com/DmitryRyumin/pkgs/blob/master/filem/filem/csv.py)

<h4 align="center"><span style="color:#EC256F;">Примеры</span></h4>

| Файлы/скрипты | Аргументы командной строки | Ссылки | Описания |
| ------------- | -------------------------- | ------ | -------- |
| load_csv.py<br>`filem_load_csv` | `--file str` - Путь к файлу CSV<br>`--lines int=0` - Количество строк для отображения (По умолчанию: все строки)<br>`--no_clear_shell` - Не очищать консоль перед выполнением | [Смотреть](https://github.com/DmitryRyumin/pkgs/blob/master/filem/filem/samples/search_file.py) | Загрузка CSV файла |
| extract_columns_csv.py<br>`filem_extract_columns_csv` | `--file str` - Путь к файлу CSV<br>`--lines int=0` - Количество строк для отображения (По умолчанию: все строки)<br>`--columns int=[0]` - Список номеров столбцов для извлечения (По умолчанию: все столбцы)<br>`--no_clear_shell` - Не очищать консоль перед выполнением | [Смотреть](https://github.com/DmitryRyumin/pkgs/blob/master/filem/filem/samples/extract_columns_csv.py) | Извлечение указанных столбцов из CSV файла |

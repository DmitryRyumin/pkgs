"""
Установка пакета
"""

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
import sys                  # Доступ к некоторым переменным и функциям Python
import pkg_resources        # Работа с ресурсами внутри пакетов
import distutils.text_file  # Работа с текстовыми файлами
import maskrcnnkeras        # Mask R-CNN

from pathlib import Path  # Работа с путями файловой системы с учетом специфики OC
from setuptools import setup, find_packages  # Упаковка проекта

# ######################################################################################################################
# Минимальная версии
# ######################################################################################################################
MIN_PYTHON_VERSION = (3, 7)  # Python
MIN_PIP_VERSION = (10, 0)    # Pip

# ######################################################################################################################
# Формирование данных для упаковки
# ######################################################################################################################
# Проверка версии Python
print(sys.version_info[:2])
if sys.version_info[:2] < MIN_PYTHON_VERSION:
    raise RuntimeError("Требуется версия Python >= {}.{}".format(MIN_PYTHON_VERSION[0], MIN_PYTHON_VERSION[1]))


# Получение пакетов рекомендованный к установке из файла
def parse_requirements(path_to_req):
    """
    Получение пакетов рекомендованный к установке из файла

    (str) -> list

    Аргументы:
       path_to_req - Путь к файлу с рекомендованными пакетами к установке

    Возвращает: list с рекомендованными пакетами к установке
    """

    # Проверка аргументов
    if type(path_to_req) is not str or not path_to_req:
        raise RuntimeError('Неверные типы аргументов в "{}" ...'.format(parse_requirements.__name__))

    pip_ver = pkg_resources.get_distribution('pip').version  # Версия PIP
    pip_version = tuple(map(int, pip_ver.split('.')[:2]))  # Разбиение полученной версии PIP на MAJOR и MINOR

    # Проверка версии Pip
    if pip_version < MIN_PIP_VERSION:
        raise RuntimeError('Требуется версия pip >= {}.{}'.format(MIN_PIP_VERSION[0], MIN_PIP_VERSION[1]))

    # Список с рекомендованными пакетами к установке
    return distutils.text_file.TextFile(filename=str(Path(__file__).with_name(path_to_req))).readlines()


try:
    # Получение пакетов рекомендованный к установке из файла
    REQUIRED_PACKAGES = parse_requirements('requirements.txt')
except FileNotFoundError:
    raise RuntimeError('Файл с пакетами рекомендованными к установке не найден ...')

CLASSIFIERS = """\
Development Status :: 5 - Production/Stable
Natural Language :: Russian
Natural Language :: English
Intended Audience :: Developers
Intended Audience :: Education
Intended Audience :: Science/Research
License :: OSI Approved :: MIT License
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3 :: Only
Programming Language :: Python :: Implementation :: CPython
Topic :: Scientific/Engineering
Topic :: Scientific/Engineering :: Mathematics
Topic :: Software Development
Topic :: Software Development :: Libraries
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: MacOS :: MacOS X
Operating System :: Microsoft :: Windows
Operating System :: POSIX :: Linux
"""

# ######################################################################################################################
# Установка пакета
# ######################################################################################################################
with open('README.md', 'r', encoding='utf8') as fh:
    long_description = fh.read()

    setup(
        name=maskrcnnkeras.__name__,
        packages=find_packages(),
        license=maskrcnnkeras.__license__,
        version=maskrcnnkeras.__version__,
        author=maskrcnnkeras.__author__,
        author_email=maskrcnnkeras.__email__,
        maintainer=maskrcnnkeras.__maintainer__,
        maintainer_email=maskrcnnkeras.__maintainer_email__,
        url=maskrcnnkeras.__uri__,
        description=maskrcnnkeras.__summary__,
        long_description=long_description,
        long_description_content_type='text/markdown',
        install_requires=REQUIRED_PACKAGES,
        keywords=['maskrcnnkeras'],
        include_package_data=True,
        classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f],
        python_requires='>=3.7',
        entry_points={
            'console_scripts': [
            ],
        }
    )

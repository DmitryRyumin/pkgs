import sys

from setuptools import setup, find_packages

MIN_PYTHON_VERSION = (3, 7)

if sys.version_info[:2] < MIN_PYTHON_VERSION:
    raise RuntimeError("Требуется версия Python >= {}.{}".format(MIN_PYTHON_VERSION[0], MIN_PYTHON_VERSION[1]))

import filem

REQUIRED_PACKAGES = [
    'core2pkgs >= 19.11.11.0',
    'pandas >= 0.25.3',
    'xmltodict >= 0.12.0',
]

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

with open('README.md', 'r') as fh:
    long_description = fh.read()

    setup(
        name = filem.__name__,
        packages = find_packages(),
        license = filem.__license__,
        version = filem.__version__,
        author = filem.__author__,
        author_email = filem.__email__,
        maintainer = filem.__maintainer__,
        maintainer_email = filem.__maintainer_email__,
        url = filem.__uri__,
        description = filem.__summary__,
        long_description = long_description,
        long_description_content_type = 'text/markdown',
        install_requires=REQUIRED_PACKAGES,
        keywords = ['filem'],
        classifiers = [_f for _f in CLASSIFIERS.split('\n') if _f],
        python_requires = '>=3.7',
        entry_points = {
            'console_scripts': [
                'filem_search_file = filem.samples.search_file:main',
                'filem_clear_folder = filem.samples.clear_folder:main',
                'filem_load_csv = filem.samples.load_csv:main',
                'filem_extract_columns_csv = filem.samples.extract_columns_csv:main',
                'filem_load_json = filem.samples.load_json:main',
                'filem_load_xml = filem.samples.load_xml:main',
            ],
        }
    )

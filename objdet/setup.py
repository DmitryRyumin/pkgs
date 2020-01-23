import sys

from setuptools import setup, find_packages

MIN_PYTHON_VERSION = (3, 7)

if sys.version_info[:2] != MIN_PYTHON_VERSION:
    raise RuntimeError("Требуется версия Python = {}.{}".format(MIN_PYTHON_VERSION[0], MIN_PYTHON_VERSION[1]))

import objdet

REQUIRED_PACKAGES = [
    'pvv >= 20.1.22.0',
    'numpy >= 1.18.1'
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
        name = objdet.__name__,
        packages = find_packages(),
        license = objdet.__license__,
        version = objdet.__version__,
        author = objdet.__author__,
        author_email = objdet.__email__,
        maintainer = objdet.__maintainer__,
        maintainer_email = objdet.__maintainer_email__,
        url = objdet.__uri__,
        description = objdet.__summary__,
        long_description = long_description,
        long_description_content_type = 'text/markdown',
        install_requires=REQUIRED_PACKAGES,
        keywords = ['objdet'],
        include_package_data = True,
        classifiers = [_f for _f in CLASSIFIERS.split('\n') if _f],
        python_requires = '>=3.7, <3.8',
        entry_points = {
            'console_scripts': [
                'objdet_play = objdet.samples.detection:main',
            ],
        }
    )

import sys

from setuptools import setup, find_packages

MIN_PYTHON_VERSION = (3, 7)

if sys.version_info[:2] != MIN_PYTHON_VERSION:
    raise RuntimeError("Требуется версия Python = {}.{}".format(MIN_PYTHON_VERSION[0], MIN_PYTHON_VERSION[1]))

import pvv

REQUIRED_PACKAGES = [
    'filem >= 19.11.12.1',
    'PyOpenGL >= 3.1.5',
    'opencv-contrib-python >= 4.1.2.30',
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
        name = pvv.__name__,
        packages = find_packages(),
        license = pvv.__license__,
        version = pvv.__version__,
        author = pvv.__author__,
        author_email = pvv.__email__,
        maintainer = pvv.__maintainer__,
        maintainer_email = pvv.__maintainer_email__,
        url = pvv.__uri__,
        description = pvv.__summary__,
        long_description = long_description,
        long_description_content_type = 'text/markdown',
        install_requires=REQUIRED_PACKAGES,
        keywords = ['pvv'],
        include_package_data = True,
        classifiers = [_f for _f in CLASSIFIERS.split('\n') if _f],
        python_requires = '>=3.7',
        entry_points = {
            'console_scripts': [
                'pvv_play = pvv.samples.play:main',
            ],
        },
    )

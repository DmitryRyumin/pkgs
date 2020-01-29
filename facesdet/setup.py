import sys

from setuptools import setup, find_packages

MIN_PYTHON_VERSION = (3, 7)

if sys.version_info[:2] != MIN_PYTHON_VERSION:
    raise RuntimeError("Требуется версия Python = {}.{}".format(MIN_PYTHON_VERSION[0], MIN_PYTHON_VERSION[1]))

import facesdet

REQUIRED_PACKAGES = [
    'pvv >= 20.1.28.2',
    'numpy >= 1.18.1',
    'dlib >= 19.19.0'
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
        name = facesdet.__name__,
        packages = find_packages(),
        license = facesdet.__license__,
        version = facesdet.__version__,
        author = facesdet.__author__,
        author_email = facesdet.__email__,
        maintainer = facesdet.__maintainer__,
        maintainer_email = facesdet.__maintainer_email__,
        url = facesdet.__uri__,
        description = facesdet.__summary__,
        long_description = long_description,
        long_description_content_type = 'text/markdown',
        install_requires=REQUIRED_PACKAGES,
        keywords = ['facesdet'],
        include_package_data = True,
        classifiers = [_f for _f in CLASSIFIERS.split('\n') if _f],
        python_requires = '>=3.7',
        entry_points = {
            'console_scripts': [
                'facesdet_play = facesdet.samples.detection:main',
            ],
        },
    )

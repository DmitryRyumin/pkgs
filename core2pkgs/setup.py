from setuptools import setup, find_packages

import core2pkgs

REQUIRED_PACKAGES = [
    'argparse >= 1.4.0',
    'trml >= 2019.9.18.1'
]

with open('README.md', 'r') as fh:
    long_description = fh.read()

    setup(
        name = core2pkgs.__name__,
        packages = find_packages(),
        license = core2pkgs.__license__,
        version = core2pkgs.__version__,
        author = core2pkgs.__author__,
        author_email = core2pkgs.__email__,
        url = core2pkgs.__uri__,
        description = core2pkgs.__summary__,
        long_description = long_description,
        long_description_content_type = 'text/markdown',
        install_requires=REQUIRED_PACKAGES,
        keywords = ['core2pkgs'],
        classifiers = [
            'License :: OSI Approved :: MIT License',
            'Natural Language :: Russian',
            'Natural Language :: English',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows',
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python",
            'Programming Language :: Python :: 3.7',
            "Programming Language :: Python :: Implementation :: CPython",
            "Development Status :: 5 - Production/Stable",
            'Intended Audience :: Developers',
            'Intended Audience :: Education',
            'Intended Audience :: Science/Research',
            'Topic :: Scientific/Engineering',
            'Topic :: Scientific/Engineering :: Mathematics',
            'Topic :: Software Development',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
        python_requires = '>=3.7'
    )
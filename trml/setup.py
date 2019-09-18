from setuptools import setup, find_packages

import trml

REQUIRED_PACKAGES = [

]

with open('README.md', 'r') as fh:
    long_description = fh.read()

    setup(
        name = trml.__name__,
        packages = find_packages(),
        license = trml.__license__,
        version = trml.__version__,
        author = trml.__author__,
        author_email = trml.__email__,
        url = trml.__uri__,
        description = trml.__summary__,
        long_description = long_description,
        long_description_content_type = 'text/markdown',
        install_requires=REQUIRED_PACKAGES,
        keywords = ['shell'],
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
            'Intended Audience :: Developers',
            'Intended Audience :: Education',
            'Intended Audience :: Science/Research',
            'Topic :: Scientific/Engineering',
            'Topic :: Scientific/Engineering :: Mathematics',
            'Topic :: Software Development',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
        python_requires = '>=3.7',
        entry_points = {
            'console_scripts': [
                'trml_add_line = trml.samples.add_line:main',
                'trml_clear = trml.samples.clear:main',
            ],
        }
    )

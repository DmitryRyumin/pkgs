from setuptools import setup, find_packages

import filem

REQUIRED_PACKAGES = [
    'core2pkgs'
]

with open('README.md', 'r') as fh:
    long_description = fh.read()

    setup(
        name = filem.__name__,
        packages = find_packages(),
        license = filem.__license__,
        version = filem.__version__,
        author = filem.__author__,
        author_email = filem.__email__,
        url = filem.__uri__,
        description = filem.__summary__,
        long_description = long_description,
        long_description_content_type = 'text/markdown',
        install_requires=REQUIRED_PACKAGES,
        keywords = ['filem'],
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
        python_requires = '>=3.7',
        entry_points = {
            'console_scripts': [
                'filem_search_file = filem.samples.search_file:main',
                'filem_clear_folder = filem.samples.clear_folder:main'
            ],
        }
    )

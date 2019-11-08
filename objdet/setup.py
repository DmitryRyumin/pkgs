from setuptools import setup, find_packages

import objdet

REQUIRED_PACKAGES = [
    'pvv >= 19.11.8.0',
    'numpy >= 1.17.2',
    'tensorflow >= 2.0.0'
]

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
                'objdet_play = objdet.samples.detection:main',
            ],
        },
    )

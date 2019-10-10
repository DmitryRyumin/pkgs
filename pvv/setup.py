from setuptools import setup, find_packages

import pvv

REQUIRED_PACKAGES = [
    'filem >= 19.10.4.3',
    'PyOpenGL >= 3.1.0',
    'opencv-contrib-python >= 4.1.1.26',
]

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
                'pvv_play = pvv.samples.play:main',
            ],
        },
    )

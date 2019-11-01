from setuptools import setup, find_packages

import facesdet

REQUIRED_PACKAGES = [
    'pvv >= 19.11.1.1',
    'numpy >= 1.17.2',
    'dlib >= 19.18.0'
]

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
                'facesdet_play = facesdet.samples.detection:main',
            ],
        },
    )

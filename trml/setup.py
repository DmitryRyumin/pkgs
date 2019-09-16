from setuptools import setup, find_packages

project_name = 'trml'

REQUIRED_PACKAGES = [

]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = project_name,
    packages = find_packages(),
    license = 'MIT',
    version = "0.0.1rc2",
    author = "Dmitry Ryumin",
    author_email = "dl_03.03.1991@mail.ru",
    description = "Shell",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    install_requires=REQUIRED_PACKAGES,
    keywords = ['shell'],
    classifiers = [
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = '>=3.7',
)

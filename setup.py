from setuptools import setup

# Read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="spacy_annotator",
    packages=["spacy_annotator"],
    version="2.1.2",
    license="MIT",
    description="SpaCy annotator for Named Entity Recognition (NER) using ipywidgets.",
    author="Enrico Alemani",
    author_email="enrico.alemani@hey.com",
    url="https://github.com/ieriii/spacy-annotator",
    download_url="https://github.com/ieriii/spacy-annotator/archive/refs/tags/2.1.1.tar.gz",
    keywords=["spacy", "NER", "NLP"],
    install_requires=[
        "ipython",
        "ipywidgets>=7.5.1",
        "pandas",
        "spacy",
    ],
    zip_safe=False,
    # Enable pypi description
    long_description=long_description,
    long_description_content_type="text/markdown",
)

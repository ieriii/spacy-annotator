from setuptools import setup

# Read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'spacy_annotator',
  packages=['spacy_annotator'],
  version = '0.1',
  license='MIT',
  description = 'SpaCy annotator for Named Entity Recognition (NER) using ipywidgets.',
  author = 'Enrico Alemani',
  author_email = 'enrico.alemani@hey.com',
  url = 'https://github.com/ieriii/',
  download_url = 'https://github.com/ieriii/spacy-annotator/archive/v_01.tar.gz',
  keywords = ['spacy', 'NER', 'NLP'],
  install_requires=[
        'numpy'
        'spacy==2.2.4'
        'ipywidgets>=7.5.1'
        'ipython'
      ],
      zip_safe=False,
      
      #Enable pypi description
      long_description=long_description,
      long_description_content_type="text/markdown"
)
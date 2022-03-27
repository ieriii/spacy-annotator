# spacy-annotator

SpaCy annotator for Named Entity Recognition (NER) using ipywidgets.
The annotator allows users to quickly assign (custom) labels to one or more entities in the text, including noisy-prelabelling!   

**Features**:

* The annotator supports pandas dataframe: it adds annotations in a separate 'annotation' column of the dataframe;
* Why not use transformers to label your data for you? 
If a model is passed into the annotator, it is used to identify entities and pre-fill the annotator for you.
* The annotations adhere to spaCy format and are ready to serve as input to a spaCy NER model.   
No additional code required!

Blog post: [medium/enrico.alemani/spacy-annotator](https://medium.com/@enrico.alemani/how-to-create-training-data-for-spacy-ner-models-using-ipywidgets-c4aa71bf61a2)

## Installation
```
pip install spacy-annotator
```

## Example: annotations using spaCy model 

https://user-images.githubusercontent.com/31287731/119233291-4079be00-bb20-11eb-8a8d-7ad1436c662b.mov



For code, see [spacy_annotator demo](demo/spacy_annotator_demo.ipynb) notebook.

## Contributors
[dayalstrub-cma](https://github.com/dayalstrub-cma) - Refactored code to class, added displacy visualisation and entity ruler.   
[LeafmanZ](https://github.com/LeafmanZ) - Added `to_spacy` method.

## Contributing

1. Fork the repo on GitHub;
2. Clone the project to your own machine;
3. Commit changes to your own branch; and
4. Push your work back up to your own fork;
5. Submit a Pull request so that I can review your changes.

## Dependencies

Spacy-annotator works with SpaCy 3.X, and ipywidgets 7.X.

## References

spacy-annotator is based on [spaCy](https://spacy.io/) and [pigeon](https://github.com/agermanidis/pigeon) (see also [PigeonXT](https://github.com/dennisbakhuis/pigeonXT)).   
Many thanks to them for making their awesome libraries publicly available. Another interesting project is [Doccano](https://github.com/doccano/doccano).

**Note**:
spaCy is a great library and, most importantly, free to use. So please also consider using the https://prodi.gy/ annotator to keep supporting the spaCy deveopment.

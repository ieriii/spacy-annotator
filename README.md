# spacy-annotator
spaCy annotator for Named Entity Recognition (NER) using ipywidgets.
The annotator allows users to quickly assign custom labels to one or more entities in the text.   

**Features**:
* The annotator supports pandas dataframe (see `pandas_annotations.py`): it adds annotations in a separate 'annotation' column of the dataframe;
* If a spacy model is passed into the annotator, the model is used to identify entities in text.   
This trick of pre-labelling the example using the current best model available allows for accelerated labelling - also known as of noisy pre-labelling;
* The annotations adhere to spaCy format and are ready to serve as input to spaCy NER model.   
No additional code required!

**Note**: not using pandas dataframe? No problem. You can always label entities from text stored in a simple python list (see `list_annotations.py`);

Blog post: [medium/enrico.alemani/spacy-annotator](https://medium.com/@enrico.alemani/how-to-create-training-data-for-spacy-ner-models-using-ipywidgets-c4aa71bf61a2)

## Example code - pandas annotations
```python
import pandas as pd
import re
from spacy_annotator.pandas_annotations import annotate as pd_annotate

# Data
df = pd.DataFrame.from_dict({'full_text' : ['New York is lovely but Milan is amazing!']})

# Annotations
pd_dd = pd_annotate(df,
            col_text = 'full_text',     # Column in pandas dataframe containing text to be labelled
            labels = ['GPE', 'PERSON'], # List of labels
            sample_size=1,              # Size of the sample to be labelled
            delimiter='~',              # Delimiter to separate entities in GUI
            model = None,               # spaCy model for noisy pre-labelling
            regex_flags=re.IGNORECASE   # One (or more) regex flags to be applied when searching for entities in text
            )

# Example output
pd_dd['annotations'][0]
```

## Preview
![spacy-annotator demo](demo/spacy-annotator_demo.gif)

## Contributing
1. Fork the repo on GitHub;
2. Clone the project to your own machine;
3. Commit changes to your own branch; and
4. Push your work back up to your own fork;
5. Submit a Pull request so that I can review your changes.

## Version
ipywidgets: 7.5.1   
re: 2.2.1   
spacy: 2.2.4

## References
spacy-annotator is based on [spaCy](https://spacy.io/) and [pigeon](https://github.com/agermanidis/pigeon).   
Many thanks to them for making their awesome libraries publicly available.

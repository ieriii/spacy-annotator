# spacy-annotator
SpaCy annotator for Named Entity Recognition (NER) using ipywidgets.

The annotator allows users to quickly assign custom labels to one or more entities in the text.   
**Features**:
* the annotator supports pandas dataframe: it adds annotations in a separate 'annotation' column of the dataframe;   
* if a spacy model is passed into the annotator, the model is used to identify entities in text. This can come handy to understand how the model can be improved in an active learning fashion; 
* the annotations adhere to spaCy format and are ready to serve as input to spaCy NER model.   
No additional code required!

Blog post: [medium/enrico.alemani/spacy-annotator](https://medium.com/@enrico.alemani/how-to-create-training-data-for-spacy-ner-models-using-ipywidgets-c4aa71bf61a2)

## Example code
```python
import pandas as pd
import re
from annotator.active_annotations import annotate

# Data
df = pd.DataFrame.from_dict({'full_text' : ['I love New York']})

# Annotations
dd = annotate(df,
            col_text = 'full_text',
            labels = ['GPE', 'PERSON'],
            sample_size=1,
            model = 'en',
            regex_flags=re.IGNORECASE
            )

# Example output
dd['annotations'][0]
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

## References
spacy-annotator is based on [SpaCy](https://spacy.io/) and [pigeon](https://github.com/agermanidis/pigeon).   
Many thanks to them for making their awesome libraries publicly available.

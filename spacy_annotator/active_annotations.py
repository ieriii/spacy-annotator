import spacy
import re
import random
import numpy as np
from collections import defaultdict
from spacy_annotator.annotator_utils import filter_spans
from IPython.display import display, clear_output
from ipywidgets import Button, HTML, HBox, Textarea, Output, Layout

def annotate(df,
             col_text,
             sample_size=0.1,
             strata=None,
             model=None,
             labels=None,
             regex_flags=0,
             shuffle=False,
             include_skip=True,
             display_fn=display):
    
    """
    Build an interactive widget for annotating a list of input examples.
    Parameters
    ----------
    df = pandas dataframe containing text to be labelled
    col_text = column in pandas dataframe containing text to be labelled
    sample_size = float, size of the sample to be labelled
    strata = dict, dictionary {'key':'varname', 'cat1':prop, 'cat2':prop}, where 'key' is the name of the categorical variable to create strata,
        'cat1' and 'cat2' are the categories in the 'key' variables and 'prop' their proportion in the strata
    model = spaCy model
    labels: list(any), list of NER labels
    regex_flags: regex, one or more regex flag to apply to re.compile. (e.g. re.I|re.DOTALL). Default: no flags
    shuffle: bool, option to shuffle data
    include_skip: bool, include option to skip example while annotating
    display_fn: func, function for displaying an example to the user
    
    Returns
    -------
    annotations (list) : list of annotations in spacy format: [example text, {'entities': [(span start, span end, label)]}]
    """
    
    assert col_text is not None, 'Please provide a pandas column containing text to be labelled.'
    assert labels is not None, 'Please provide a list of labels.'
    
    
    current_index = -1
    
    
    if model is not None:
        nlp = spacy.load(model)  

    if strata is not None:
        assert sum([v for k,v in strata.items() if k !='key']) == 1, 'The sum of proportions in strata is different from 1'
        sample = (df
                  .groupby(strata['key'], group_keys=False)
                  .apply(lambda x: x.sample(frac=(len(df)*sample_size*strata[x.name]/len(x))))
                 ).reset_index(drop=True)
        
    else:
        sample = df.sample(frac=sample_size).reset_index(drop=True)
        
    if shuffle==True:
        sample = sample.sample(frac=1).reset_index(drop=True)

    if 'annotations' not in sample.columns:
        sample['annotations'] = ''

    def set_label_text():
        nonlocal count_label
        count_label.value = f'{current_index} examples annotated, {len(sample) - current_index} examples left'
        
    def reset_textarea():
        value = (';\n'.join(f'{label}: insert' for label in labels)+';')
        return value

    def show_next():
        nonlocal current_index
        current_index += 1
        set_label_text()
        if current_index >= len(sample):
            for btn in buttons:
                btn.disabled = True
            return
        
        with out:
            clear_output(wait=True)
            print ('\033[1mText:\033[0m')
            display_fn(sample[col_text][current_index])
            print('')
            
            # Active learning
            if model is not None:
                    
                with nlp.disable_pipes('ner'):
                    doc = nlp(sample[col_text][current_index])
                
                # Set probability threshold
                threshold = 0.3
                # Search for entities using beam search
                beams = nlp.entity.beam_parse([ doc ], beam_width = 16, beam_density = 0.0001)
                
                # Get scores
                entity_scores = defaultdict(float)
                for beam in beams:
                    for score, ents in nlp.entity.moves.get_beam_parses(beam):
                        for start, end, label in ents:
                            entity_scores[(start, end, label)] += score

                
                if strata is not None:
                    print(f'\033[1mEntities and scores from {sample[strata["key"]][current_index]} sample\033[0m')
                else:
                    print ('\033[1mEntities and scores\033[0m')
                
                if any(val >= threshold for val in sorted(entity_scores.values(), reverse=True)):
                    for key in entity_scores:
                        start, end, label = key
                        score = entity_scores[key]
                        if (score >= threshold):
                            print (f'{label}, {doc[start:end]}, Score: {score}')

                elif all(val< threshold for val in sorted(entity_scores.values(), reverse=True)):
                    print('No entities found')
                else:
                    print('No entities found')
    
    def add_annotation(df, annotation, regex_flags):
        
        spans=[]
        for text in annotation.split(';'):
            
            if text:
                label, items = text.split(':')
                for item in items.split(','):
                    
                    item  = item.strip()
                    label = label.strip()
                    
                    if item:   # This controls for potential input error such as input empty string after comma
                        r = re.compile(f'\\b{item}\\b', flags=regex_flags)
                        spans.extend([(span.start(), span.end(), label) for span in r.finditer(sample[col_text][current_index])])
                    
                    else:
                        continue
                
            else:
                continue
        
        # If spans overlap, keep the (first) longest spans
        spans = filter_spans(spans)
            
        # Define entities for each text
        entities = {'entities': spans}
        
        # Add entities to dataframe
        df.at[current_index, 'annotations'] = (df[col_text][current_index], entities)
  
        show_next()

    def skip(btn):
        show_next()
    
    def finish(btn):
        for btn in buttons:
            btn.disabled = True
        return

    count_label = HTML()
    print('\033[1mInstructions\033[0m \nInput must be in the following format: \nlabelA: item1, item2; \nlabelB: itemX, itemZ; \n\nIf no entities in text, leave as is and press submit. \nSimilarly, if no entities for a particular label, leave as is (or delete the line for that label). \n\nButtons: \n*submit inserts new annotation (or overwrites existing one if one is present). \n*skip moves forward and leaves empty string (or existing annotation if one is present). \n*finish terminates the annotation session.')
    set_label_text()
    display(count_label)

    buttons = []
    
    # Textarea
    def get_bigger(args):        
        ta.rows = ta.value.count('\n') + 1
    ta = Textarea(value = (';\n'.join(f'{label}: insert' for label in labels)+';'),                
                rows=len(labels),                            
                layout=Layout(width="auto"))
    ta.observe(get_bigger, 'value')
    display(ta)
    
    # Buttons
    btn = Button(description='submit')
    def on_click(btn):
        add_annotation(sample, ta.value, regex_flags)
        ta.value = reset_textarea()
    btn.on_click(on_click)
    buttons.append(btn)

    if include_skip:
        btn = Button(description='skip')
        btn.on_click(skip)
        buttons.append(btn)
    
    btn = Button(description='finish')
    btn.on_click(finish)
    buttons.append(btn)
    
    box = HBox(buttons)
    display(box)

    out = Output()
    display(out)

    show_next()
    
    return sample

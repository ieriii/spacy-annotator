# TODO review requirements
from collections import defaultdict
from IPython.display import clear_output, display, display_html
from ipywidgets import Button, HTML, HBox, Text, Output, Layout
import numpy as np
import pandas as pd
import re
import random
import spacy
from spacy import displacy

# TODO review
from .annotator_utils import filter_spans

# TODO review
from .pandas_annotations import annotate
from .list_annotations import annotate

class Annotator: # TODO (object) ?
    # TODO clean up
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
    shuffle (bool):, option to shuffle data
    delimiter: str, delimiter to separate entities in GUI. Default: ',' (i.e. comma)
    include_skip: bool, include option to skip example while annotating
    display_fn: func, function for displaying an example to the user
    
    Returns
    -------
    annotations (list): list of annotations in spacy format: [example text, {'entities': [(span start, span end, label)]}]
    """
    
    def __init__(
        self,
        *,
         model=None,
         labels,
         delimiter=',',
#          regex_flags=0,
         include_skip=True,
    ):
        self.model = model
        if self.model is not None:
            self.nlp = model
        else:
            # TODO think of better solution?
            self.nlp = spacy.load("en_core_web_sm", disable=["tagger", "parser"])
        self.labels = labels # TODO check spacy terminology
        self.delimiter = delimiter
        self.include_skip = include_skip
    
    @property
    def instructions(self):
        print(
            # TODO clean up
            """
            \033[1mInstructions\033[0m \n
            For each entity type, input must be a DELIMITER separated string. \n
            If no entities in text, leave as is and press submit.
            Similarly, if no entities for a particular label, leave as is. \n
            Buttons: \n
            \t * submit inserts new annotation (or overwrites existing one if one is present). \n
            \t * skip moves forward and leaves empty string (or existing annotation if one is present). \n
            \t * finish terminates the annotation session.
            """
        )
        
    def _load_data(self, df, sample_size=1,):
        df_out = df.copy()
#         if strata is not None:
#             assert sum([v for k,v in strata.items() if k !='key']) == 1, 'The sum of proportions in strata is different from 1'
#             sample = (df
#                       .groupby(strata['key'], group_keys=False)
#                       .apply(lambda x: x.sample(frac=(len(df)*sample_size*strata[x.name]/len(x))))
#                      ).reset_index(drop=True)

#         else:
#             sample = df.sample(frac=sample_size).reset_index(drop=True)

#         if shuffle==True:
#             sample = sample.sample(frac=1).reset_index(drop=True)

        if 'annotations' in df.columns:
            raise Exception("Dataframe already has an annotations column, I don't want to overwrite this.")
        else:
            df_out['annotations'] = ''
        
        return df_out
    
    def __add_annotation(self, df, col_text, current_index, annotations): # , regex_flags):
        spans=[]
        for label, items in annotations.items():
            if items:
                for item in items.split(self.delimiter):
                    item  = item.strip()
                    if item: ## This controls for potential input error such as input empty string after comma
                        # TODO review
                        r = re.compile(f'\\b{item}\\b') # , flags=regex_flags)
                        spans.extend([(span.start(), span.end(), label) for span in r.finditer(df[col_text][current_index])])
                    else:
                        continue
            else:
                continue
        # If spans overlap, keep the (first) longest spans
        # TODO review
        spans = filter_spans(spans)
        # Define entities for each text
        entities = {'entities': spans}
        # Add entities to dataframe
        df.at[current_index, 'annotations'] = (df[col_text][current_index], entities)
    
    def annotate(
        self, 
        *,
        df, 
        col_text,
#          sample_size=1,
#          shuffle=False,
#          strata=None,
        show_instructions=False, 
        **kwargs
    ):
        ## CHECK INPUTS ----
        
        assert col_text is not None, 'Please provide a name of column containing text to be labelled.'

        ## PRE-PROCESS DATA ---
        
        sample = self._load_data(df, **kwargs)
        
        ## IPYWIDGET FUNCS ----
            
        def skip(btn):
            show_next()

        def finish(btn):
            for btn in buttons:
                btn.disabled = True
            return
        
        def submit(btn):
            self.__add_annotation(sample, col_text, current_index, {t.description: t.value for t in textboxes.values()}) # TODO , regex_flags)
            for textbox in textboxes.values():
                textbox.value = ""
            show_next()
            
        def set_label_text():
            nonlocal count_label
            count_label.value = f'{current_index} examples annotated, {len(sample) - current_index} examples left'
            
        def reset_textarea():
            value = (';\n'.join(f'{label}: insert' for label in self.labels)+';')
            return value

        def show_next():
            nonlocal current_index
            current_index += 1
            set_label_text()
            if current_index >= len(sample):
                for btn in buttons:
                    btn.disabled = True
                with out:
                    clear_output(wait=True)
                    print ("\033[1mThat's all folks!\033[0m\n")
            else:
                with out:
                    clear_output(wait=True)
                    print ('\033[1mText:\033[0m')
                    doc = self.nlp(sample[col_text][current_index])
                    if self.model is None:
                        doc.ents = []
                    for label in textboxes.keys():
                        textboxes[label].value = ", ".join([ent.text for ent in doc.ents if ent.label_ == label])
                    # TODO remove warning of no ents on first doc
                    # TODO remove null
                    html = displacy.render(doc, style="ent")
                    display_html(html, raw=True)
                    print('')
            # TODO check out nlp.entity.beam_parse in spacy_annotator.pandas_annotations.annotate
            # understand threshold used by default, etc.
            # see https://stackoverflow.com/questions/46934523/spacy-ner-probability

        ## IPYWIDGET ----
        
        if show_instructions:
            self.instructions
        
        buttons = []
        
        btn = Button(description='submit', button_style="success")
        btn.on_click(submit)
        buttons.append(btn)

        if self.include_skip:
            btn = Button(description='skip', button_style="danger")
            btn.on_click(skip)
            buttons.append(btn)
            
#         btn = Button(description='previous')
#         # TODO add "previous" button, cf pigeonXT
#         buttons.append(btn)
        
        btn = Button(description='finish')
        btn.on_click(finish)
        buttons.append(btn)
        
        current_index = -1
        count_label = HTML()
        
        set_label_text()
        display(count_label)

        # TODO rename to meaningful names: entities, text, buttons, etc.
        textboxes = {label:
                     Text(
                         value='',
                         description=f'{label}',
                         placeholder=f'ent one{self.delimiter} ent two{self.delimiter} ent three',
                         #     disabled=False,
                         layout=Layout(width="auto")
                     ) for label in self.labels
                    }
        display(*textboxes.values())

        box = HBox(buttons)
        display(box)

        out = Output()
        display(out)

        show_next()

        return sample

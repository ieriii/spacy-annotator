import re
import random
from spacy_annotator.annotator_utils import filter_spans
from IPython.display import display, clear_output
from ipywidgets import Button, HTML, HBox, Textarea, Output, Layout

def annotate(examples,
             labels=None,
             regex_flags = 0,
             shuffle=False,
             include_skip=True,
             display_fn=display):
    
    """
    Build an interactive widget for annotating a list of input examples.
    Parameters
    ----------
    examples: list(any), list of items to annotate
    labels: list(any), list of NER labels
    regex_flags: regex, one or more regex flag to apply to re.compile. (e.g. re.I|re.DOTALL). Default: no flags
    shuffle: bool, shuffle the examples before annotating
    include_skip: bool, include option to skip example while annotating
    display_fn: func, function for displaying an example to the user
    
    Returns
    -------
    annotations (list) : list of annotations in spacy format: [example text, {'entities': [(span start, span end, label)]}]
    """
    
    assert labels is not None, 'Please provide a list of labels'

    examples = list(examples)
    if shuffle:
        random.shuffle(examples)

    annotations = []
    current_index = -1

    def set_label_text():
        nonlocal count_label
        count_label.value = f'{len(annotations)} examples annotated, {len(examples) - current_index} examples left'
        
    def reset_textarea():
        value = (';\n'.join(f'{label}: insert' for label in labels)+';')
        return value
    
    def show_next():
        nonlocal current_index
        current_index += 1
        set_label_text()
        if current_index >= len(examples):
            for btn in buttons:
                btn.disabled = True
            print('Annotation done.')
            return
        with out:
            clear_output(wait=True)
            display_fn(examples[current_index])

    def add_annotation(annotation, regex_flags):
        
        spans=[]
        for text in annotation.split(';'):
            
            if text:
                label, items = text.split(':')
                for item in items.split(','):
                    
                    item  = item.strip()
                    label = label.strip()
                    
                    if item:   # This controls for potential input error such as input empty string after comma
                        r = re.compile(f'\\b{item}\\b', flags=regex_flags)
                        spans.extend([(span.start(), span.end(), label) for span in r.finditer(examples[current_index])])
                    
                    else:
                        continue
                
            else:
                continue
        
        # If spans overlap, keep the (first) longest spans
        spans = filter_spans(spans)
            
        # Define entities for each text
        entities = {'entities': spans}
        
        # Add entities to annotations
        annotations.append((examples[current_index], entities))
            
        show_next()

    def skip(btn):
        show_next()

    count_label = HTML()
    print('\033[1mInstructions\033[0m \nInput must be in the following format: \nlabelA: item1, item2; \nlabelB: itemX, itemZ; \n\nIf no entities in text, leave as is and press submit. \nSimilarly, if no entities for a particular label, leave as is (or delete the line for that label).')
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
        add_annotation(ta.value, regex_flags)
        ta.value = reset_textarea()
    btn.on_click(on_click)
    buttons.append(btn)

    if include_skip:
        btn = Button(description='skip')
        btn.on_click(skip)
        buttons.append(btn)

    box = HBox(buttons)
    display(box)

    out = Output()
    display(out)

    show_next()

    return annotations
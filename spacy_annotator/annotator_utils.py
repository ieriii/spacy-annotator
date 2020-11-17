def filter_spans(spans):
    """
    Filter a sequence of spans and remove duplicates or overlaps. 
    It is useful for creating named entities (where one token can only be part of one entity). 
    When spans overlap, the (first) longest span is preferred over shorter spans.
    
    Parameters
    ----------
    spans (list of tuples): The spans to filter.
    
    Returns
    -------
    annotatinos (list): The filtered spans
    """
    
    
    get_sort_key = lambda span: (span[1] - span[0], -span[0])
    sorted_spans = sorted(spans, key=get_sort_key, reverse=True)

    result = []
    seen_tokens = set()
    for span in sorted_spans:     
        
        # Check for end - 1 here because boundaries are inclusive
        if span[0] not in seen_tokens and span[1] - 1 not in seen_tokens:
            result.append(span)
        seen_tokens.update(range(span[0], span[1]))

    return result
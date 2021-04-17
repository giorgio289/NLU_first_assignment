# NLU_first_assignment
## Requirements:
To run the code you need at least Python 2.7 and [SpaCy](https://spacy.io/)<br>
To install SpaCy run:<br>
```pip install spacy``` or ```conda install -c conda-forge spacy```<br>
Download english language with:<br>
```python -m spacy download en_core_web_sm```<br>
## Short code description
The code available at [main.py]() is divided in two section: the first is made of the required functions and the second of a test script.
### Functions:
The available functions are:
* ```extract_path(sent)``` which extracts the path from ROOT to each of the token in the sentence passed as input
* ```extract_subtree(sent)``` which extracts the subtree for each token in the sentence
* ```check_if_subtree_ordered(sent,segment)``` and ```check_if_subtree_unordered(sent,segment)``` which check if a giver segment is a subtree respectively condidering and not condidering the order of the elements
* ```span_head(lista)``` and ```span_head_with_context(lista,context)``` which return the root of a span respectively considering the context or not
* ```subj_dobj_iobj(sent)``` which  returns *nsbj*, *iobj* and *dobj* if they are present
### Test script:
Takes as input a sentence and a segment and uses them as input to the functions, then prints all the result in a pretty way
### Note:
For a more detailed description of the code see [report.pdf]()

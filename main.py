import spacy
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
from collections import defaultdict

# extract a path of dependency relations from the ROOT to a token
# input: a sentece as string
# uotput: a dictionary of the form token: [path]
def extract_path(sent):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(sent)
    out={}
    for token in doc:
        reverse_path=[tok.dep_ for tok in token.ancestors]
        out[token.text]=reverse_path[::-1]
    return out
    
# extract subtree of a dependents given a token
# input: a sentence in form o a string
# output: a dictionary of the form token: [subtree]
def extract_subtree(sent):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(sent)
    out={}
    for token in doc:
        out[token.text]=[tok.text for tok in token.subtree]
    return out

# check if a given list of tokens (segment of a sentence) forms a subtree connsidering the order
# input: a sentence in form of a string and a segment in form of a list of string
# ouput: True if the segment is a subtree else False
def check_if_subtree_ordered(sent,segment):
    for subtree in extract_subtree(sent).values():
        if subtree==segment:
            return True
    return False

# check if a given list of tokens (segment of a sentence) forms a subtree without connsidering the order
# input: a sentence in form of a string and a segment in form of a list of string
# ouput: True if the segment is a subtree else False
def check_if_subtree_unordered(sent,segment):
    segment.sort()
    for subtree in extract_subtree(sent).values():
        subtree.sort()
        if subtree == segment:
            return True
    return False

# identify head of a span, given its tokens without considering the context of the sentece
# input: span in form of list of string
# output: root of the span as token
def span_head(lista):
    nlp = spacy.load('en_core_web_sm')
    sent=' '.join(lista)
    doc = nlp(sent)
    span=doc[0:-1]
    return span.root

# identify head of a span, given its tokens considering the context of the sentece
# input: span in form of list of string
# output: list of root of the span as token
def span_head_with_context(lista,context):
    nlp = spacy.load('en_core_web_sm')
    p_matcher = PhraseMatcher(nlp.vocab)
    sent = ' '.join(lista)
    p_matcher.add("Rule", [nlp(sent)])
    doc = nlp(context)
    match = p_matcher(doc)
    if match:
        out=[]
        for match_id,start,end in match:
            span = doc[start:end]
            out.append(span.root)
        return out
    else:
        return span_head(lista)
    

# extract sentence subject, direct object and indirect object spans
# input: a sentence in form of a string
# output: a dictionary of the form dependency: [tokens]
def subj_dobj_iobj(sent):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(sent)
    out = defaultdict(list)
    matcher = Matcher(nlp.vocab)
    elem_to_find = ['nsubj','dobj','dative']
    for string in elem_to_find:
        matcher.add(string, [[{"DEP": string}]])
    matches = matcher(doc)
    for match_id, start, end in matches:
        for nc in doc.noun_chunks:
            span_=doc[start:end]
            if span_[0] in nc:
                out[nlp.vocab.strings[match_id]].append(nc)
    return out
 
    
# FUNCTION TESTS:

# print dictionary in a pretty way
# input: a dictionary
# ouput: None
def print_dict(dictionary):
    for key, value in dictionary.items():
        print("{0}: {1}".format(key,value))

# Inputs        
#sentence = "He was a genius of the best kind and his dog was green."
sentence = "I saw the man with a telescope"
segment = ['the','man']
span_obj = ['with','a','telescope']

print("---------- BEGIN ----------\n")
print("The the sentence used is: \""+sentence+"\"")
print("\nThe depency path for each token of the sentence are:")
print_dict(extract_path(sentence))
print("\nThe subtrees for each token of the sentence are:")
print_dict(extract_subtree(sentence))
if check_if_subtree_ordered(sentence,segment):
    print("\nThe ordered segment "+str(segment)+" IS a subtree")
else:
    print("\nThe ordered segment "+str(segment)+" IS NOT a subtree")
if check_if_subtree_unordered(sentence,segment):
    print("The unordered segment "+str(segment)+" IS a subtree")
else:
    print("The unordered segment "+str(segment)+" IS NOT a subtree")
print("\nThe head of the span "+str(span_obj)+" without considering the context is: "+span_head(span_obj).text)
print("The head of the span "+str(span_obj)+" considering the context is: "+str(span_head_with_context(span_obj,sentence)))
print("\nIf present subjects, direct objects and indirect objects of the sentence are: ")
print_dict(subj_dobj_iobj(sentence))
print("\n---------- END ----------\n")
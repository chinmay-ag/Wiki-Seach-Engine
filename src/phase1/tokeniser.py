#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 12:25:41 2017

@author: chinmay
"""
###########tokenization, case folding and stop words removal implementation##
###Try for stemming and call indexer from here.#########

import re
from nltk.corpus import stopwords
from Stemmer import Stemmer

#regex
exclude1='<.*?>'
exclude2='nbsp'
stop_words = set(stopwords.words('english'))

def tokenise(value,identifier,category,content_stop):
    token_list=[]
    final_list=[]
    value=re.sub(exclude1," ",value)
    value=re.sub(exclude2," ",value)
    value=re.sub(r'[^a-zA-Z]'," ",value)
    value=value.lower()
    if category=='e':
        value=re.sub(r'(http|www|com)'," ",value)
    if category=='c':
        value=re.sub(r'category'," ",value)
    token_list=value.split()    
    for w in token_list:
        if w not in content_stop.keys():
            final_list.append(w)
#    stemmer = PorterStemmer()
    stemmer=Stemmer("english")
    final_list=[ stemmer.stemWord(key) for key in final_list ]
#    final_list = [stemmer.stem(plural,0, len(plural)-1) for plural in final_list] 
    if final_list:
        #call next function here.
        return (final_list)    
    ####after work of token_list is done####
    token_list=[]
    final_list=[]

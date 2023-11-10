import sys
import os
import nltk
import ssl
from nltk.tokenize import word_tokenize, sent_tokenize
from transformers import AutoTokenizer, AutoModel
from operator import itemgetter
import string
from nltk.stem.snowball import PorterStemmer
from nltk.corpus import stopwords
from collections import Counter
from scipy.interpolate import make_interp_spline
import numpy as np
import pandas as pd
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import Epsilla
from pyepsilla import vectordb
from sentence_transformers import SentenceTransformer
from typing import List
from glob import glob

import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')


def reading(fileName):
    f = open(fileName, "r")
    content = f.read() 
    f.close()
    return content

def writing(input, filename):
    f = open(filename, 'w')
    f.write(input)
    f.close()
    
# # Method1: ------------------------------------->
# from langchain.document_loaders import WebBaseLoader
# webs = ['https://www.mtholyoke.edu/academics/find-your-program/computer-science']


# datas = []
# for web in webs:
#     loader = WebBaseLoader(web)
#     data = loader.load()
#     datas.append(data[0].page_content)

# if (os.getcwd() != "/Users/astridz/Documents/Moho_Bot/Documents_collection"):
#     os.chdir('Documents_collection')
    
# for n, data in enumerate(datas):
#     writing(data, f"page{n}.txt")
    
# os.chdir('../')

# # ------------------------------------->

from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(string=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

URLs = reading("URL.txt")
URLList = URLs.split()

if (os.getcwd() != "/Users/astridz/Documents/Moho_Bot/Documents_collection"):
        os.chdir('Documents_collection')
for link in URLList:
    pure_name = link.split('/')[-1]
    html = urllib.request.urlopen(link).read()
    document = text_from_html(html)
    document_tokenize = " ".join(nltk.sent_tokenize(document))
    
    writing(document_tokenize, f"{pure_name}.txt")




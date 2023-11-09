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


#run in terminal:
# # # if (os.getcwd() != "/Users/astridz"):
# # #     os.chdir('/Users/astridz')
# # # docker pull epsilla/vectordb
# # # docker run --pull=always -d -p 8888:8888 epsilla/vectordb


def reading(fileName):
    f = open(fileName, "r")
    content = f.read() 
    f.close()
    return content


# Local embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

class LocalEmbeddings():
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return model.encode(texts).tolist()

embeddings = LocalEmbeddings()
files = glob("./Documents_collection/*")

splitted_documents = []
for file in files:
    
    loader = TextLoader(file)
    documents = loader.load()
    
    splitted_documents.extend(CharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200).split_documents(documents))
 
    print("splited document size:" , len(splitted_documents))
    
    client = vectordb.Client()
    
    # Connect to Epsilla as knowledge base.
    vector_store = Epsilla.from_documents(
        splitted_documents,
        embeddings,
        client,
        db_path="/tmp/localchatdb",
        db_name="LocalChatDB",
        collection_name="LocalChatCollection"
    )
    
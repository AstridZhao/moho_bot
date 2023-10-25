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

def reading(fileName):
    f = open(fileName, "r")
    content = f.read() 
    f.close()
    return content

def writing(input, filename):
    f = open(filename, 'w')
    f.write(input)
    f.close()
    
from langchain.document_loaders import WebBaseLoader
web = "https://www.mtholyoke.edu/academics/find-your-program/computer-science"
loader = WebBaseLoader(web)
cs_data = loader.load()
cs_data_s = cs_data[0].page_content

#Testing:
print(os.getcwd())
if (os.getcwd() != "/Users/astridz/Documents/Moho_Bot/Documents_collection"):
    os.chdir('Documents_collection')
writing(cs_data_s, "cs_page.txt")
os.chdir('../')

# # Run in terminal :
# if (os.getcwd() != "/Users/astridz"):
#     os.chdir('/Users/astridz')

# docker pull epsilla/vectordb
# docker run --pull=always -d -p 8888:8888 epsilla/vectordb

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt')
nltk.download('stopwords')

# def preprocessing(data, stopping, stemming):# Tokenize each document in the list
#     tokenized_documents = []
#     trans = str.maketrans('','', string.punctuation)
#     sentences = nltk.sent_tokenize(data)  # Tokenize the document into sentences
#     for each in sentences:
#             #Tokenization: remove punctuation
#             each = each.translate(trans)
#             #content clear
#             each = each.replace ("\n", " ")
#             #Case folding: make lowercase
#             each = each.lower()
#             words = [nltk.word_tokenize(each)]
#             # Tokenize each sentence into words
#             tokenized_documents.extend(words)

#     stemmer = PorterStemmer()
#     stoplist = set(stopwords.words('english'))
#     eachline = []
#     output = []
    
#     for sentences in tokenized_documents:
#             #Stopping & Normalization option
#             if (stopping == True):
#                 filtered_stop = [word for word in sentences if word not in stoplist]
#                 if (stemming == True):
#                     stem_words = filtered_stop
#                     stem_words  = [stemmer.stem(w) for w in stem_words]
#                     eachline= ' '.join(stem_words)
#                 else:
#                     eachline = ' '.join(filtered_stop)
#             else:
#                 if (stemming == True):
#                     stem_words = sentences
#                     stem_words  = [stemmer.stem(w) for w in stem_words]
#                     eachline= ' '.join(stem_words)
#                 else:
#                     eachline= each
#             eachline = [eachline]
#             output.extend(eachline)
#     # print(output)
#     output_string = " ".join(output)
#     return  output_string

# # store tokenizing data into ".txt" file
# def create_db(data, filename):
#     if (os.getcwd() != "/Users/astridz/Documents/Moho_Bot/Documents_collection"):
#         os.chdir('Documents_collection')
        
#     data_string = data[0].page_content
#     data_string = data_string.replace("\n", "")
#     clean_data = preprocessing(data_string, True, False)
    
#     writing(clean_data, filename)
#     os.chdir('../')
#     AssertionError(os.getcwd() != "/Users/astridz/Documents/Moho_Bot")

# filename = "cs_page.txt"
# create_db(cs_data, filename)

# Local embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

class LocalEmbeddings():
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return model.encode(texts).tolist()

embeddings = LocalEmbeddings()

# Get list of all files in "./documents/"
# Testing: remove # !
files = glob("./Documents_collection/*")
for file in files:
    loader = TextLoader(file)
    documents = loader.load()
    #TODO: use CharacterTextSplitter when use ORIGINAL data document
    # Use Holistic view: Understanding the overall meaning of the text; 
    # Identifying the relationships between different parts of the text; Generating new text
    splitted_documents = CharacterTextSplitter(
        chunk_size=1200, 
        chunk_overlap=500).split_documents(documents)

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

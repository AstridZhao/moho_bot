import os
import ssl
# from nltk.tokenize import word_tokenize, sent_tokenize
# from nltk.stem.snowball import PorterStemmer
# from nltk.corpus import stopwords
from langchain.document_loaders import TextLoader 
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import Epsilla
from sentence_transformers import SentenceTransformer
from typing import List
from glob import glob
from langchain.vectorstores import Epsilla
from pyepsilla import vectordb
from langchain.vectorstores import Chroma

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')


#run in terminal:
# if (os.getcwd() != "/Users/astridz"):
#     os.chdir('/Users/astridz')
# docker pull epsilla/vectordb
# docker run --pull=always -d -p 8888:8888 epsilla/vectordb

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

# os.chdir("./Documents_collection/")

# files = ["statistics.txt"]

splitted_documents = []
splitter = RecursiveCharacterTextSplitter( separators=[" ", ",", "\n"],chunk_size=1000, chunk_overlap=200)

for file in files:
    loader = TextLoader(file)
    documents = loader.load()
    split_docs = splitter.split_documents(documents)
    print("Splitted document chunk size for current file:", len(split_docs))
    splitted_documents.extend(split_docs)
    # print("splited document:" , len(splitted_documents))


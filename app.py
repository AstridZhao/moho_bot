from langchain.vectorstores import Epsilla
from pyepsilla import vectordb
from sentence_transformers import SentenceTransformer
import streamlit as st
import os
import subprocess
from typing import List

# Local embedding model for embedding the question.
model = SentenceTransformer('all-MiniLM-L6-v2')

class LocalEmbeddings():
    def embed_query(self, text: str) -> List[float]:
        return model.encode(text).tolist()

embeddings = LocalEmbeddings()

# Connect to Epsilla as knowledge base.
client = vectordb.Client()
vector_store = Epsilla(
    client,
    embeddings,
    db_path="/tmp/localchatdb",
    db_name="LocalChatDB"
)
vector_store.use_collection("LocalChatCollection")

# Initialize Llama2
from transformers import AutoTokenizer
import requests
import json

model_name = 'TheBloke/Llama-2-7b-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf'
pure_name = model_name.split('/')[-1]
parts = model_name.split('/')
model_path = f"{parts[0]}/{parts[1]}"

# os.chdir('/Users/astridz/Documents/Llama.cpp')
# --------------------------------
# install llama.cpp if don't have
# install model if you don't have
# --------------------------------

st.title("💬 Moho Bot")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if question := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": question})
    
    # WaitReview: add vector search: 
    # https://github.com/epsilla-cloud/app-gallery/blob/main/local-chatbot/app.py
    #https://medium.com/@anoopjohny2000/building-a-conversational-chat-interface-with-streamlit-and-langchain-for-csvs-8c150b1f982d?source=read_next_recirc-----a5053b16f85----2---------------------81756fa8_2a08_42cb_bb9e_43cd23b2ae3a-------

    #TODO: FIX vector_store.similarity_search
    context = '\n'.join(map(lambda doc: doc.page_content, vector_store.similarity_search(question, k = 5)))
    st.chat_message("user").write(question)
    
    prompt = f'''
        You are helpful assistant to answer the user question based on the given information. 
        You can get some help from the given context to help you to summerize your answer.
        Please don't make things up or say things not mentioned in the Context. 
        Ask for more information when needed. 
        
        Question: 
            {question}
        Context: 
            {context}
        '''

    # WaitReview: call model
    os.chdir('/Users/astridz/Documents/llama.cpp')
    # command = ./main -m llama-2-7b-chat.Q4_K_M.gguf  -n 1024 -ngl 48
    # command = ['./main', '-m', pure_name, '-ngl 48', prompt]
    # ./main -m ./models/7B/ggml-model-q4_0.bin -n 1024 --repeat_penalty 1.0 --color -i -r "User:" -f ./prompts/chat-with-bob.txt
    command = f"./main -m {pure_name} -c 1024 -ngl 48 {prompt}"
    process = subprocess.Popen(command, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    output = process.stdout.read()
    content = ''
    if output:
        content = content + output
    # Change back to the parent directory using Python
    msg = { 'role': 'assistant', 'content': content }
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg['content'])
    os.chdir('/Users/astridz/Documents/Moho_Bot')
    
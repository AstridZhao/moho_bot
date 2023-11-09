from langchain.vectorstores import Epsilla
from pyepsilla import vectordb
from sentence_transformers import SentenceTransformer
import streamlit as st
import os
import subprocess
from typing import List
from transformers import AutoTokenizer
import requests
import json

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
model_name = 'TheBloke/Llama-2-7b-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf'
pure_name = model_name.split('/')[-1]
parts = model_name.split('/')
model_path = f"{parts[0]}/{parts[1]}"

# os.chdir('/Users/astridz/Documents/Llama.cpp')
# --------------------------------
# install llama.cpp if don't have
# install model if you don't have
# --------------------------------'

st.title("💬 Moho Bot")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if question := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": question})
    
    
    # https://github.com/epsilla-cloud/app-gallery/blob/main/local-chatbot/app.py
    #https://medium.com/@anoopjohny2000/building-a-conversational-chat-interface-with-streamlit-and-langchain-for-csvs-8c150b1f982d?source=read_next_recirc-----a5053b16f85----2---------------------81756fa8_2a08_42cb_bb9e_43cd23b2ae3a-------

    #TODO:  vector_store.similarity_search
    # https://python.langchain.com/docs/modules/data_connection/vectorstores/
    context = '\n'.join(map(lambda doc: doc.page_content, vector_store.similarity_search(question, k = 5)))
    # context = '\n'.join(map(lambda doc: doc.page_content, vector_store.similarity_search(question, k = 5)))
    # context = vector_store
    print(context)
    st.chat_message("user").write(question)
    
    prompt = f'''
        You are a helpful question answer assistant. 
        
        Answer the question followed the rules:
        1. Do not copy the context in your answer.
        2. Try to understand the Context and rephrase them.
        3. Please don't make things up or say things not mentioned in the Context. 
        4. If you don't know the answer, just say you don't know, and ask the user if they are interested in to know something else.
        5. The context you got is the most updated information, you should trust it.
        
        
        Based on given Context: "{context}", answer question: {question}
    '''
    
    # print(prompt)
    # WaitReview: call model
    os.chdir('/Users/chenluwang/Documents/llama.cpp')
   # command = f"./main -m {pure_name} -c 1024 -ngl 48 -p '{prompt}'"
    # ./main -m llama-2-7b-chat.Q4_K_M.gguf -c 1024 -ngl 48 -p
    command = ['./main', '-m', pure_name, '-c', '2048', '-ngl', '48', '-p', prompt]
    # print(base_command)
    # print(command)
    
    #TODO: subprocess 
    # process = subprocess.Popen(command, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    content = ''
    
    #Testing: which can print corrent output
    # try:
    #     outs, errs = process.communicate(timeout=15)
    #     print("communicated")
    # except subprocess.TimeoutExpired:
    #     process.kill()
    #     outs, errs = process.communicate()
    
    while True:
        output = process.stdout.readline()
        if output:
            content = output
        return_code = process.poll()
        if return_code is not None:
            break
    
    # result = []
    # result.append(content.pop())
    # result.append(content.pop())
    # results = " ".join(result)
    
    
    print("answer is : \n", content)
    msg = { 'role': 'assistant', 'content':content}
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg['content'])
    
    os.chdir('/Users/astridz/Documents/Moho_Bot')
    